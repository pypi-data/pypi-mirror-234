from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from slingshot.sdk import SlingshotSDK

from .config.slingshot_cli import SlingshotCLIApp
from .shared import datetime_to_human_readable

app = SlingshotCLIApp()
console: Console = Console()


@app.command("create", requires_project=True)
async def create(
    volume_name: str = typer.Argument(None, help="The name of the new volume"), *, sdk: SlingshotSDK
) -> None:
    await sdk.create_volume(volume_name)
    console.print(f"Volume created successfully -- [green]{volume_name}[/green]")


@app.command("list", requires_project=True)
async def list_volumes(sdk: SlingshotSDK) -> None:
    volumes = await sdk.list_volumes()
    volumes.sort(key=lambda s: s.created_at, reverse=True)

    table = Table(title="Volumes")
    table.add_column("Volume Name", style="cyan")
    table.add_column("Created At", style="cyan")

    for volume in volumes:
        table.add_row(volume.volume_name, datetime_to_human_readable(volume.created_at))
    console.print(table)


@app.command("delete", requires_project=True)
async def delete(
    volume_name: str = typer.Argument(None, help="The name of the volume to be deleted"), *, sdk: SlingshotSDK
) -> None:
    await sdk.delete_volume(volume_name)

    console.print(f"Volume deleted successfully -- [green]{volume_name}[/green]")
