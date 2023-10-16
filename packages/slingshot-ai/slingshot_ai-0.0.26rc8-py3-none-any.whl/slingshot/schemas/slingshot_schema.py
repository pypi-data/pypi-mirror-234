from __future__ import annotations

import json
import typing
from abc import ABC
from pathlib import Path, PurePath
from typing import Annotated, Any, Literal, Optional, Union

import deepdiff
from pydantic import BaseModel, ConfigDict, Field, RootModel, TypeAdapter, field_validator, model_validator
from pydantic_core.core_schema import FieldValidationInfo
from typing_extensions import override

from slingshot import schemas
from slingshot.schemas import RequestedRequirement
from slingshot.schemas.utils import has_path_ending_in_filename, requested_requirements_from_str
from slingshot.schemas.validation_warnings import SlingshotDeprecationWarning, record_validation_warning
from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.graphql import fragments
from slingshot.shared.utils import (
    get_default_num_gpu,
    machine_size_to_machine_type_gpu_count,
    machine_type_gpu_count_to_machine_size,
)

if typing.TYPE_CHECKING:
    from pydantic.main import IncEx

REPO = "https://github.com/slingshot-ai/slingshot"
PATH_TO_FILE = "slingshot_client/src/slingshot/schemas"
FILENAME = "slingshot-schema.config.json"
FILE_LOCATION = "/".join([REPO, "blob/main", PATH_TO_FILE, FILENAME])
ALPHANUMERIC_UNDERSCORE_HYPHEN_RE = "^[A-Za-z][A-Za-z0-9_-]*$"  # This should match the regex on the backend
LOCAL_ONLY_MANIFEST_SECTIONS = ['sources']


class SlingshotBaseModel(BaseModel):
    model_config = ConfigDict(extra='forbid')


# NOTE: We prefer to forbid extra fields, but this is not compatible with how Pydantic parse unions where fields
# are required in some places and not permitted in others. This would be clean if we had a single field that
# explicitly discriminated the type of subclass, but this does not work here as we support either a name or a tag,
# but without any other field that controls which.
class BaseMountSpec(SlingshotBaseModel):
    mode: str = Field(..., title="Mode", description="The mode to use for the mount.")
    path: str = Field(..., title="Path", description="The path to mount into the environment.", pattern=r'/mnt/[\w-]+')

    @field_validator('path', mode='after')
    @classmethod
    def fail_on_mount_paths_that_look_like_filenames(cls, path: str) -> str:
        if has_path_ending_in_filename(path):
            # TODO: raise custom error type instead of ValueError here and in other places so we can handle explicitly
            raise ValueError(
                f"The specified mount path '{path}' appears to be a filename. "
                + "Mounts paths must refer to directories, rather than individual files"
            )
        return path

    def diff(self, other: BaseMountSpec) -> list[str]:
        what_changed = []
        if self.mode != other.mode:
            what_changed.append(f"mode: {other.mode} → {self.mode}")
        if self.path != other.path:
            what_changed.append(f"path: {other.path} → {self.path}")
        return what_changed


class MountSelector(BaseModel):
    name: str = Field(..., title="Name", description="The name of the artifact to download.")
    tag: str | None = Field('latest', title="Tag", description="The tag of the artifact.")
    project: str | None = Field(
        None,
        title="Project",
        description="The id of a project to download an artifact from, only required when accessing artifacts from other projects",
    )

    def diff(self, other: MountSelector) -> list[str]:
        what_changed = []
        if self.name != other.name:
            what_changed.append(f"name: {other.name} → {self.name}")
        if self.tag != other.tag and self.tag and self.tag is not None and other.tag is not None:
            what_changed.append(f"tag: {other.tag} → {self.tag}")
        if self.project != other.project and self.tag and self.project is not None and other.project is not None:
            what_changed.append(f"project: {other.project} → {self.project}")
        return what_changed


class MountTarget(BaseModel):
    name: str = Field(..., title="Name", description="The name of the artifact to upload.")
    tag: str | None = Field(None, title="Tag", description="The tag(s) to apply to the artifact, comma separated.")

    @property
    def tags(self) -> list[str]:
        """Gets the tags as a list, sorted alphabetically to ensure a canonical representation."""
        return sorted([tag.strip() for tag in (self.tag.split(',') if self.tag else [])])

    def diff(self, other: MountTarget) -> list[str]:
        what_changed = []
        if self.name != other.name:
            what_changed.append(f"name: {other.name} → {self.name}")
        if self.tags != other.tags and self.tag:
            what_changed.append(f"tag(s): {','.join(other.tags) or 'None'} → {','.join(self.tags) or 'None'}")
        return what_changed


class DownloadMountSpec(BaseMountSpec):
    mode: Literal["DOWNLOAD"] = Field(..., title="Mode", description="The mode to use for the mount.")
    selector: MountSelector = Field(..., title="Selector", description="The artifact selector.")

    def diff(self, other: BaseMountSpec) -> list[str]:
        d = super().diff(other)
        if isinstance(other, DownloadMountSpec):
            d.extend(self.selector.diff(other.selector))
        return d


class UploadMountSpec(BaseMountSpec):
    mode: Literal["UPLOAD"] = Field(..., title="Mode", description="The mode to use for the mount.")
    target: MountTarget = Field(..., title="Target", description="The artifact target.")

    def diff(self, other: BaseMountSpec) -> list[str]:
        d = super().diff(other)
        if isinstance(other, UploadMountSpec):
            d.extend(self.target.diff(other.target))
        return d


class VolumeMountSpec(BaseMountSpec):
    mode: Literal["VOLUME"] = Field(..., title="Mode", description="The mode to use for the mount.")
    name: str = Field(..., title="Name", description="The name of the volume to mount.")

    def diff(self, other: BaseMountSpec) -> list[str]:
        d = super().diff(other)
        if isinstance(other, VolumeMountSpec) and self.name != other.name:
            d.append(f"name: {other.name} → {self.name}")
        return d


MountSpecUnion = Annotated[Union[DownloadMountSpec, UploadMountSpec, VolumeMountSpec], Field(discriminator="mode")]


class SourceMapping(SlingshotBaseModel):
    """Represents an individual source mapping configuration, pointing a local directory to a remote one."""

    path: str = Field(..., title="Path", description="Mapping in the format <localdir>:<remotedir>.")
    exclude_paths: list[str] = Field(
        default_factory=list,
        alias="excludePaths",
        title="Exclude paths",
        description="A list of .gitignore style rules used to exclude source files.",
    )

    @property
    def local_path(self) -> Path:
        return Path(SourceMapping._split_path(self.path)[0])

    @property
    def remote_path(self) -> Path:
        return Path(SourceMapping._split_path(self.path)[1])

    @field_validator("path", mode='before')
    @classmethod
    def ensure_path_mapping_is_valid(cls, path: str) -> str:
        if not isinstance(path, str):
            raise ValueError("path must be a string")

        from_path_str, to_path_str = SourceMapping._split_path(path)

        PurePath(from_path_str)
        to_path = PurePath(to_path_str)

        if to_path.is_absolute():
            raise ValueError("Remote path must be relative")
        # NOTE: We prevent all usages of .. here for two reasons:
        # 1. So that we can prevent users from going above the working directory in a remote, as this won't work
        #    for the push/zip case
        # 2. So that we can compare remote paths without ambiguity, as we don't allow multiple mappings for the same
        #    remote directory (and we don't want to see both foo/../bar and bar)
        if ".." in to_path_str:
            raise ValueError("Remote path may not contain '..'")

        return path

    @staticmethod
    def _split_path(path_str: str) -> tuple[str, str]:
        # NOTE: Windows is a thing, don't just split on :, take the last occurance
        split_idx = path_str.rfind(":")
        if split_idx == -1:
            raise ValueError("Path must be in the format <localdir>:<remotedir>")
        return path_str[:split_idx], path_str[split_idx + 1 :]


def remote_mount_spec_to_local(mount_spec: fragments.MountSpec) -> MountSpecUnion:
    if mount_spec.mode == "DOWNLOAD":
        return DownloadMountSpec(
            mode="DOWNLOAD",
            path=mount_spec.path,
            selector=MountSelector(name=mount_spec.name, tag=mount_spec.tag, project=mount_spec.referenced_project_id),
        )
    elif mount_spec.mode == "UPLOAD":
        return UploadMountSpec(
            mode="UPLOAD", path=mount_spec.path, target=MountTarget(name=mount_spec.name, tag=mount_spec.tag)
        )
    elif mount_spec.mode == "VOLUME":
        return VolumeMountSpec(mode="VOLUME", path=mount_spec.path, name=mount_spec.name)
    raise SlingshotException(f"Unknown mount mode: {mount_spec.mode}")


def diff_mount_spec(new: MountSpecUnion, existing: fragments.MountSpec) -> list[str]:
    """Returns a list of differences between a local and a remote mount spec."""
    return new.diff(remote_mount_spec_to_local(existing))


class EnvironmentSpec(SlingshotBaseModel):
    python_version: Literal["3.10"] = Field("3.10", title="Python version")
    python_packages: list[str] = Field(
        default_factory=list,
        title="Python packages",
        description=f"List of Python packages to install in the environment.",
    )
    post_install_command: str = Field(
        "",
        title="Post-install command",
        description="Custom command to run after all packages have been installed. Skipped if not specified.",
    )
    apt_packages: list[str] = Field(
        default_factory=list, title="APT packages", description=f"List of APT packages to install"
    )
    model_config = ConfigDict(
        title="Environment",
        json_schema_extra={
            "example": {"python_version": "3.10", "python_packages": ["numpy", "pandas", "torch==2.0.1"]}
        },
    )

    # All python packages can be converted to RequestedRequirement
    @field_validator("python_packages")
    @classmethod
    def convert_python_packages(cls, v: list[str]) -> list[str]:
        for i in v:
            try:
                requested_requirements_from_str(i)
            except ValueError as e:
                raise ValueError(f"Error occurred while trying to parse python packages") from e
        return v

    def diff(self, existing: fragments.ExecutionEnvironmentSpec) -> list[str]:
        """Returns a list of differences between this and another environment."""
        diff = []
        current_python_packages = [requested_requirements_from_str(pkg) for pkg in self.python_packages]
        current_apt_packages = [schemas.RequestedAptPackage(name=pkg) for pkg in self.apt_packages]
        assert existing.environment_instances, "Environment spec has no instances"
        existing_env_instance = existing.environment_instances[0]
        existing_python_packages = TypeAdapter(list[RequestedRequirement]).validate_python(
            existing_env_instance.requested_python_requirements
        )
        existing_apt_packages = TypeAdapter(list[schemas.RequestedAptPackage]).validate_python(
            existing_env_instance.requested_apt_packages
        )
        existing_post_install_command = existing_env_instance.post_install_command

        if existing_post_install_command != self.post_install_command:
            existing_post_install_command_repr = existing_post_install_command.replace("\n", "\\n")
            new_post_install_command_repr = self.post_install_command.replace("\n", "\\n")
            diff.append(f"Post-install command: {existing_post_install_command_repr} → {new_post_install_command_repr}")

        python_package_diffs = self._diff_python_requirements(current_python_packages, existing_python_packages)
        if python_package_diffs:
            diff.append(f"Python packages changed")
            diff.extend(python_package_diffs)

        apt_package_diffs = self._diff_apt_packages(current_apt_packages, existing_apt_packages)
        if apt_package_diffs:
            diff.append(f"APT packages changed")
            diff.extend(apt_package_diffs)

        return diff

    @staticmethod
    def _diff_python_requirements(
        current: list[RequestedRequirement], existing: list[RequestedRequirement]
    ) -> list[str]:
        diff = []
        for req in current:
            if req not in existing:
                diff.append(f"  [green]+[/green] {str(req)}")
        for req in existing:
            if req not in current:
                diff.append(f"  [red]-[/red] {str(req)}")
        return diff

    @staticmethod
    def _diff_apt_packages(
        current: list[schemas.RequestedAptPackage], existing: list[schemas.RequestedAptPackage]
    ) -> list[str]:
        diff = []
        for req in current:
            if req not in existing:
                diff.append(f"  [green]+[/green] {req.name}")
        for req in existing:
            if req not in current:
                diff.append(f"  [red]-[/red] {req.name}")
        return diff


class AbstractComponentSpec(SlingshotBaseModel, ABC):
    """
    Base class for all component definitions, including runs, deployments, apps, and the specific app sub types.
    """

    name: str = Field(..., title="Name", description="The name of the app.", pattern=ALPHANUMERIC_UNDERSCORE_HYPHEN_RE)
    machine_type: schemas.MachineType = Field(..., title="Machine type", description="The machine type to be used.")
    num_gpu: int | None = Field(
        None, title="Number of GPUs", description="The number of GPUs to use.", validate_default=True
    )
    config_variables: dict[str, Any] = Field(
        default_factory=dict, title="Arguments", description="Optional user defined arguments to pass to the app."
    )
    mounts: list[MountSpecUnion] = Field(default_factory=list, title="Mounts", description="The mounts to be attached.")
    attach_project_credentials: bool = Field(
        True,
        title="Attach project credentials",
        description=(
            "If true, will make an API key available to instances under the `SLINGSHOT_API_KEY` environment"
            "variable so that they can make requests using the Slingshot SDK for this project"
        ),
    )

    model_config = ConfigDict(title="Component")

    @model_validator(mode='before')
    @classmethod
    def warn_on_missing_explicit_machine_type(cls, data: Any) -> Any:
        if 'machine_type' not in data or not data['machine_type']:
            default_machine_type = schemas.MachineType.CPU_SMALL
            if not cls in [WebappComponentSpec, LabelStudioComponentSpec, RedisComponentSpec]:
                # We're defaulting silently for apps, see https://linear.app/slingshotai/issue/ENG-1998
                record_validation_warning(
                    SlingshotDeprecationWarning(
                        f"'machine_type' not set for '{data['name']}', defaulting to '{default_machine_type}'. "
                        + "Specifying machine_type will be required in upcoming versions of the CLI."
                    )
                )
            return {**data, 'machine_type': default_machine_type}

        return data

    @model_validator(mode='before')
    @classmethod
    def warn_on_use_of_machine_size(cls, data: dict[str, typing.Any]) -> Any:
        if 'machine_size' in data:
            record_validation_warning(
                SlingshotDeprecationWarning(
                    "'machine_size' has been replaced with 'machine_type'. "
                    + "Use 'slingshot machines' to see available options"
                )
            )

        return data

    @field_validator("config_variables", mode='before')
    @classmethod
    def show_nicer_error_for_nested_config_variables(cls, v: dict[str, Any]) -> dict[str, Any]:
        """
        Pydantic will enforce this already but the errors aren't pretty, do a manual check here.
        """
        if not isinstance(v, dict):
            raise ValueError("config_variables must be a mapping")

        return v

    @field_validator("mounts")
    @classmethod
    def validate_mount_paths_unique(cls, v: list[MountSpecUnion]) -> list[MountSpecUnion]:
        """
        Verify that all mount paths are unique. We add an explicit message for the case of a download path conflicting
        with an upload path as prior to Aug 2023 this used to be supported.
        """
        download_paths = [str(spec.path) for spec in v if spec.mode == "DOWNLOAD"]
        upload_paths = [str(spec.path) for spec in v if spec.mode == "UPLOAD"]
        all_mount_paths = [str(spec.path) for spec in v]

        # TODO: mention which paths are conflicting in the error
        if set(download_paths).intersection(set(upload_paths)):
            raise ValueError("The same mount path cannot be used for both upload and download.")
        if len(all_mount_paths) != len(set(all_mount_paths)):
            raise ValueError("Mount paths must be unique across all mounts")

        return v

    @field_validator("num_gpu", mode="before")
    @classmethod
    def validate_num_gpu(cls, v: int | None, info: FieldValidationInfo) -> int | None:
        """Validate that the number of GPUs is valid based on machine_type."""
        if "machine_type" not in info.data:
            # This means the user has input an invalid machine type, therefore we can't deduce the number of GPUs.
            return None
        machine_type: schemas.MachineType = info.data["machine_type"]
        v = v if v is not None else get_default_num_gpu(machine_type)
        try:
            machine_type_gpu_count_to_machine_size(gpu_count=v, machine_type=machine_type)
        except ValueError as e:
            raise ValueError(f"Invalid number of GPUs ({v}) for machine type {machine_type}") from e
        return v

    def diff(self, existing: fragments.ComponentSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        diff = []
        name = existing.spec_name
        config_variables = json.loads(existing.config_variables) if existing.config_variables else {}

        existing_machine_type, existing_num_gpu = machine_size_to_machine_type_gpu_count(existing.machine_size)
        self_machine_type = self.machine_type
        self_num_gpu = self.num_gpu

        if self.name != name:
            diff.append(f"Name changed from '{name}' → '{self.name}'")
        if deepdiff.DeepDiff(config_variables, self.config_variables, ignore_order=True):
            diff.append(f'Config variables changed from {config_variables} → {self.config_variables}')
        if self_machine_type != existing_machine_type:
            diff.append(f"Machine type changed from '{existing_machine_type}' → '{self_machine_type}'")
        if self_num_gpu != existing_num_gpu:
            diff.append(f"Number of GPUs changed from '{existing_num_gpu}' → '{self_num_gpu}'")
        if self.attach_project_credentials and not existing.service_account:
            diff.append(f"Project credentials added")
        elif not self.attach_project_credentials and existing.service_account:
            diff.append(f"Project credentials removed")

        my_mount_path = {f"{i.mode}: {i.path}": i for i in self.mounts}
        existing_mounts = {f"{i.mode}: {i.path}": i for i in existing.mount_specs}
        added_keys = set(my_mount_path.keys()) - set(existing_mounts.keys())
        for i in added_keys:
            diff.append(f"Added mount '{i}'")
        removed_keys = set(existing_mounts.keys()) - set(my_mount_path.keys())
        for i in removed_keys:
            diff.append(f"Removed mount '{i}'")
        same_path = set(existing_mounts.keys()) & set(my_mount_path.keys())
        for i in same_path:
            existing_mount = existing_mounts[i]
            new = my_mount_path[i]
            d = diff_mount_spec(new, existing_mount)
            if d:
                diff.append(f"Changed mount '{i}': {d}")

        return diff


class WebappComponentSpec(AbstractComponentSpec):
    using: Literal['webapp'] = Field(
        ..., title="Using", description="Which package to use. Set to webapp for a custom web application."
    )
    port: Optional[int] = Field(None, title="Port", description="The port to expose.")
    cmd: str = Field(..., title="Command", description="The command to run.")
    environment: str = Field(..., title="Environment", description="The name of the environment.")

    model_config = ConfigDict(title="Web app")

    def diff(self, existing: fragments.ComponentSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.component_type != schemas.ComponentType.APP:
            raise ValueError(f"Cannot diff an app against a non-app.")
        diff = super().diff(existing)
        env_spec = existing.execution_environment_spec
        environment = env_spec.execution_environment_spec_name if env_spec else None
        if self.environment != environment:
            diff.append(f"Environment changed from '{environment}' → '{self.environment}'")
        if self.cmd != existing.command:
            diff.append(f"Command changed from '{existing.command}' → '{self.cmd}'")
        if self.port != existing.app_port:
            diff.append(f"Port changed from '{existing.app_port}' → '{self.port}'")
        return diff


class SessionComponentSpec(AbstractComponentSpec):
    using: Literal['session'] = Field(
        ...,
        title="Using",
        description="Which package to use. When specified, this feature automatically adjusts the behavior of the app.",
    )
    # TODO: Allow users to not specify envs for Sessions
    environment: str = Field(..., title="Environment", description="The name of the execution environment.")

    model_config = ConfigDict(title="Session")

    @property
    def port(self) -> int:
        return 8080

    def diff(self, existing: fragments.ComponentSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_sub_type != schemas.AppSubType.SESSION:
            raise ValueError(f"Cannot diff session app against a non-session.")
        diff = super().diff(existing)
        env_spec = existing.execution_environment_spec
        environment = env_spec.execution_environment_spec_name if env_spec else None
        if self.environment != environment:
            diff.append(f"Environment changed from '{environment}' → '{self.environment}'")
        if self.port != existing.app_port:
            diff.append(f"Port changed from '{existing.app_port}' → '{self.port}'")
        return diff


class RedisComponentSpec(AbstractComponentSpec):
    using: Literal['redis'] = Field(
        ...,
        title="Using",
        description="Which package to use. When specified, this feature automatically adjusts the behavior of the app.",
    )

    model_config = ConfigDict(title="Redis")

    @property
    def port(self) -> int:
        return 6379

    def diff(self, existing: fragments.ComponentSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_sub_type != schemas.AppSubType.REDIS:
            raise ValueError(f"Cannot diff Redis app against other component type.")
        diff = super().diff(existing)
        if self.port != existing.app_port:
            diff.append(f"Port changed from '{existing.app_port}' → '{self.port}'")
        return diff


class LabelStudioComponentSpec(AbstractComponentSpec):
    using: Literal['label-studio'] = Field(
        ...,
        title="Using",
        description="Which package to use. When specified, this feature automatically adjusts the behavior of the app.",
    )

    import_run: str = Field(
        "label-studio-import",
        title="Import Run",
        description="The name of the run used to import data to Label Studio.",
    )

    export_run: str = Field(
        "label-studio-export",
        title="Export Run",
        description="The name of the run used to export data from Label Studio.",
    )

    model_config = ConfigDict(title="Label Studio")

    @staticmethod
    def get_default_import_run() -> RunSpec:
        return RunSpec(
            name="label-studio-import",
            environment="label-studio-run-env",
            machine_type=schemas.MachineType.CPU_SMALL,
            cmd="python label_studio/label_studio_import.py",
            mounts=[
                DownloadMountSpec(mode="DOWNLOAD", path="/mnt/data", selector=MountSelector(name="dataset")),
                DownloadMountSpec(mode="DOWNLOAD", path="/mnt/annotations", selector=MountSelector(name="annotations")),
            ],
        )

    @staticmethod
    def get_default_export_run() -> RunSpec:
        return RunSpec(
            name="label-studio-export",
            environment="label-studio-run-env",
            machine_type=schemas.MachineType.CPU_SMALL,
            cmd="python label_studio/label_studio_export.py",
            mounts=[UploadMountSpec(mode="UPLOAD", path="/mnt/annotations", target=MountTarget(name="annotations"))],
            attach_project_credentials=True,
        )

    @staticmethod
    def get_default_run_environment() -> EnvironmentSpec:
        return EnvironmentSpec(python_packages=["label-studio-sdk>=0.0.30", "slingshot-ai"])

    def diff(self, existing: fragments.ComponentSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_sub_type != schemas.AppSubType.LABEL_STUDIO:
            raise ValueError(f"Cannot diff Label Studio app against other component type.")
        diff = super().diff(existing)
        # TODO: Add diff for import/export runs
        return diff


class RunSpec(AbstractComponentSpec):
    name: str = Field("run", title="Name", description="The name of the run.")
    cmd: str = Field(..., title="Command", description="The command to run.")
    environment: str = Field(..., title="Environment", description="The name of the environment.")

    model_config = ConfigDict(title="Run")

    def diff(self, existing: fragments.ComponentSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.component_type != schemas.ComponentType.RUN:
            raise ValueError(f"Cannot diff a run against a non-run.")
        diff = super().diff(existing)
        env_spec = existing.execution_environment_spec
        environment = env_spec.execution_environment_spec_name if env_spec else None
        if self.environment != environment:
            diff.append(f"Environment changed from '{environment}' → '{self.environment}'")
        if self.cmd != existing.command:
            diff.append(f"Command changed from '{existing.command}' → '{self.cmd}'")
        return diff


class DeploymentSpec(AbstractComponentSpec):
    name: str = Field("deployment", title="Name", description="The name of the deployment.")
    cmd: str = Field(..., title="Command", description="The command to run.")
    environment: str = Field(..., title="Environment", description="The name of the environment.")
    model_config = ConfigDict(title="Deployment")

    def diff(self, existing: fragments.ComponentSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.component_type != schemas.ComponentType.DEPLOYMENT:
            raise ValueError(f"Cannot diff a run against a non-deployment.")
        diff = super().diff(existing)
        env_spec = existing.execution_environment_spec
        environment = env_spec.execution_environment_spec_name if env_spec else None
        if self.environment != environment:
            diff.append(f"Environment changed from '{environment}' → '{self.environment}'")
        if self.cmd != existing.command:
            diff.append(f"Command changed from '{existing.command}' → '{self.cmd}'")
        return diff


AppSpecUnion = Annotated[
    Union[SessionComponentSpec, RedisComponentSpec, LabelStudioComponentSpec, WebappComponentSpec],
    Field(discriminator='using'),
]


class SafeAppSpec(RootModel[AppSpecUnion]):
    """
    Reads an app spec with extra validation for missing 'using'. Using a root model appears to be the only way to add
    validation before Pydantic picks the specific class to validate - this significantly improves the error message
    when no 'using' is specified.
    """

    @model_validator(mode='before')
    @classmethod
    def require_sub_type_to_be_specified(cls, data: Any) -> Any:
        if isinstance(data, BaseModel):
            data = data.model_dump()

        if 'using' not in data or not data['using']:
            record_validation_warning(
                SlingshotDeprecationWarning("Specifying 'using' for an app is required since version 0.0.19")
            )

            raise ValueError("Apps require a 'using' field to be specified, use 'webapp' for a custom web application")
        return data


class ProjectManifest(SlingshotBaseModel):
    environments: dict[str, EnvironmentSpec] = Field(
        default_factory=dict, title="Environments", description="The environments to use for the job."
    )
    apps: list[AppSpecUnion] = Field(default_factory=list, title=AbstractComponentSpec.model_config["title"])
    runs: list[RunSpec] = Field(default_factory=list, title=RunSpec.model_config["title"])
    deployments: list[DeploymentSpec] = Field(default_factory=list, title=DeploymentSpec.model_config["title"])
    sources: list[SourceMapping] | None = Field(
        None,
        title="Sources",
        description="Sources to include for Slingshot components. If not set, the project directory will be used. "
        "Can be set to an empty list to explicitly disable sources.",
    )

    model_config = ConfigDict(
        title="Slingshot Config Spec",
        from_attributes=True,
        json_schema_extra={"$schema": "http://json-schema.org/draft/2020-12/schema", "$id": FILE_LOCATION},
    )

    @override
    def model_dump(
        self,
        *,
        mode: Literal['json', 'python'] | str = 'python',
        by_alias: bool = False,
        include: IncEx = None,
        exclude: IncEx = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = True,  # Overriden from Pydantic defaults
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
        # If true, sections of the manifest that are local only (not not pushed to Slingshot) will be excluded,
        # if false (the default), all sections will be included.
        exclude_local_only: bool = False,
    ) -> dict[str, Any]:
        # We override the include/exclude logic, users shoudn't pass explicit values
        assert include is None and exclude is None, "The project manifest doesn't support include/exclude"

        if exclude_local_only:
            exclude = set(LOCAL_ONLY_MANIFEST_SECTIONS)

        res = super().model_dump(
            mode=mode,
            exclude=exclude,
            by_alias=by_alias,
            exclude_none=exclude_none,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            round_trip=round_trip,
            warnings=warnings,
        )

        # We usually want "exclude_defaults" so as to not fill up our slingshot.yaml with a lot of redundant values
        # when pulling in remote changes, but the top level definitions are different. We always populate them as a
        # placeholder to the user and to make diffs cleaner when environments and components are added for the first
        # time. To get the behaviour that we want without passing "exclude_defaults" to the child models, we explicitly
        # populate the empty objects here.
        if 'environments' not in res:
            res['environments'] = dict()
        if 'apps' not in res:
            res['apps'] = []
        if 'runs' not in res:
            res['runs'] = []
        if 'deployments' not in res:
            res['deployments'] = []

        return res

    @field_validator('apps', mode='before')
    @classmethod
    def complain_if_missing_using_in_app(cls, value: Any) -> list[Any]:
        return [SafeAppSpec.model_validate(app).root for app in value]

    @model_validator(mode="after")
    def slingshot_yaml_global_validator(self) -> ProjectManifest:
        ProjectManifest.validate_label_studio_runs(self)
        # Must be before env validation, since it might add new envs
        ProjectManifest.validate_environments_are_defined(self)
        ProjectManifest.validate_session_environments(self)
        ProjectManifest.validate_source_mappings_are_unique(self)
        return self

    @model_validator(mode='before')
    @classmethod
    def check_machine_deprecations(cls, manifest: dict[str, Any]) -> dict[str, Any]:
        all_apps_runs_deployments = []
        all_apps_runs_deployments.extend(manifest['apps'] if 'apps' in manifest else [])
        all_apps_runs_deployments.extend(manifest['runs'] if 'runs' in manifest else [])
        all_apps_runs_deployments.extend(manifest['deployments'] if 'deployments' in manifest else [])

        # Check old GPUs
        for app_run_deployment in all_apps_runs_deployments:
            machine_type = app_run_deployment['machine_type'] if 'machine_type' in app_run_deployment else None
            if machine_type in {"GPU", "GPU_A100"}:
                record_validation_warning(
                    SlingshotDeprecationWarning(
                        f"Machine type '{machine_type}' is not supported in slingshot.yaml (since version '0.0.10'). "
                        + "Hint: Use 'slingshot machines' for machine options."
                    )
                )

        return manifest

    @staticmethod
    def validate_environments_are_defined(manifest: ProjectManifest) -> None:
        """Validate that all referenced environments are in the environments list"""
        envs: dict[str, EnvironmentSpec] = manifest.environments
        for app_or_run_or_deployment in [*manifest.apps, *manifest.runs, *manifest.deployments]:
            env = getattr(app_or_run_or_deployment, "environment", None)
            if env and env not in envs:
                name = getattr(app_or_run_or_deployment, "name", None)
                raise SlingshotException(
                    f"Environment '{env}' used in '{name}' not found in 'environments' {list(envs.keys())}"
                )

    @staticmethod
    def validate_session_environments(manifest: ProjectManifest) -> None:
        sessions = [app for app in manifest.apps if isinstance(app, SessionComponentSpec)]
        envs: dict[str, EnvironmentSpec] = manifest.environments
        session_envs = {session.environment: envs[session.environment] for session in sessions if session.environment}

        for session_env_name, session_env in session_envs.items():
            requested_python_requirements = session_env.python_packages
            if not any("jupyterlab" in requirement for requirement in requested_python_requirements):
                raise SlingshotException(
                    f"'jupyterlab' was not found in the '{session_env_name}' environment. Please add it and try again."
                )

    @staticmethod
    def validate_label_studio_runs(manifest: ProjectManifest) -> None:
        """Make sure Label Studio is set up correctly"""
        label_studio_apps = [app for app in manifest.apps if isinstance(app, LabelStudioComponentSpec)]
        if not label_studio_apps:
            return
        if len(label_studio_apps) > 1:
            app_names = [app.name for app in label_studio_apps]
            # TODO: Implement logic for multiple label studio apps
            raise SlingshotException(f"Only one label studio app is supported per Slingshot Project. Found {app_names}")

        runs: list[RunSpec] = manifest.runs
        import_run_name = label_studio_apps[0].import_run
        export_run_name = label_studio_apps[0].export_run
        label_studio_app_name = label_studio_apps[0].name

        if import_run_name not in [run.name for run in runs]:
            raise SlingshotException(
                f"Run '{import_run_name}' (used as the 'import_run' for {label_studio_app_name}) was not found in "
                "'runs'. Please add it and try again."
            )

        if export_run_name not in [run.name for run in runs]:
            raise SlingshotException(
                f"Run '{export_run_name}' (used as the 'export_run' for {label_studio_app_name}) was not found in "
                "'runs'. Please add it and try again."
            )

    @staticmethod
    def validate_source_mappings_are_unique(manifest: ProjectManifest) -> None:
        destinations = [source.remote_path for source in (manifest.sources or [])]
        if len(set(destinations)) != len(destinations):
            raise SlingshotException("Remote directories in source mappings must be unique.")


if __name__ == "__main__":
    with open(Path(PATH_TO_FILE) / FILENAME, "w") as f:
        json.dump(ProjectManifest.model_json_schema(), f, indent=2)
