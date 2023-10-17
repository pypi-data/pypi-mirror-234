from __future__ import annotations

import os
import typing
from typing import TYPE_CHECKING, Callable, Literal, Optional

import typer
from click import Choice
from simple_term_menu import TerminalMenu  # type: ignore

from slingshot import schemas
from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.graphql import fragments
from slingshot.sdk.utils import console

if TYPE_CHECKING:
    from slingshot.sdk import SlingshotSDK


T = typing.TypeVar("T")


class RefValue(typing.Generic[T]):
    def __init__(self, value: T) -> None:
        self.current = value


GLOBAL_Y_AUTO_CONFIRM_REF = RefValue(False)


def prompt_for_single_choice(
    prompt_text: str,
    values: list[str],
    skip_if_one_value: bool = False,
    default: Optional[int] = None,
    skip_silently: bool = False,
) -> int:
    """
    Prompts the user to select a single value from a list of values. Returns the selected value.

    Example:
        prompt_for_single_choice("Select a color", ["red", "green", "blue"])
    """
    assert len(values) > 0, "No values provided to prompt_for_single_choice"
    prompt_text = prompt_text.rstrip(":")
    prompt_text = f"{prompt_text}:" if not prompt_text.endswith("?") else prompt_text
    options_str = "\n".join([f"[{i + 1}] {val}" for i, val in enumerate(values)])

    if skip_if_one_value and len(values) == 1:
        if not skip_silently:
            console.print(f"{prompt_text}")
            console.print(f"{options_str}")
            console.print(f"Selected: {values[0]} (skipped, only option available)")
        return 0

    if os.environ.get("UNIT_TESTING") == "1":
        if default is not None:
            return default
        else:
            return 0

    if not console.is_terminal:
        raise SlingshotException("Not running within a known terminal. Cannot prompt.")

    menu = TerminalMenu(
        values,
        title=prompt_text,
        menu_highlight_style=("fg_red", "bold"),
        raise_error_on_interrupt=True,  # Raises KeyboardInterrupt on Ctrl-C --> Typer
        clear_menu_on_exit=False,  # Looks weird in Warp
        show_search_hint=True,
    )
    idx = menu.show()
    if idx is None:
        raise typer.Abort()
    selected = values[idx]
    console.print(f"Selected: {selected}\n")
    return idx


def prompt_confirm(prompt_text: str, default: bool) -> bool:
    """Prompts the user to select a binary choice. Returns True if the user selects "Y" or "y" """
    if GLOBAL_Y_AUTO_CONFIRM_REF.current:
        return True
    options = "[Y/n]" if default else "[y/N]"
    if os.environ.get("UNIT_TESTING") == "1":
        return default
    if not console.is_terminal:
        console.print(f"{prompt_text} {options}")
        raise SlingshotException("Not running within a known terminal. Cannot prompt.")
    choice = typer.prompt(
        f"{prompt_text} {options}",
        type=Choice(["Y", "N", "y", "n"]),
        default="y" if default else "n",
        show_default=False,
        show_choices=False,
    )
    return choice.lower() == "y"


def filter_for_apps(app: fragments.ComponentSpec) -> bool:
    return app.component_type == schemas.ComponentType.APP


def filter_for_runs(app: fragments.ComponentSpec) -> bool:
    return app.component_type == schemas.ComponentType.RUN


def filter_for_deployments(app: fragments.ComponentSpec) -> bool:
    return app.component_type == schemas.ComponentType.DEPLOYMENT


def filter_for_running_deployments(deployment_spec: fragments.ComponentSpec) -> bool:
    return deployment_spec.deployment_status is not None and deployment_spec.deployment_status.is_active


def filter_for_running_apps(app: fragments.ComponentSpec) -> bool:
    return app.app_instance_status is not None and app.app_instance_status.is_active


def filter_for_sessions(app: fragments.ComponentSpec) -> bool:
    return app.app_sub_type == schemas.AppSubType.SESSION


@typing.overload
async def prompt_for_app_spec(
    sdk: SlingshotSDK,
    *filters: Callable[[fragments.ComponentSpec], bool],
    app_display_name: str,
    raise_if_missing: Literal[True] = True,
    skip_if_one_value: bool = True,
) -> tuple[str, str]:
    ...


@typing.overload
async def prompt_for_app_spec(
    sdk: SlingshotSDK,
    *filters: Callable[[fragments.ComponentSpec], bool],
    app_display_name: str,
    raise_if_missing: Literal[False],
    skip_if_one_value: bool = True,
) -> tuple[str, str] | None:
    ...


async def prompt_for_app_spec(
    sdk: SlingshotSDK,
    *filters: Callable[[fragments.ComponentSpec], bool],
    app_display_name: str,
    raise_if_missing: bool = True,
    skip_if_one_value: bool = True,
) -> tuple[str, str] | None:
    """Prompts the user to select an app from the list of apps in the project."""
    all_app_specs = await sdk.list_components()
    app_specs = [component_spec for component_spec in all_app_specs if all(f(component_spec) for f in filters)]
    app_spec_names = [component_spec.spec_name for component_spec in app_specs]
    if len(app_spec_names) == 0:
        if raise_if_missing:
            raise SlingshotException(f"No {app_display_name}s found")
        console.print(f"No {app_display_name}s found")
        return None

    index = prompt_for_single_choice(f"Select {app_display_name}:", app_spec_names, skip_if_one_value=skip_if_one_value)
    spec_id = app_specs[index].spec_id
    spec_name = app_specs[index].spec_name
    return spec_id, spec_name


async def prompt_for_recent_run(
    sdk: SlingshotSDK,
    error_message: str = 'No runs found',
    skip_if_one_value: bool = False,
    allowed_status: Optional[set[schemas.ComponentInstanceStatus]] = None,
) -> fragments.Run:
    runs = await sdk.list_runs()
    if allowed_status is not None:
        runs = [run for run in runs if run.run_status in allowed_status]

    if not runs:
        raise SlingshotException(error_message)

    runs = sorted(runs, key=lambda run: run.created_at, reverse=True)[:5]
    # TODO: allow user to select "more" and get next page
    idx = prompt_for_single_choice(
        "Select a run:", [i.run_name for i in runs], skip_if_one_value=skip_if_one_value, default=0
    )
    return runs[idx]


async def run_by_name_or_prompt(
    sdk: SlingshotSDK,
    name: Optional[str] = None,
    allowed_status: Optional[set[schemas.ComponentInstanceStatus]] = None,
    error_message: str = "No runs found",
    skip_if_one_value: bool = False,
) -> fragments.Run:
    if name:
        run = await sdk.get_run(name)
        if not run:
            raise SlingshotException(f"Run {name} not found")
        return run
    return await prompt_for_recent_run(
        sdk, allowed_status=allowed_status, error_message=error_message, skip_if_one_value=skip_if_one_value
    )


async def deployment_spec_id_by_name_or_prompt(sdk: SlingshotSDK, name: Optional[str] = None) -> str:
    if name:
        deployment_spec = await sdk.get_deployment(name)
        if not deployment_spec:
            raise SlingshotException(f"Deployment '{name}' not found")
        return deployment_spec.spec_id

    spec_id, _ = await prompt_for_app_spec(sdk, filter_for_deployments, app_display_name="deployment")
    return spec_id


async def component_spec_id_by_name_or_prompt(sdk: SlingshotSDK, name: Optional[str] = None) -> str:
    if name:
        component_spec = await sdk.get_app(name)
        if not component_spec:
            raise SlingshotException(f"App '{name}' not found")
        return component_spec.spec_id

    spec_id, _ = await prompt_for_app_spec(sdk, filter_for_apps, app_display_name="app")
    return spec_id
