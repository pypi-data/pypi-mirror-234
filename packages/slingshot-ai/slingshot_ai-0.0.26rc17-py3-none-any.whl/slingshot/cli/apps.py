from __future__ import annotations

from typing import Optional

import typer
from rich.table import Table

from .. import schemas
from ..sdk.errors import SlingshotException
from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from ..shared.config import load_slingshot_project_config
from .config.slingshot_cli import SlingshotCLIApp
from .shared import (
    component_spec_id_by_name_or_prompt,
    filter_for_apps,
    filter_for_running_apps,
    filter_for_sessions,
    follow_app_logs_until_ready,
    get_default_source_mappings,
    prompt_for_app_spec,
    prompt_push_code,
)
from .shared.code_sync import start_code_sync
from .shared.ssh import ensure_user_is_configured_for_ssh

app = SlingshotCLIApp()


@app.command("start", requires_project=True)
async def start_app(
    *,
    sdk: SlingshotSDK,
    name: Optional[str] = typer.Argument(None, help="App name"),
    sessions: bool = typer.Option(False, "--sessions", "-s", help="Only show sessions"),
) -> str:
    """Start a Slingshot app"""
    applied = await sdk.apply_project()
    source_code_id = await prompt_push_code(sdk)

    if not name:
        filter_fn = filter_for_sessions if sessions else filter_for_apps
        id_and_name_or_none = await prompt_for_app_spec(
            sdk, filter_fn, app_display_name='session' if sessions else 'app', raise_if_missing=True
        )
        if id_and_name_or_none:
            _, name = id_and_name_or_none
        else:
            raise typer.Exit(1)

    assert sdk.project
    component_spec = await sdk.api.get_component_spec_by_name(name, sdk.project.project_id)
    if not component_spec:
        raise SlingshotException(f"No run found with the name '{name}'")

    app_instance = await sdk.start_app(app_name=name, source_code_id=source_code_id)
    url = await sdk.web_path_util.app(component_spec=app_instance.spec_id)
    console.print(f"Starting app '{name}'. See details here: {url}")

    console.print(f"Following logs. Ctrl-C to stop, and run 'slingshot app logs {name} --follow' to follow again")
    status = await follow_app_logs_until_ready(sdk, app_instance.spec_id)
    if status == schemas.ComponentInstanceStatus.ERROR:
        raise SlingshotException(f"App failed to start. Try again or contact support for help.")

    if status.is_ready:
        refreshed_app_spec = await sdk.get_app(name)
        assert refreshed_app_spec is not None, "App does not exist anymore"

        console.print(f"[green]App '{name}' started successfully[/green].")
        if refreshed_app_spec.app_instance_url:
            console.print(f"App will be available at {refreshed_app_spec.app_instance_url}")
            console.print(f"Open the URL with [blue]slingshot app open {name}[/blue]")
        return name

    console.print(f"App stopped with status {status}")
    return name


@app.command("stop", requires_project=True)
async def stop_app(*, sdk: SlingshotSDK, name: Optional[str] = typer.Argument(None, help="App name")) -> None:
    """Stop a Slingshot app"""
    if not name:
        _, name = await prompt_for_app_spec(
            sdk, filter_for_apps, filter_for_running_apps, app_display_name="app", skip_if_one_value=False
        )
    await sdk.stop_app(app_name=name)
    console.print(f"[green]App '{name}' stopped successfully[/green].")


@app.command(name="logs", requires_project=True)
async def app_logs(
    name: Optional[str] = typer.Argument(None, help="App name"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow logs"),
    refresh_rate: float = typer.Option(3.0, "--refresh-rate", "-r", help="Refresh rate in seconds"),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Get logs for a Slingshot app."""
    spec_id = await component_spec_id_by_name_or_prompt(sdk, name)
    await sdk.print_logs(spec_id=spec_id, follow=follow, refresh_rate_s=refresh_rate)


@app.command("open", requires_project=True)
async def open_app(*, sdk: SlingshotSDK, name: Optional[str] = typer.Argument(None, help="App name")) -> None:
    """Open a Slingshot app in your browser"""
    spec_id = await component_spec_id_by_name_or_prompt(sdk, name)
    app_instance = await sdk.api.get_latest_app_instance_for_app_spec(spec_id=spec_id)
    if app_instance is None or not app_instance.app_instance_url:
        console.print(f"[red]No URL found for app[/red]")
        return

    console.print(f"[green]Opening {app_instance.app_instance_url}[/green]")
    typer.launch(app_instance.app_instance_url)


@app.command("list", requires_project=True)
async def list_apps(*, sdk: SlingshotSDK) -> None:
    """List all Slingshot apps as a table"""
    app_specs = await sdk.list_components()
    app_specs = [spec for spec in app_specs if spec.component_type == schemas.ComponentType.APP]
    if not app_specs:
        console.print(
            "No apps found! Edit [yellow]slingshot.yaml[/yellow] or use [yellow]slingshot add[/yellow] to add one."
        )
        return

    table = Table(title="Apps")
    table.add_column("App Name", style="cyan")
    table.add_column("Status", style="cyan")
    table.add_column("Environment", style="cyan")
    table.add_column("URL", style="cyan")
    for component_spec in app_specs:
        env_spec = component_spec.execution_environment_spec
        env_name = env_spec.execution_environment_spec_name if env_spec else '-'
        row = [component_spec.spec_name, component_spec.app_instance_status, env_name, component_spec.app_instance_url]
        table.add_row(*row)
    console.print(table)


@app.command("sync", requires_project=True, hidden=True)
async def sync_app(
    name: Optional[str] = typer.Argument(None, help="App name."),
    sessions: bool = typer.Option(False, "--sessions", "-s", help="Only show sessions"),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Sync a local directory with an app"""
    project = load_slingshot_project_config()
    await ensure_user_is_configured_for_ssh(sdk)
    if not name:
        if sessions:
            _, name = await prompt_for_app_spec(sdk, filter_for_sessions, app_display_name='session')
        else:
            _, name = await prompt_for_app_spec(sdk, filter_for_apps, app_display_name='app')

    component_spec = await sdk.get_app(name)
    if not component_spec:
        raise SlingshotException(f"{'Session' if sessions else 'App'} '{name}' not found")

    # TODO: Inform the user of how sync works for app, e.g. we'll copy the files, but it's up to them to actually do
    #   something with updated files (hot reloading, reloading config, restarting processes, etc)
    await start_code_sync(
        project.sources if project.sources else get_default_source_mappings(), component_spec, sdk=sdk
    )
