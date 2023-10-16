from __future__ import annotations

import typer

from slingshot.cli.config.slingshot_cli import SlingshotCLIApp
from slingshot.sdk.slingshot_sdk import SlingshotSDK
from slingshot.sdk.utils import console

app = SlingshotCLIApp()


@app.command(name="apply", requires_project=True, top_level=True, requires_auth=True)
async def apply(
    *,
    sdk: SlingshotSDK,
    force: bool = typer.Option(
        False, "--force", "-f", help="Ignore conflicts and apply the local version to the remote"
    ),
) -> None:
    """Apply the local slingshot.yaml file for the current project by updating the remote."""
    any_changes = await sdk.apply_project(force=force)
    if not any_changes:
        console.print("[cyan]No changes pushed[/cyan]")


@app.command(name="pull", requires_project=True, top_level=True, requires_auth=True)
async def pull(
    *,
    sdk: SlingshotSDK,
    force: bool = typer.Option(False, "--force", "-f", help="Ignore conflicts and apply remote changes to local"),
) -> None:
    """Pull remote changes to the current local slingshot YAML file."""
    any_changes_pulled = await sdk.pull_remote_changes(force=force)
    if not any_changes_pulled:
        console.print("[cyan]No remote changes to pull[cyan]")
