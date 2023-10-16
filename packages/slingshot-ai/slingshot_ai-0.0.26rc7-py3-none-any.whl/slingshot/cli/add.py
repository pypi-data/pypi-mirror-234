from __future__ import annotations

import re
import shutil
import typing
import uuid
from pathlib import Path
from typing import Literal, Optional, cast

import typer
from pydantic import ValidationError

from slingshot.cli.config.slingshot_cli import SlingshotCLIApp
from slingshot.cli.shared import create_empty_project_manifest, prompt_confirm, prompt_for_single_choice
from slingshot.schemas import slingshot_schema as slingshot_yaml_schemas
from slingshot.sdk import SlingshotSDK
from slingshot.sdk.config import client_settings
from slingshot.sdk.utils import console, edit_slingshot_yaml

from .. import schemas
from ..sdk.errors import SlingshotException
from ..shared.config import load_slingshot_project_config
from ..shared.utils import pydantic_to_dict
from .project import list_and_set_project_id

app = SlingshotCLIApp()

OPTIONS = ["run", "deployment", "app", "environment", "label-studio", "session"]


def _display_name_to_id(input_str: str) -> str:
    """Converts a name to a valid project ID by removing special characters and replacing spaces with hyphens."""
    lower = input_str.strip().lower()
    single_space = re.sub(r"\s+", "-", lower)
    single_hyphen = re.sub(r"-+", "-", single_space)
    alphanumeric_hyphen_underscore = re.sub(r"[^a-z0-9-_]", "", single_hyphen)
    return alphanumeric_hyphen_underscore


def _short_unique_id() -> str:
    return uuid.uuid4().hex[:4]


async def _create_project(sdk: SlingshotSDK) -> str:
    new_id = None
    display_name = typer.prompt("Enter a name for your project")

    # Use the display name to generate a project ID and append UUID if it's not available
    project_id_default = _display_name_to_id(display_name)
    if not await sdk._api.project_id_available(project_id_default):
        project_id_default = f"{project_id_default}-{_short_unique_id()}"

    while True:
        # Replace multiple spaces with a single space and spaces with hyphens
        new_id = new_id or typer.prompt(
            "Enter a slug for your project (unique ID used for URLs)", default=project_id_default
        )
        try:
            project_response = await sdk.create_project(new_id, display_name=display_name)
            if project_response.error:
                console.print(f"[red]Error creating project[/red]: {project_response.error.message}")
                display_name = None
                new_id = None
                continue

            assert project_response.data is not None
            assert project_response.data.project_id
            console.print(f"Created project: {new_id}")
            await sdk.use_project(project_response.data.project_id)
            return project_response.data.project_id
        except ValidationError as e:
            for error in e.errors():
                loc = error["loc"]
                if loc[0] == "project_id":
                    console.print(f"[red]Project slug is invalid[/red]: {error['msg']}")
                    new_id = None
                if loc[0] == "project_display_name":
                    console.print(f"[red]Project name is invalid[/red]: {error['msg']}")
                    display_name = None


@app.command(requires_auth=False, requires_project=False, top_level=True, name="init")
async def init(*, sdk: SlingshotSDK) -> None:
    """Initialize a new project in the current directory"""
    has_project = bool(sdk.project_id)
    has_slingshot_yaml = (
        client_settings.slingshot_config_path.exists() and client_settings.slingshot_config_path.stat().st_size > 0
    )
    options = ["Create new project", "Select existing project"]

    if not has_project and not has_slingshot_yaml:
        create_or_choose_project = prompt_for_single_choice(
            "Create a new project or select an existing project?", options
        )
        if create_or_choose_project == 0:  # Create new project
            await _create_project(sdk)
            create_empty_project_manifest(client_settings.slingshot_config_path)
            await prompt_add_component(sdk)
            await sdk.apply_project()
        else:  # Select existing project
            await list_and_set_project_id(sdk)
            await sdk.pull_remote_changes()  # No YAML so we can just pull anything that exists on the remote
    if not has_project and has_slingshot_yaml:
        console.print(
            f"[yellow]slingshot.yaml[/yellow] detected, but no project is currently being tracked ({client_settings.slingshot_config_path})."
        )
        create_or_choose_project = prompt_for_single_choice(
            f"Create a new project (at {client_settings.slingshot_config_path}) or select an existing project?", options
        )
        if create_or_choose_project == 0:  # Create new project
            await _create_project(sdk)
        else:  # Select existing project
            await list_and_set_project_id(sdk)
        await sdk.apply_project()
    if has_project and not has_slingshot_yaml:
        console.print(f"Project '{sdk.project_id}' is already tracked.")
        if prompt_confirm("Do you want to pull any remote changes?", default=True):
            # TODO: Shouldn't the SDK already be setup at this point?
            assert sdk.project_id  # Always safe as has_project depends on it
            await sdk.use_project(sdk.project_id)
            await sdk.pull_remote_changes(force=True)  # No YAML so we can just pull anything that exists on the remote
    if has_project and has_slingshot_yaml:
        console.print(
            f"Project '{sdk.project_id}' already initialized. You may modify it by editing the 'slingshot.yaml' or track another project with 'slingshot use'."
        )
        if prompt_confirm("Do you want to create a new project on Slingshot?", default=False):
            await _create_project(sdk)
        await sdk.apply_project()


async def prompt_add_component(sdk: SlingshotSDK) -> None:
    first = True
    while True:
        prompt = "Do you want to add another component?" if not first else "Do you want to add a component?"
        if not prompt_confirm(prompt, default=False):
            break
        await add_component.function(sdk=sdk, component=None)
        first = False


@app.command(requires_auth=False, requires_project=False, top_level=True, name="add")
async def add_component(
    *,
    sdk: SlingshotSDK,
    component: Optional[str] = typer.Argument(
        None, help="The component to add. One of " + ", ".join(OPTIONS), show_default=False
    ),
) -> None:
    """
    Add a component (run, deployment, app, environment) to the project.
    """
    # The intent of this command is to add a valid component (app, session, etc) to the slingshot.yaml, but with the
    # expectation that the user will edit the file to provide the specific name, command, etc to be used. As such we
    # don't offer to apply the new configuration - applying it would apply something that isn't yet ready.
    # As the goal is the keep the slingshot.yaml in a valid state at all times (if nothing else, so that the user can
    # add multiple things, one run, one session, etc), we do need to specify a valid environment for each component.
    # The logic here is that we create an environment for each category, runs, sessions, apps, etc if they do not
    # already exist. The environments that are created will contain "must have" packages where applicable, e.g.
    # jupyter for sessions and slingshot for deployments, but will otherwise not try to anticipate the user's needs.

    # Load config before anything else to force errors early if current file isn't valid
    load_slingshot_project_config()

    if component is None:
        component_i = prompt_for_single_choice("What component do you want to add?", OPTIONS)
        component = OPTIONS[component_i]
    if component not in OPTIONS:
        raise typer.BadParameter(f"Invalid component: {component}. Must be one of " + ", ".join(OPTIONS))

    if component == "environment":
        _create_new_environment()
    elif component == "label-studio":
        _create_label_studio()
    else:
        component = cast(Literal["run", "deployment", "app", "session"], component)
        _create_app_spec(component)


def _print_template_added_message(type_: str, name: str) -> None:
    console.print(
        f"Template {type_} '{name}' added to your 'slingshot.yaml'.\n\n"
        f"To edit your {type_} parameters, edit the 'slingshot.yaml' in your IDE or "
        f"'Start {type_.capitalize()}' on app.slingshot.xyz."
    )


def _create_new_environment() -> None:
    name = f"env-{_short_unique_id()}"
    env = schemas.EnvironmentSpec(python_packages=[])
    with edit_slingshot_yaml() as current_config:
        if "environments" not in current_config:
            current_config["environments"] = {}
        current_config["environments"][name] = pydantic_to_dict(env)

    _print_template_added_message("environment", name)


def _create_label_studio() -> None:
    app_name = f"label-studio-{_short_unique_id()}"
    ls_app = schemas.LabelStudioComponentSpec(
        name=app_name,
        using="label-studio",
        machine_type=schemas.MachineType.CPU_SMALL,
        # TODO: include a volume so we automatically can persist data across app restarts
    )

    ls_runs_env = schemas.LabelStudioComponentSpec.get_default_run_environment()
    with edit_slingshot_yaml() as current_config:
        _insert_env_if_not_exists(
            env_name="label-studio-run-env", python_packages=ls_runs_env.python_packages, current_config=current_config
        )
        import_run = schemas.LabelStudioComponentSpec.get_default_import_run()
        export_run = schemas.LabelStudioComponentSpec.get_default_export_run()

        _add_component_to_config(ls_app, current_config)
        _add_component_to_config_if_not_exists(import_run, current_config)
        _add_component_to_config_if_not_exists(export_run, current_config)
        _print_template_added_message("app", ls_app.name)

    if prompt_confirm(
        "Label Studio requires auxiliary runs to import and export data. Do you want to use template code for these runs?",
        default=True,
    ):
        _copy_template_to_user_dir(
            "label_studio/label_studio_data_export_template.py", "label_studio/label_studio_export.py"
        )
        _copy_template_to_user_dir(
            "label_studio/label_studio_data_import_template.py", "label_studio/label_studio_import.py"
        )


def _component_to_config_key(component: schemas.AbstractComponentSpec) -> str:
    if isinstance(component, schemas.RunSpec):
        return "runs"
    elif isinstance(component, schemas.DeploymentSpec):
        return "deployments"
    else:
        return "apps"


def _component_to_display_name(component: schemas.AbstractComponentSpec) -> str:
    if isinstance(component, schemas.RunSpec):
        return "Run"
    elif isinstance(component, schemas.DeploymentSpec):
        return "Deployment"
    elif isinstance(component, schemas.SessionComponentSpec):
        return "Session"
    else:
        return "App"


def _add_component_to_config(component: schemas.AbstractComponentSpec, current_config: dict[str, typing.Any]) -> None:
    """Add a new app, run or deployment to the config being edited (current_config)"""
    config_key = _component_to_config_key(component)

    if not current_config.get(config_key):
        current_config[config_key] = []
    current_config[config_key].append(pydantic_to_dict(component))


def _add_component_to_config_if_not_exists(
    component: schemas.AbstractComponentSpec, current_config: dict[str, typing.Any]
) -> None:
    """Add a new app, run or deployment if it doesn't already exist"""
    config_key = _component_to_config_key(component)
    components_of_type = current_config[config_key] if config_key in current_config else []
    if any(existing_component["name"] == component.name for existing_component in components_of_type):
        console.print(
            f"{_component_to_display_name(component)} '{component.name}' already exists, skipping creation",
            style="yellow",
        )
    else:
        _add_component_to_config(component, current_config)
        console.print(f"{_component_to_display_name(component)} '{component.name}' added")


def _insert_env_if_not_exists(env_name: str, python_packages: list[str], current_config: dict[str, typing.Any]) -> None:
    if "environments" in current_config and env_name in current_config["environments"]:
        console.print(f"Environment '{env_name}' already exists, skipping creation", style="yellow")
    else:
        environment = slingshot_yaml_schemas.EnvironmentSpec(python_packages=python_packages)
        current_config["environments"][env_name] = pydantic_to_dict(environment)
        console.print(f"Environment '{env_name}' added", style="green")


def _create_app_spec(type_: Literal["run", "deployment", "app", "session"]) -> None:
    default_name_prefix = {"run": "run", "deployment": "deploy", "app": "app", "session": "session"}
    name = f"{default_name_prefix[type_]}-{_short_unique_id()}"

    if type_ == "deployment":
        with edit_slingshot_yaml() as current_config:
            _insert_env_if_not_exists("deployment-environment", ["slingshot-ai", "uvicorn", "fastapi"], current_config)
            _add_component_to_config(
                schemas.DeploymentSpec(
                    name=name,
                    environment="deployment-environment",
                    cmd="python deployment.py",
                    machine_type=schemas.MachineType.CPU_SMALL,
                    mounts=[
                        schemas.DownloadMountSpec(
                            path="/mnt/model", mode="DOWNLOAD", selector=schemas.MountSelector(name="model")
                        )
                    ],
                ),
                current_config,
            )

        if prompt_confirm("Do you want to use a template deployment script?", default=True):
            _copy_template_to_user_dir("deployment_template.py", "deployment.py")
    elif type_ == "run":
        with edit_slingshot_yaml() as current_config:
            _insert_env_if_not_exists("run-environment", [], current_config)
            _add_component_to_config(
                schemas.RunSpec(
                    name=name,
                    cmd="python train.py",
                    environment="run-environment",
                    machine_type=schemas.MachineType.CPU_SMALL,
                ),
                current_config,
            )
    elif type_ == "session":
        with edit_slingshot_yaml() as current_config:
            _insert_env_if_not_exists(
                "session-environment", ["jupyterlab>=4.0.0", "jupyter_collaboration"], current_config
            )

            _add_component_to_config(
                schemas.SessionComponentSpec(
                    name=name,
                    using="session",
                    environment="session-environment",
                    machine_type=schemas.MachineType.CPU_SMALL,
                ),
                current_config,
            )
    elif type_ == "app":
        with edit_slingshot_yaml() as current_config:
            _insert_env_if_not_exists("app-environment", [], current_config)
            _add_component_to_config(
                schemas.WebappComponentSpec(
                    name=name,
                    using="webapp",
                    cmd="python app.py",
                    environment="app-environment",
                    machine_type=schemas.MachineType.CPU_SMALL,
                    port=8080,
                ),
                current_config,
            )
    else:
        assert False, f"Invalid type: {type_}"

    _print_template_added_message(type_, name)


def _copy_template_to_user_dir(template_filename: str, target_filename: str) -> None:
    console.print(f"Copying a template to '{target_filename}'...")
    target_path = client_settings.slingshot_config_path.parent / target_filename
    if target_path.exists():
        if not prompt_confirm(f"File '{target_filename}' already exists. Overwrite?", default=False):
            console.print("Aborting", style="red")
            return  # No need to raise an exception, the user can just try again
    template_path = Path(__file__).parent.parent / "templates" / template_filename
    if not template_path.exists():
        raise SlingshotException(f"Template file {template_path} not found")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(template_path, target_path)
    console.print(f"Template copied to '{target_filename}'")
