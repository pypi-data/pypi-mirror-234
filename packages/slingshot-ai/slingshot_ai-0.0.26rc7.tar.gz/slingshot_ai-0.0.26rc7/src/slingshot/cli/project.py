from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.table import Table

from slingshot import schemas

from ..sdk.config import client_settings, project_config
from ..sdk.errors import SlingshotFileNotFoundException, SlingshotUnauthenticatedError
from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from ..shared.config import load_slingshot_project_config
from ..shared.utils import get_data_or_raise
from .config.slingshot_cli import SlingshotCLIApp
from .shared import create_empty_project_manifest, prompt_for_single_choice

app = SlingshotCLIApp()


@app.command("details", requires_project=True, hidden=True)
async def project_details(sdk: SlingshotSDK) -> None:
    """Prints the details of the current project."""
    assert sdk.project, "Project should be set"
    display_name = sdk.project.display_name
    project_id = sdk.project.project_id
    console.print(f"Project ID: [bold]{project_id}[/bold]")
    console.print(f"Display name: [bold]{display_name}[/bold]")
    console.print(f"(via {client_settings.slingshot_config_path.parent}")


@app.command("list", requires_auth=True)
async def list_projects(sdk: SlingshotSDK) -> None:
    """Lists all projects that the current user has access to."""
    projects = await sdk.list_projects()
    table = Table(title="Projects")
    table.add_column("Name", style="cyan")
    table.add_column("Project ID", style="cyan")
    for i, project in enumerate(projects):
        table.add_row(project.display_name, project.project_id)
    console.print(table)


@app.command("open", requires_project=True)
async def open_project(sdk: SlingshotSDK) -> None:
    """
    Opens the project in your default browser.
    """
    url = await sdk.web_path_util.project()
    console.print(f"Opening project in browser: [link={url}]{url}[/link]")
    typer.launch(url)


@app.command("fork")
async def fork_project(project_id: Optional[str] = typer.Argument(None), *, sdk: SlingshotSDK) -> None:
    """
    Forks the current project and opens it in your default browser.
    """
    if not project_id:
        # TODO: make selector if unset
        assert sdk.project, "Project should be set or project_id should be passed as an argument"
        project_id = sdk.project.project_id

    new_project_id_resp = await sdk._api.fork_project(project_id)  # TODO: add flow like in slingshot init
    new_project_id = get_data_or_raise(new_project_id_resp).project_id
    url = await sdk.web_path_util.project(new_project_id)
    console.print(f"Opening project in browser: [link={url}]{url}[/link]")
    typer.launch(url)


@app.command("use", requires_auth=True, requires_project=False, top_level=True)
async def set_tracked_project(project_id: Optional[str] = typer.Argument(None), *, sdk: SlingshotSDK) -> None:
    """
    Select which project to use for the current directory.
    """
    if project_id:
        await _set_project_id(sdk, project_id)
    else:
        await list_and_set_project_id(sdk)


async def list_and_set_project_id(sdk_: SlingshotSDK) -> None:
    me = await sdk_.me()
    if not me:
        raise SlingshotUnauthenticatedError()
    projects = me.projects
    if not projects:
        console.print("No projects found.")
        return  # Can't set a project ID if user has no projects
    choice = prompt_for_single_choice(
        f"Select the project you want to work on", [i.project_id for i in projects], skip_if_one_value=False
    )

    project_id = projects[choice].project_id
    await _set_project_id(sdk_, project_id)


async def _set_project_id(sdk_: SlingshotSDK, project_id: str) -> None:
    old_project_id = project_config.project_id
    project_config.project_id = project_id
    current_project_config = _try_load_slingshot_project_config()
    if old_project_id != project_id:
        project_config.last_pushed_manifest = None

    config_file = project_config.model_config.get('config_file')
    assert isinstance(config_file, Path)
    directory = config_file.parent.parent

    console.print(f"This directory ({directory}) is now associated with the project: [bold]{project_id}[/bold]")
    await sdk_.use_project(project_id)

    if current_project_config is None:
        console.print("No 'slingshot.yaml' file found -- initializing one from the remote project manifest...")
        create_empty_project_manifest(client_settings.slingshot_config_path)
        await sdk_.pull_remote_changes(force=True)
        console.print("Done.")


def _try_load_slingshot_project_config() -> schemas.ProjectManifest | None:
    try:
        return load_slingshot_project_config()
    except SlingshotFileNotFoundException:
        return None
