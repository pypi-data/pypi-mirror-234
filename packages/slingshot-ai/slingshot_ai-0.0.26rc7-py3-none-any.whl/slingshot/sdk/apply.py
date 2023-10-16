from __future__ import annotations

import json
import typing
from logging import getLogger
from typing import TYPE_CHECKING, Optional

import sentry_sdk
from pydantic import ValidationError

from slingshot import schemas
from slingshot.cli.shared import create_empty_project_manifest, prompt_confirm, prompt_for_single_choice
from slingshot.schemas import ProjectManifest, requested_requirements_from_str
from slingshot.sdk import config
from slingshot.sdk.apply_diff import (
    apply_diff_to_local_manifest,
    compute_project_manifest_diff,
    detect_local_remote_diff_conflicts,
    diff_to_str,
)
from slingshot.sdk.config import client_settings
from slingshot.sdk.errors import SlingshotException, SlingshotFileNotFoundException
from slingshot.sdk.graphql import fragments
from slingshot.sdk.utils import console, edit_slingshot_yaml
from slingshot.sdk.wrapped_diff import DiffItem
from slingshot.shared.config import load_slingshot_project_config
from slingshot.shared.utils import (
    get_data_or_raise,
    machine_size_to_machine_type_gpu_count,
    machine_type_gpu_count_to_machine_size,
)

if TYPE_CHECKING:
    from slingshot.sdk.slingshot_sdk import SlingshotSDK

    EnvSpecPlan = tuple[
        list[tuple[schemas.EnvironmentSpec, str]],
        list[tuple[schemas.EnvironmentSpec, fragments.ExecutionEnvironmentSpec]],
        list[fragments.ExecutionEnvironmentSpec],
    ]
    ComponentSpecPlan = tuple[
        list[schemas.AbstractComponentSpec],
        list[tuple[schemas.AbstractComponentSpec, str]],
        list[fragments.ComponentSpec],
    ]
else:
    EnvSpecPlan = tuple
    ComponentSpecPlan = tuple

logger = getLogger(__name__)


def _convert_using_to_app_subtype(using: str) -> schemas.AppSubType:
    using = using.upper()
    using = using.replace("-", "_")
    return schemas.AppSubType(using)


class ApplyService:
    WAIT_FOR_ENV_POLL_INTERVAL = 2

    def __init__(self, sdk: "SlingshotSDK") -> None:
        if not (project := sdk.project):
            raise SlingshotException(
                "SDK has no project set.", cli="No project set. Please run 'slingshot init' or 'slingshot use'."
            )
        self._project = project
        self._sdk = sdk

    async def plan(self, config_: schemas.ProjectManifest | None = None) -> tuple[EnvSpecPlan, ComponentSpecPlan]:
        if not config_:
            config_ = load_slingshot_project_config()
        env_plan, _ = await self.plan_environments(config_)
        app_plan = await self.plan_apps(config_)
        return env_plan, app_plan

    async def plan_apps(self, config_: schemas.ProjectManifest) -> ComponentSpecPlan:
        existing_component_specs = await self._sdk.list_components()
        components_mapping: dict[schemas.ComponentType, typing.Sequence[schemas.AbstractComponentSpec]] = {
            schemas.ComponentType.RUN: config_.runs,
            schemas.ComponentType.DEPLOYMENT: config_.deployments,
        }

        component_specs_to_create = []
        component_specs_to_update = []
        component_specs_to_delete = []
        all_change_msgs = []

        # Check App Sub Types
        for app_sub_type in schemas.AppSubType:
            apps_from_sub_type = [
                app
                for app in config_.apps
                if isinstance(app, schemas.AbstractComponentSpec)
                and _convert_using_to_app_subtype(app.using) == app_sub_type
            ]
            (
                app_sub_type_specs_to_create,
                app_sub_type_component_specs_to_update,
                app_sub_type_component_specs_to_delete,
                app_sub_type_app_change_msgs,
            ) = _diff_existing_app_yaml_specs(
                existing_component_specs, apps_from_sub_type, schemas.ComponentType.APP, app_sub_type  # noqa
            )
            component_specs_to_create += app_sub_type_specs_to_create
            component_specs_to_update += app_sub_type_component_specs_to_update
            component_specs_to_delete += app_sub_type_component_specs_to_delete
            all_change_msgs += app_sub_type_app_change_msgs

        # Check Runs, Apps, Deployments
        for component_type, components in components_mapping.items():
            (
                component_type_specs_to_create,
                component_type_specs_to_update,
                component_type_specs_to_delete,
                component_type_change_msgs,
            ) = _diff_existing_app_yaml_specs(existing_component_specs, list(components), component_type)
            component_specs_to_create += component_type_specs_to_create
            component_specs_to_update += component_type_specs_to_update
            component_specs_to_delete += component_type_specs_to_delete
            all_change_msgs += component_type_change_msgs

        if all_change_msgs:
            console.print("\n".join(all_change_msgs))

        return component_specs_to_create, component_specs_to_update, component_specs_to_delete

    async def plan_environments(self, config_: schemas.ProjectManifest) -> tuple[EnvSpecPlan, set[str]]:
        existing_env_specs = await self._sdk.list_environments()
        (
            env_specs_to_create,
            env_specs_to_update,
            env_specs_to_delete,
            updated_spec_names,
            change_msgs,
        ) = _diff_existing_env_yaml_specs(existing_env_specs, config_.environments)
        if change_msgs:
            console.print("\n".join(change_msgs))
        return (env_specs_to_create, env_specs_to_update, env_specs_to_delete), updated_spec_names

    async def apply_env_specs(self, env_spec_plan: EnvSpecPlan) -> dict[str, str]:
        """
        Returns a dict mapping env spec names to env spec ids
        """
        env_specs_to_create, env_specs_to_update, env_specs_to_delete = env_spec_plan
        existing_specs = await self._sdk.list_environments()
        env_spec_name_to_id = {
            spec.execution_environment_spec_name: spec.execution_environment_spec_id for spec in existing_specs
        }

        has_env_updates = (len(env_specs_to_create) + len(env_specs_to_update) + len(env_specs_to_delete)) > 0
        if not has_env_updates:
            console.print("No changes detected to environments ✅ ")
            return env_spec_name_to_id

        for spec, spec_name in env_specs_to_create:
            try:
                new_env_spec = await self.create_env_spec(environment_name=spec_name, environment_spec=spec)
                env_spec_name_to_id[spec_name] = new_env_spec.execution_environment_spec_id
            except Exception as e:
                raise SlingshotException(f"Failed to create environment: {e}") from e

        for spec, existing_spec in env_specs_to_update:
            try:
                updated_env_spec = await self.update_env_spec(
                    environment_spec=spec, existing_execution_environment_spec=existing_spec
                )
                spec_id = updated_env_spec.execution_environment_spec_id
                env_spec_name_to_id[existing_spec.execution_environment_spec_name] = spec_id
            except Exception as e:
                raise SlingshotException(f"Failed to update environment: {e}") from e
        for env_spec_to_delete in env_specs_to_delete:
            try:
                await self.delete_env_spec(env_spec_to_delete)
            except Exception as e:
                raise SlingshotException(f"Failed to delete environment: {e}") from e
        return env_spec_name_to_id

    async def create_env_spec(
        self, environment_name: str, environment_spec: schemas.EnvironmentSpec
    ) -> fragments.ExecutionEnvironmentSpec:
        console.print(f"Creating environment '{environment_name}'...", end="")
        requested_python_requirements = [requested_requirements_from_str(i) for i in environment_spec.python_packages]
        requested_apt_requirements = [schemas.RequestedAptPackage(name=p) for p in environment_spec.apt_packages]
        create_env_spec_resp = await self._sdk.create_environment(
            name=environment_name,
            requested_python_requirements=requested_python_requirements,
            requested_apt_requirements=requested_apt_requirements,
            post_install_command=environment_spec.post_install_command,
        )
        if create_env_spec_resp.error:
            raise SlingshotException(f"Failed to create environment: {create_env_spec_resp.error}")
        console.print("✅ ")

        create_env_spec = get_data_or_raise(create_env_spec_resp)
        env_spec = await self._sdk.get_environment(create_env_spec.execution_environment_spec_id)
        assert env_spec, "Environment was not created"
        return env_spec

    async def update_env_spec(
        self,
        environment_spec: schemas.EnvironmentSpec,
        existing_execution_environment_spec: fragments.ExecutionEnvironmentSpec,
    ) -> fragments.ExecutionEnvironmentSpec:
        environment_name = existing_execution_environment_spec.execution_environment_spec_name
        execution_environment_spec_id = existing_execution_environment_spec.execution_environment_spec_id
        console.print(f"Updating environment '{environment_name}'...", end="")
        requested_python_requirements = [requested_requirements_from_str(i) for i in environment_spec.python_packages]
        requested_apt_requirements = [schemas.RequestedAptPackage(name=p) for p in environment_spec.apt_packages]
        await self._sdk.update_environment(
            name=environment_name,
            requested_python_requirements=requested_python_requirements,
            requested_apt_requirements=requested_apt_requirements,
            post_install_command=environment_spec.post_install_command,
        )
        console.print("✅ ")
        env_spec = await self._sdk.get_environment(execution_environment_spec_id)
        assert env_spec, "Environment was not updated"
        return env_spec

    async def delete_env_spec(self, env_spec: fragments.ExecutionEnvironmentSpec) -> None:
        console.print(f"Deleting environment '{env_spec.execution_environment_spec_name}'...", end="")
        await self._sdk.delete_environment(environment_id=env_spec.execution_environment_spec_id)
        console.print("✅ ")

    async def apply_component_specs(
        self, component_spec_plan: ComponentSpecPlan, env_spec_name_to_id: dict[str, str]
    ) -> None:
        component_specs_to_create, component_specs_to_update, component_specs_to_delete = component_spec_plan

        has_app_updates = (
            len(component_specs_to_create) + len(component_specs_to_update) + len(component_specs_to_delete)
        ) > 0
        if not has_app_updates:
            console.print("No changes detected to apps, runs, or deployments ✅ ")
            return

        # Note: temporary hack to make sure runs are created before everything else. This is needed because
        # Label Studio Apps now have references to run ids (which must exist before the app is created)
        run_specs_to_create = [
            component_spec
            for component_spec in component_specs_to_create
            if isinstance(component_spec, schemas.RunSpec)
        ]
        remaining_apps_to_create = [
            component_spec
            for component_spec in component_specs_to_create
            if not isinstance(component_spec, schemas.RunSpec)
        ]

        # Similarly, we need to delete runs last due to the foreign key constraint
        run_specs_to_delete = [
            component_spec
            for component_spec in component_specs_to_delete
            if component_spec.component_type == schemas.ComponentType.RUN
        ]
        remaining_apps_to_delete: list[fragments.ComponentSpec] = [
            component_spec
            for component_spec in component_specs_to_delete
            if component_spec.component_type != schemas.ComponentType.RUN
        ]

        for run_spec_to_create in run_specs_to_create:
            try:
                await self.create_component_spec(
                    component_spec=run_spec_to_create,
                    exec_env_spec_id=env_spec_name_to_id[run_spec_to_create.environment]
                    if run_spec_to_create.environment
                    else None,
                )
            except Exception as e:
                raise SlingshotException(f"Failed to create: {e}") from e

        for other_app_to_create in remaining_apps_to_create:
            try:
                # Note: if we're creating a Label Studio app, we need to fetch the import and export run ids first
                #  If/when we generalize Apps to own Runs, we should refactor this (or if this starts to get too messy)
                import_run_spec = None
                export_run_spec = None
                if isinstance(other_app_to_create, schemas.LabelStudioComponentSpec):
                    import_run_spec = await self._sdk.get_app(other_app_to_create.import_run)
                    export_run_spec = await self._sdk.get_app(other_app_to_create.export_run)
                    assert import_run_spec, f"Import run '{other_app_to_create.import_run}' does not exist"
                    assert export_run_spec, f"Export run '{other_app_to_create.export_run}' does not exist"
                env_name = getattr(other_app_to_create, "environment", None)
                env_spec_id = env_spec_name_to_id[env_name] if env_name else None
                _ = await self.create_component_spec(
                    component_spec=other_app_to_create,
                    exec_env_spec_id=env_spec_id,
                    import_run_spec=import_run_spec,
                    export_run_spec=export_run_spec,
                )
            except Exception as e:
                raise SlingshotException(f"Failed to create app: {e}") from e

        for app_to_update, app_to_update_id in component_specs_to_update:
            try:
                env_name = getattr(app_to_update, "environment", None)
                env_spec_id = env_spec_name_to_id[env_name] if env_name else None
                await self.update_component_spec(
                    component_spec=app_to_update,
                    existing_component_spec_id=app_to_update_id,
                    exec_env_spec_id=env_spec_id,
                )
            except Exception as e:
                raise SlingshotException(f"Failed to update app: {e}") from e
        for other_app_to_delete in remaining_apps_to_delete:
            try:
                await self.delete_component_spec(other_app_to_delete)
            except Exception as e:
                raise SlingshotException(f"Failed to delete: {e}") from e
        for spec in run_specs_to_delete:
            try:
                await self.delete_component_spec(spec)
            except Exception as e:
                raise SlingshotException(f"Failed to delete: {e}") from e

    async def create_component_spec(
        self,
        component_spec: schemas.AbstractComponentSpec,
        exec_env_spec_id: str | None = None,
        import_run_spec: schemas.HasComponentSpecId | None = None,
        export_run_spec: schemas.HasComponentSpecId | None = None,
    ) -> schemas.HasComponentSpecId:
        console.print(f"Creating '{component_spec.name}'...", end="")
        component_type = _get_component_type(component_spec)
        app_sub_type = _get_app_sub_type(component_spec)
        machine_size = machine_type_gpu_count_to_machine_size(component_spec.machine_type, component_spec.num_gpu)
        component_spec_id_response = await self._sdk.create_app(
            name=component_spec.name,
            command=component_spec.cmd if hasattr(component_spec, "cmd") else None,
            component_type=component_type,
            app_sub_type=app_sub_type,
            exec_env_spec_id=exec_env_spec_id,
            machine_size=machine_size,
            mounts=component_spec.mounts,
            attach_project_credentials=(
                component_spec.attach_project_credentials
                if hasattr(component_spec, "attach_project_credentials")
                else False
            ),
            config_variables=component_spec.config_variables,
            app_port=component_spec.port if hasattr(component_spec, "port") else None,
            import_run_spec_id=import_run_spec.spec_id if import_run_spec else None,
            export_run_spec_id=export_run_spec.spec_id if export_run_spec else None,
        )
        spec_id = get_data_or_raise(component_spec_id_response)
        console.print("✅")
        return spec_id

    async def update_component_spec(
        self,
        component_spec: schemas.AbstractComponentSpec,
        existing_component_spec_id: str,
        exec_env_spec_id: str | None = None,
        import_run_spec: schemas.HasComponentSpecId | None = None,
        export_run_spec: schemas.HasComponentSpecId | None = None,
    ) -> None:
        component_type = _get_component_type(component_spec)
        app_sub_type = _get_app_sub_type(component_spec)
        spec_display_name = _get_spec_display_name(component_type, app_sub_type)
        console.print(f"Updating {spec_display_name} '{component_spec.name}'...", end="")
        machine_size = machine_type_gpu_count_to_machine_size(component_spec.machine_type, component_spec.num_gpu)
        await self._sdk.update_app(
            spec_id=existing_component_spec_id,
            command=component_spec.cmd if hasattr(component_spec, "cmd") else None,
            env_spec_id=exec_env_spec_id,
            machine_size=machine_size,
            config_variables=component_spec.config_variables,
            mounts=component_spec.mounts,
            attach_project_credentials=(
                component_spec.attach_project_credentials
                if hasattr(component_spec, "attach_project_credentials")
                else False
            ),
            app_port=component_spec.port if hasattr(component_spec, "port") else None,
            batch_size=component_spec.batch_size if hasattr(component_spec, "batch_size") else None,
            batch_interval=component_spec.batch_interval if hasattr(component_spec, "batch_interval") else None,
            import_run_spec_id=import_run_spec.spec_id if import_run_spec else None,
            export_run_spec_id=export_run_spec.spec_id if export_run_spec else None,
        )
        console.print("✅ ")

    async def delete_component_spec(self, component_spec: fragments.ComponentSpec) -> None:
        console.print(
            f"Deleting {component_spec.friendly_component_type} '{component_spec.spec_name}' from the remote project manifest...",
            end="",
        )
        await self._sdk.delete_app(spec_id=component_spec.spec_id)
        console.print("✅ ")

    async def apply_changes_to_remote(self, env_spec_plan: EnvSpecPlan, component_spec_plan: ComponentSpecPlan) -> None:
        """
        Applies all environments and app specs in the given plans by updating the remote.
        """
        console.print(f"Applying 'slingshot.yaml' for project '{self._project.project_id}'.")
        env_spec_name_to_id = await self.apply_env_specs(env_spec_plan=env_spec_plan)
        await self.apply_component_specs(
            component_spec_plan=component_spec_plan, env_spec_name_to_id=env_spec_name_to_id
        )
        _update_last_pushed_manifest(load_slingshot_project_config())

    async def check_conflicts_pull_remote_changes(self, force: bool = False) -> bool:
        """
        Pulls the remote manifest to the local slingshot.yaml.

        The last pushed manifest is used as the base of the initial diff. If there is no last-pushed manifest,
        the base is an empty manifest so that all remote changes are computed in the diff and can be pulled.
        Then, the local slingshot.yaml applied using the resulting diff. If there are conflicts, the user is
        prompted to override either the local or remote changes.

        Returns True if there were changes pulled, False otherwise.
        """
        # Step 1. Load all manifests (local, last_pushed, remote)
        local_manifest = _load_local_manifest(create_empty=True)
        remote_manifest = await _safe_load_remote_project_manifest(self._sdk, raise_on_error=not force)

        last_pushed_manifest: ProjectManifest | None
        if force:
            last_pushed_manifest = ProjectManifest()  # Force pull from remote into an empty manifest
        else:
            last_pushed_manifest = _load_last_pushed_manifest()

        # If the last pushed manifest is None, the user hasn't used the CLI from this directory before, so we are
        # unsure about what the source of truth should be for pulling.
        if last_pushed_manifest is None:
            should_pull, last_pushed_manifest = await _maybe_set_last_pushed_manifest(local_manifest, remote_manifest)
            if not should_pull:
                return False

        # Step 2. Compute diff between the last pushed and remote, and the last pushed and local
        remote_diff = compute_project_manifest_diff(last_pushed_manifest, remote_manifest)
        local_diff = compute_project_manifest_diff(last_pushed_manifest, local_manifest)
        if not remote_diff:
            logger.debug("No remote changes detected")
            return False

        # Step 3. Check for conflicts between the remote and local relative to the last pushed manifest
        if not force and detect_local_remote_diff_conflicts(local_diff=local_diff, remote_diff=remote_diff):
            console.print("[red]Conflict detected[/red]")
            return await _handle_conflict(
                local_diff=local_diff, remote_diff=remote_diff, remote_manifest=remote_manifest, force=force
            )

        # Step 4. Pull any changes from the remote into the local manifest
        console.print("Changes found on the remote since your last push:")
        console.print(diff_to_str(remote_diff))
        try:
            apply_diff_to_local_manifest(remote_diff, remote_manifest, force=force)
            _update_last_pushed_manifest(load_slingshot_project_config())
            console.print("[green]Changes pulled to your local 'slingshot.yaml'[/green]")
            return True
        except Exception as e:
            sentry_sdk.capture_exception(e)
            console.print("[red]An error occurred while pulling[/red]")
            console.print("Changes found on the local copy since your last push:")
            console.print(diff_to_str(local_diff))
            return await _prompt_override_local_remote(diff=remote_diff, remote_manifest=remote_manifest, force=force)

    async def apply(self, *, force: bool) -> bool:
        """
        Detects conflicts, pulls, and then applies local changes to the remote.

        Returns if any changes were applied or pulled.
        """
        # 1. Check for conflicts between the remote and local manifests and pull changes from the remote
        any_changes_pulled = False
        if not force:
            any_changes_pulled = await self.check_conflicts_pull_remote_changes()

        # 2. Plan and apply changes from local to the remote
        # Reload local, in case it was changed
        local_manifest = load_slingshot_project_config(force_reload=True, silence_warnings=True)
        env_spec_plan, component_spec_plan = await self.plan(config_=local_manifest)
        if any(env_spec_plan) or any(component_spec_plan):
            if force or prompt_confirm("Do you want to apply these changes?", default=True):
                await self.apply_changes_to_remote(env_spec_plan=env_spec_plan, component_spec_plan=component_spec_plan)
                await self.restart_updated_apps(env_spec_plan=env_spec_plan, component_spec_plan=component_spec_plan)
                return True
            return any_changes_pulled

        # Make sure the last pushed manifest is at parity with the local manifest if there were no plan changes
        _update_last_pushed_manifest(load_slingshot_project_config())
        return any_changes_pulled

    async def restart_updated_apps(self, env_spec_plan: EnvSpecPlan, component_spec_plan: ComponentSpecPlan) -> None:
        _, component_specs_to_update, _ = component_spec_plan

        # We only want to restart deployments and custom apps
        apps_or_deployments_to_restart = [
            (component_spec, component_type)
            for component_spec, _ in component_specs_to_update
            if (component_type := _get_component_type(component_spec))
            in {schemas.ComponentType.DEPLOYMENT, schemas.ComponentType.APP}
        ]
        # TODO: also restart apps and deployments if their envs changed

        for component_spec, component_type in apps_or_deployments_to_restart:
            match component_type:
                case schemas.ComponentType.DEPLOYMENT:
                    deployment_spec = await self._sdk.get_deployment(deployment_name=component_spec.name)
                    deployment_is_active = (
                        deployment_spec
                        and deployment_spec.deployment_status
                        and deployment_spec.deployment_status.is_active
                    )
                    if not deployment_is_active:
                        continue
                    if prompt_confirm(f"Do you want to restart deployment '{component_spec.name}'?", default=False):
                        console.print("Restarting deployment...", end="")
                        await self._sdk.start_deployment(deployment_name=component_spec.name)
                        console.print("✅")

                case schemas.ComponentType.APP:
                    app_spec = await self._sdk.get_app(app_name=component_spec.name)
                    app_is_active = app_spec and app_spec.app_instance_status and app_spec.app_instance_status.is_active
                    if not app_is_active:
                        continue
                    if prompt_confirm(f"Do you want to restart app '{component_spec.name}'?", default=False):
                        console.print("Restarting app...", end="")
                        await self._sdk.start_app(app_name=component_spec.name)
                        console.print("✅")


async def _maybe_set_last_pushed_manifest(
    local_manifest: ProjectManifest, remote_manifest: ProjectManifest
) -> tuple[bool, ProjectManifest]:
    """
    Sets the last pushed manifest to either the local or remote manifest and returns a tuple indicating if
    we should continue pulling remote changes, and the last pushed manifest.
    """
    empty_manifest = ProjectManifest()
    if remote_manifest == empty_manifest:  # If empty remote, assume local is ground truth to avoid pulling
        _update_last_pushed_manifest(empty_manifest)
        return False, empty_manifest

    # Diff local and remote to see if there are any changes between local and remote
    local_remote_diff = compute_project_manifest_diff(local_manifest, remote_manifest)
    if not local_remote_diff:  # If no diff, we can just set local to ground truth as the last pushed manifest
        _update_last_pushed_manifest(local_manifest)
        return False, local_manifest

    # Otherwise, prompt the user to choose which manifest is the source of truth and pull from that
    last_pushed_manifest = await _prompt_set_last_pushed_manifest(
        local_manifest=local_manifest, remote_manifest=remote_manifest
    )
    return True, last_pushed_manifest


async def _prompt_set_last_pushed_manifest(
    local_manifest: ProjectManifest, remote_manifest: ProjectManifest
) -> ProjectManifest:
    """
    Prompts the user to set the last pushed manifest to either the local or remote manifest.
    """
    prompt_result = prompt_for_single_choice(
        "Detected difference between local and remote, choose one as your source of truth:", ["local", "remote"]
    )
    if prompt_result == 0:
        _update_last_pushed_manifest(local_manifest)
    else:
        _update_last_pushed_manifest(remote_manifest)
    new_last_pushed_manifest = _load_last_pushed_manifest()
    assert new_last_pushed_manifest, "Failed to set last pushed manifest"
    return new_last_pushed_manifest


async def _prompt_override_local_remote(
    diff: list[DiffItem], remote_manifest: schemas.ProjectManifest, *, force: bool
) -> bool:
    """Overwrites the local manifest with the applied diff. Returns if changes were applied."""
    console.print("[yellow]Unable to sync remote changes with your local 'slingshot.yaml'[/yellow]")
    if not force:
        prompt_result = prompt_for_single_choice(
            "Do you want to use the local or remote version?", ["local", "remote", "resolve manually"], default=0
        )
        if prompt_result == 0:
            _update_last_pushed_manifest(load_slingshot_project_config())
            console.print(
                "[bold]Ignored[/bold] the remote changes. To override the remote manifest with your local "
                "'slingshot.yaml', run 'slingshot apply -f'."
            )
            return False
        elif prompt_result == 2:
            with edit_slingshot_yaml(raise_if_absent=False, filename=".slingshot.remote.yaml") as slingshot_yaml:
                slingshot_yaml.clear()
                slingshot_yaml.update(remote_manifest.model_dump())

            console.print(
                "[bold]Manual resolution:[/bold] A copy of the remote slingshot manifest has been saved to "
                "'.slingshot.remote.yaml'. Please resolve the conflicts manually in 'slingshot.yaml' and then "
                "force-apply your local resolution with 'slingshot apply -f'."
            )
            return False

    # If force pull or the user chose to use the remote for conflict resolution, apply remote diff to local manifest
    apply_diff_to_local_manifest(diff, reference_manifest=remote_manifest, force=True)
    _update_last_pushed_manifest(load_slingshot_project_config())
    return True


def _get_component_type(spec: schemas.AbstractComponentSpec) -> schemas.ComponentType:
    if isinstance(spec, schemas.RunSpec):
        return schemas.ComponentType.RUN
    elif isinstance(spec, schemas.DeploymentSpec):
        return schemas.ComponentType.DEPLOYMENT
    else:
        return schemas.ComponentType.APP


def _get_app_sub_type(spec: schemas.AbstractComponentSpec) -> schemas.AppSubType | None:
    if isinstance(spec, schemas.WebappComponentSpec):
        return schemas.AppSubType.WEBAPP
    if isinstance(spec, schemas.SessionComponentSpec):
        return schemas.AppSubType.SESSION
    if isinstance(spec, schemas.RedisComponentSpec):
        return schemas.AppSubType.REDIS
    if isinstance(spec, schemas.LabelStudioComponentSpec):
        return schemas.AppSubType.LABEL_STUDIO
    return None


def _diff_existing_env_yaml_specs(
    existing_env_specs: list[fragments.ExecutionEnvironmentSpec], yaml_env_specs: dict[str, schemas.EnvironmentSpec]
) -> tuple[
    list[tuple[schemas.EnvironmentSpec, str]],  # tuple of spec, name
    list[tuple[schemas.EnvironmentSpec, fragments.ExecutionEnvironmentSpec]],  # tuple of spec, existing spec to update
    list[fragments.ExecutionEnvironmentSpec],  # existing specs to delete
    set[str],  # updated spec names
    list[str],  # change messages
]:
    env_specs_to_create: list[tuple[schemas.EnvironmentSpec, str]] = []
    env_specs_to_update: list[tuple[schemas.EnvironmentSpec, fragments.ExecutionEnvironmentSpec]] = []
    env_specs_to_delete: list[fragments.ExecutionEnvironmentSpec] = []

    existing_env_names = {spec.execution_environment_spec_name for spec in existing_env_specs}
    existing_env_name_to_spec = {spec.execution_environment_spec_name: spec for spec in existing_env_specs}
    yaml_env_names = {spec_name for spec_name in yaml_env_specs.keys()}

    updated_spec_names: set[str] = set()
    change_msgs: list[str] = []
    for spec_name, env_spec in yaml_env_specs.items():
        if spec_name not in existing_env_names:
            change_msgs.append(f"[green](+)[/green] environment '{spec_name}'")
            env_specs_to_create.append((env_spec, spec_name))
            continue

        _change_msgs: list[str] = []
        existing_env_spec = existing_env_name_to_spec[spec_name]
        if diff := env_spec.diff(existing_env_spec):
            _change_msgs.extend(f"\t- {i}" for i in diff)
        if _change_msgs:
            change_msgs.append(f"Detected [yellow]changes[/yellow] to environment '{spec_name}'")
            change_msgs.extend(_change_msgs)
            updated_spec_names.add(spec_name)
            env_specs_to_update.append((env_spec, existing_env_spec))

    for existing_spec in existing_env_specs:
        if existing_spec.execution_environment_spec_name not in yaml_env_names:
            logger.debug(
                f"Detected environment '{existing_spec.execution_environment_spec_name}' has been [red]deleted[/red]"
            )
            logger.debug(f"\t- Environment will be [red]deleted[/red]")
            env_specs_to_delete.append(existing_spec)

    return env_specs_to_create, env_specs_to_update, env_specs_to_delete, updated_spec_names, change_msgs


def _diff_existing_app_yaml_specs(
    all_existing_component_specs: list[fragments.ComponentSpec],
    yaml_component_specs: typing.Sequence[schemas.AbstractComponentSpec],
    component_type: schemas.ComponentType,
    app_sub_type: schemas.AppSubType | None = None,
) -> tuple[
    list[schemas.AbstractComponentSpec],
    list[tuple[schemas.AbstractComponentSpec, str]],
    list[fragments.ComponentSpec],
    list[str],
]:
    spec_display_name = _get_spec_display_name(component_type, app_sub_type)
    component_specs_to_create: list[schemas.AbstractComponentSpec] = []
    component_specs_to_update: list[tuple[schemas.AbstractComponentSpec, str]] = []
    component_specs_to_delete: list[fragments.ComponentSpec] = []

    existing_component_specs = [spec for spec in all_existing_component_specs if spec.component_type == component_type]
    existing_spec_name_to_spec: dict[str, fragments.ComponentSpec] = {
        component_spec.spec_name: component_spec for component_spec in existing_component_specs
    }
    yaml_component_spec_names = {component_spec.name for component_spec in yaml_component_specs}

    change_msgs: list[str] = []
    for component_spec in yaml_component_specs:
        if component_spec.name not in existing_spec_name_to_spec:
            change_msgs.append(f"[green](+)[/green] {spec_display_name} '{component_spec.name}'")
            component_specs_to_create.append(component_spec)
            continue

        existing_component_spec = existing_spec_name_to_spec[component_spec.name]
        _change_msgs: list[str] = []
        if component_spec_diff := component_spec.diff(existing_component_spec):
            _change_msgs.extend(f"\t- {i}" for i in component_spec_diff)
        if _change_msgs:
            change_msgs.append(f"[yellow]Changes[/yellow] to {spec_display_name} '{component_spec.name}'")
            change_msgs.extend(_change_msgs)

        # Only update if there are changes to the component spec itself, not just the environment
        if len(component_spec_diff) > 0:
            component_specs_to_update.append((component_spec, existing_component_spec.spec_id))

    for existing_component_spec in existing_component_specs:
        if existing_component_spec.spec_name not in yaml_component_spec_names and (
            _normalize_app_sub_type(existing_component_spec) == app_sub_type
        ):
            console.print(f"[red](-)[/red] {spec_display_name} '{existing_component_spec.spec_name}'")
            component_specs_to_delete.append(existing_component_spec)

    return component_specs_to_create, component_specs_to_update, component_specs_to_delete, change_msgs


def _normalize_app_sub_type(app: fragments.ComponentSpec) -> Optional[schemas.AppSubType]:
    """
    Ensures that an app always has an app sub type type. Prior to Aug 2023, apps without a
    'using' configured (without a sub type) were treated by default as web apps.
    """
    if app.component_type == schemas.ComponentType.APP and app.app_sub_type is None:
        return schemas.AppSubType.WEBAPP
    return app.app_sub_type


async def _safe_load_remote_project_manifest(sdk: "SlingshotSDK", raise_on_error: bool) -> schemas.ProjectManifest:
    try:
        return await _remote_project_manifest(sdk)
    # TODO: wrap ValidationError that we throw as a subtype of a SlingshotException?
    except (SlingshotException, ValidationError) as e:
        error_msg = e.cli if isinstance(e, SlingshotException) else str(e)
        if raise_on_error:
            raise SlingshotException(
                f"Error reading the remote slingshot manifest: {error_msg}\n"
                f"Try force applying with `slingshot apply -f`, or contact Slingshot support if this issue persists."
            )
        console.print(f"[yellow]Warning[/yellow]: {error_msg}")
        return ProjectManifest()  # Return an empty manifest if we failed to load and don't want to raise


async def _remote_project_manifest(sdk: "SlingshotSDK") -> schemas.ProjectManifest:
    # Build environment specs
    existing_env_specs = await sdk.list_environments()
    env_specs_by_name = {}
    for env_spec in existing_env_specs:
        assert env_spec.environment_instances, "Environment spec has no instances"
        env_instance = env_spec.environment_instances[0]
        parsed_env_spec = schemas.EnvironmentSpec(
            python_packages=[
                str(schemas.RequestedRequirement.model_validate(i)) for i in env_instance.requested_python_requirements
            ],
            apt_packages=[
                schemas.RequestedAptPackage.model_validate(i).name for i in env_instance.requested_apt_packages
            ],
            post_install_command=env_instance.post_install_command,
        )
        env_specs_by_name[env_spec.execution_environment_spec_name] = parsed_env_spec

    # Build app specs
    component_specs: list[schemas.AbstractComponentSpec] = []
    existing_component_specs = await sdk.list_components()
    for spec in existing_component_specs:
        name = spec.spec_name
        existing_env_spec = spec.execution_environment_spec
        environment = existing_env_spec.execution_environment_spec_name if existing_env_spec else None
        config_variables = json.loads(spec.config_variables) if spec.config_variables else {}
        port = spec.app_port
        attach_project_credentials = spec.service_account
        cmd = spec.command
        machine_type, num_gpu = machine_size_to_machine_type_gpu_count(spec.machine_size)
        mounts = [schemas.remote_mount_spec_to_local(ms) for ms in spec.mount_specs]
        if spec.component_type == schemas.ComponentType.APP and (
            spec.app_sub_type is None or spec.app_sub_type == schemas.AppSubType.WEBAPP
        ):
            assert environment, f"Custom app '{name}' has no environment"
            assert cmd, f"Custom app '{name}' has no command"
            component_specs.append(
                schemas.WebappComponentSpec(
                    name=name,
                    environment=environment,
                    machine_type=machine_type,
                    num_gpu=num_gpu,
                    config_variables=config_variables,
                    port=port,
                    attach_project_credentials=attach_project_credentials,
                    cmd=cmd,
                    using="webapp",
                    mounts=mounts,
                )
            )
        elif spec.component_type == schemas.ComponentType.APP and spec.app_sub_type == schemas.AppSubType.SESSION:
            assert environment, f"Session app '{name}' has no environment"
            component_specs.append(
                schemas.SessionComponentSpec(
                    name=name,
                    environment=environment,
                    machine_type=machine_type,
                    num_gpu=num_gpu,
                    config_variables=config_variables,
                    attach_project_credentials=attach_project_credentials,
                    using="session",
                    mounts=mounts,
                )
            )
        elif spec.component_type == schemas.ComponentType.APP and spec.app_sub_type == schemas.AppSubType.REDIS:
            component_specs.append(
                schemas.RedisComponentSpec(name=name, machine_type=machine_type, num_gpu=num_gpu, using="redis")
            )
        elif spec.component_type == schemas.ComponentType.APP and spec.app_sub_type == schemas.AppSubType.LABEL_STUDIO:
            component_specs.append(
                schemas.LabelStudioComponentSpec(
                    name=name, machine_type=machine_type, num_gpu=num_gpu, using="label-studio"
                )
            )
        elif spec.component_type == schemas.ComponentType.RUN:
            assert environment, f"Run app '{name}' has no environment"
            assert cmd, f"Run app '{name}' has no command"
            component_specs.append(
                schemas.RunSpec(
                    name=name,
                    environment=environment,
                    machine_type=machine_type,
                    num_gpu=num_gpu,
                    config_variables=config_variables,
                    attach_project_credentials=attach_project_credentials,
                    cmd=cmd,
                    mounts=mounts,
                )
            )
        elif spec.component_type == schemas.ComponentType.DEPLOYMENT:
            assert environment, f"Deployment '{name}' has no environment"
            assert cmd, f"Deployment '{name}' has no command"
            component_specs.append(
                schemas.DeploymentSpec(
                    name=name,
                    environment=environment,
                    machine_type=machine_type,
                    num_gpu=num_gpu,
                    config_variables=config_variables,
                    attach_project_credentials=attach_project_credentials,
                    cmd=cmd,
                    mounts=mounts,
                )
            )
        else:
            raise ValueError(f"Unknown component type {spec.component_type}")

    return schemas.ProjectManifest(
        environments=env_specs_by_name,
        apps=[
            app
            for app in component_specs
            if isinstance(
                app,
                (
                    schemas.WebappComponentSpec,
                    schemas.SessionComponentSpec,
                    schemas.RedisComponentSpec,
                    schemas.LabelStudioComponentSpec,
                ),
            )
        ],
        runs=[app for app in component_specs if isinstance(app, schemas.RunSpec)],
        deployments=[app for app in component_specs if isinstance(app, schemas.DeploymentSpec)],
    )


async def _handle_conflict(
    local_diff: list[DiffItem], remote_diff: list[DiffItem], remote_manifest: schemas.ProjectManifest, force: bool
) -> bool:
    console.print("Changes found on the remote since your last push:")
    console.print(diff_to_str(remote_diff))
    console.print("Changes found on the local copy since your last push:")
    console.print(diff_to_str(local_diff))
    return await _prompt_override_local_remote(diff=remote_diff, remote_manifest=remote_manifest, force=force)


def _load_local_manifest(create_empty: bool) -> schemas.ProjectManifest:
    """Load the current local manifest, or create an empty one if it doesn't exist."""
    if create_empty:
        try:
            current_manifest = load_slingshot_project_config()  # Reload local, in case it was changed
        except SlingshotFileNotFoundException:
            create_empty_project_manifest(client_settings.slingshot_config_path)
            current_manifest = load_slingshot_project_config()  # Reload local, which is now an empty manifest.
    else:
        current_manifest = load_slingshot_project_config()
    return current_manifest


def _migrate_last_pushed_manifest(manifest: dict[str, typing.Any]) -> dict[str, typing.Any]:
    """
    Apply corrections to the cached manifest before validating. This attempts to correct for breaking changes to the
    schema that would cause the existing files from .slingshot to not load cleanly causing crashes.
    """
    if 'apps' in manifest and isinstance(manifest['apps'], list):
        for app in manifest['apps']:
            if 'using' not in app:
                # We used to treat apps without 'using' as custom/web apps, this is now set explicitly
                app['using'] = 'webapp'
            else:
                # Label studio and redis used to require an explicit environment, this is now controlled by the template
                if app['using'] in ['label-studio', 'redis'] and 'environment' in app:
                    del app['environment']
    return manifest


def _update_last_pushed_manifest(manifest: ProjectManifest) -> None:
    """Update the cached last pushed manifest with the given manifest."""
    # NOTE: We need to exclude "local only" sections here to avoid them showing up as spurious diffs
    config.project_config.last_pushed_manifest = manifest.model_dump(exclude_local_only=True)


def _load_last_pushed_manifest() -> schemas.ProjectManifest | None:
    """Load the last pushed manifest, and return if the last pushed manifest is empty."""
    last_pushed_manifest_dict = config.project_config.last_pushed_manifest

    # First make sure this is a valid project manifest
    if last_pushed_manifest_dict:
        last_pushed_manifest_dict = _migrate_last_pushed_manifest(last_pushed_manifest_dict)
        try:
            return ProjectManifest.model_validate(last_pushed_manifest_dict)
        except ValidationError as e:
            # TODO: if this fails, this is most likely due to a breaking change in the schema. We should attempt to
            #  migrate the manifest to the new schema, and if that fails, we should let the user choose to override
            #  the remote manifest.
            return None
    else:
        return None


def _get_spec_display_name(component_type: schemas.ComponentType, app_sub_type: schemas.AppSubType | None) -> str:
    """Return the display name for the component type and sub type."""
    match component_type:
        case schemas.ComponentType.APP:
            match app_sub_type:
                case schemas.AppSubType.WEBAPP:
                    return "web app"
                case schemas.AppSubType.SESSION:
                    return "session"
                case schemas.AppSubType.REDIS:
                    return "redis"
                case schemas.AppSubType.LABEL_STUDIO:
                    return "label studio"
                case _:
                    return "app"
        case schemas.ComponentType.RUN:
            return "run"
        case schemas.ComponentType.DEPLOYMENT:
            return "deployment"
        case _:
            raise ValueError(f"Unknown component type {component_type}")
