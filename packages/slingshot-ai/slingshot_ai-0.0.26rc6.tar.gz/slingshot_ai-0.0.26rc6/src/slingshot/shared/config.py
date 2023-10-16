from __future__ import annotations

import typing
from collections.abc import Iterable
from pathlib import Path
from typing import Optional, Type, Union

from pydantic import BaseModel, ValidationError
from pydantic_core import ErrorDetails
from rich.console import Console
from ruamel import yaml as r_yaml

from slingshot import schemas
from slingshot.schemas import SlingshotDeprecationWarning, SlingshotValidationWarningMessage, catch_validation_warnings
from slingshot.sdk.config import client_settings
from slingshot.sdk.errors import SlingshotException, SlingshotFileNotFoundException

console: Console = Console()


_cached_config: Optional[schemas.ProjectManifest] = None
_cached_config_path: Optional[Path] = None


def load_slingshot_project_config(
    config_path: Optional[Path] = None, force_reload: bool = False, silence_warnings: bool = False
) -> schemas.ProjectManifest:
    global _cached_config
    global _cached_config_path
    config_path = config_path if config_path is not None else client_settings.slingshot_config_path
    if force_reload or not _cached_config or config_path != _cached_config_path:
        _cached_config = load_slingshot_manifest_from_path(config_path, silence_warnings=silence_warnings)
        _cached_config_path = config_path
    return _cached_config


def mark_slingshot_project_config_dirty() -> None:
    """
    Ensures that the next attempt to load the slingshot.yaml file will reload it from disk,
    not using a cached value.
    """
    global _cached_config
    global _cached_config_path
    _cached_config = None
    _cached_config_path = None


def load_slingshot_manifest_from_path(config_path: Path, silence_warnings: bool = False) -> schemas.ProjectManifest:
    """
    Loads the slingshot.yaml file from the given path and parses it into a ProjectManifest object.

    :param config_path: The path to the slingshot.yaml file. This should only be used for testing.
    :param silence_warnings: If True, warnings will not be printed to the console.
    :return ProjectManifest:
    """
    try:
        text = config_path.read_text()
    except FileNotFoundError as e:
        raise SlingshotFileNotFoundException(
            f"Could not find slingshot.yaml at {config_path}.\n" f"You can add one by running 'slingshot init'"
        ) from e
    try:
        config_yaml = r_yaml.safe_load(text)
    except r_yaml.YAMLError as e:
        raise SlingshotException(f"Could not parse slingshot.yaml in {config_path}") from e
    if not config_yaml:
        raise SlingshotException(f"Empty slingshot.yaml in {config_path}. Please run 'slingshot init'")
    try:
        with catch_validation_warnings() as validation_warnings:
            config = schemas.ProjectManifest.model_validate(config_yaml)

    except Exception as e:
        # Don't capture warnings twice, we'll get more of them as we try to parse specific sections independently
        with catch_validation_warnings():
            raise _beautify_project_manifest_parsing_exception(config_yaml, e) from e
    finally:
        # Report validation warnings regardless of errors
        if not silence_warnings:
            _report_warnings(validation_warnings)
    return config


def _report_warnings(warnings: list[SlingshotValidationWarningMessage]) -> None:
    deprecation_warnings = [w.message for w in warnings if w.category == SlingshotDeprecationWarning]
    if deprecation_warnings:
        console.print("[yellow]⚠️ Detected deprecated usages in slingshot.yaml: [/yellow]")
        for warning in deprecation_warnings:
            console.print(f"    {warning}")
    other_validation_warnings = [w.message for w in warnings if w.category != SlingshotDeprecationWarning]
    if other_validation_warnings:
        console.print("[yellow]⚠️ Loaded slingshot.yaml with warnings:[/yellow]")
        for warning in other_validation_warnings:
            console.print(f"    {warning}")


def _describe_loc(loc: Iterable[Union[str, int]]) -> str:
    """
    Converts a "loc" (location) of a validation error from the Pydantic format to something that makes
    more sense to a user looking at their slignshot.yaml. The Pydantic path includes a few things that
    might make sense in the Python object world but don't really map to the .yaml file, including:
    * The name of the model that is being instantiated
    * The discriminator, when using discriminating unions (e.g. the value of the "using" value for apps,
      or mode for mounts) - in uppercase.
    We check for these cases and strip them out as not helpful to the user. We also show numerical
    indices using [] notation, e.g. mounts[0] instead of mounts.0 to indicate the first entry in a list

    Examples:
        >>> _describe_loc(["apps", 0, "using"])
        'apps[0].using'
        >>> _describe_loc(["mounts", 0, "DOWNLOAD"])
        'mounts[0]'
        >>> _describe_loc(["apps", 1, "SlingshotCustomAppSpec", "cmd"])
        'apps[1].cmd'
    """
    res = ""
    for l in loc:
        if isinstance(l, int):
            res += f"[{l}]"
        elif l.endswith("Spec"):
            # HACK: Pydantic includes the spec name here, but it won't mean much to the user - we drop it
            continue
        elif l.upper() == l:
            # HACK: Pydantic includes discriminator fields in the path (such as mode for mounts), don't show these
            continue
        else:
            if res:
                res += "."
            res += l

    return res


def _describe_error(err: ErrorDetails) -> str:
    """
    Prettifies errors as given by Pydantic. While the default messages are mostly fine, there are cases where we can
    be more clear by checking the specific error code and overriding the message. We also clean up the 'loc' as
    provided by Pydantic to give a location more relevant to the structure of the slingshot.yaml file, stripping out
    bits that only make sense in the Python object world such as the name of models or the discriminator.
    """

    msg = err['msg']
    if err['type'] == 'extra_forbidden':
        msg = 'Unrecognized extra field'

    # Pydantic includes "Value error" as the prefix for ValueErrors thrown by explicit validators, remove this
    msg = msg.replace("Value error, ", "")
    loc = _describe_loc(err['loc'])

    return f"{f'{loc}: ' if loc else ''}{msg}\n"


def _validate_dict_section(
    config_yaml: dict[typing.Any, typing.Any], section_key: str, section_name: str, model: Type[BaseModel]
) -> str:
    message = ""
    config_fragment_yaml = config_yaml[section_key]
    if not isinstance(config_fragment_yaml, dict):
        raise SlingshotException(f"'{section_key}' must be a YAML mapping (was: {type(config_fragment_yaml)})")
    # Try to parse each environment individually to get a more helpful error message,
    #  if it's one of them that's failing.
    for sub_section_name, sub_section in config_fragment_yaml.items():
        try:
            model.model_validate(sub_section)
        except ValidationError as e2:
            message = f"{section_name} [yellow]{sub_section_name}[/yellow] has errors:\n"
            for err in e2.errors():
                message += f"    {_describe_error(err)}"
    return message


def _validate_list_section(
    config_yaml: dict[typing.Any, typing.Any], section_key: str, section_name: str, model: Type[BaseModel]
) -> str:
    message = ""
    config_fragment_yaml = config_yaml[section_key]
    if not isinstance(config_fragment_yaml, list):
        raise SlingshotException(f"'{section_key}' must be a YAML list (was: {type(config_fragment_yaml)})")
    # Try to parse each environment individually to get a more helpful error message,
    #  if it's one of them that's failing.
    for sub_section in config_fragment_yaml:
        try:
            model.model_validate(sub_section)
        except ValidationError as e2:
            message = f"{section_name} [yellow]{sub_section['name']}[/yellow] has errors:\n"
            for err in e2.errors():
                message += f"    {_describe_error(err)}"
    return message


# noinspection PyBroadException
def _beautify_project_manifest_parsing_exception(
    config_yaml: dict[typing.Any, typing.Any], e: Exception
) -> SlingshotException:
    if isinstance(e, SlingshotException):
        return e

    message = ""
    if (isinstance(e, ValidationError) or isinstance(e, KeyError)) and 'environments' in str(e):
        message += _validate_dict_section(config_yaml, 'environments', "Environment", schemas.EnvironmentSpec)
    if (isinstance(e, ValidationError) or isinstance(e, KeyError)) and 'apps' in str(e):
        message += _validate_list_section(config_yaml, 'apps', "App", schemas.SafeAppSpec)
    if (isinstance(e, ValidationError) or isinstance(e, KeyError)) and 'runs' in str(e):
        message += _validate_list_section(config_yaml, 'runs', "Run", schemas.RunSpec)
    if (isinstance(e, ValidationError) or isinstance(e, KeyError)) and 'deployments' in str(e):
        message += _validate_list_section(config_yaml, 'deployments', "Deployment", schemas.DeploymentSpec)
    if isinstance(e, ValidationError) and not message:
        # If we've not been able to trigger the custom handling above, show the messages as is
        for error in e.errors():
            message += _describe_error(error)

    if message:
        return SlingshotException("Your slingshot.yaml file contains validation errors:\n" + message.strip())
    else:
        return SlingshotException(f"Invalid slingshot.yaml: {e=}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
