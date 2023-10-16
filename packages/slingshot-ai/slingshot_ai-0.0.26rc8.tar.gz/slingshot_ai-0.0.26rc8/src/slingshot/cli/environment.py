from __future__ import annotations

from rich.table import Table

from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from .config.slingshot_cli import SlingshotCLIApp

app = SlingshotCLIApp()


@app.command("list", requires_project=True)
async def list_environments(sdk: SlingshotSDK) -> None:
    """List all environments in the project."""
    envs = await sdk.list_environments()
    if not envs:
        console.print(
            "No environments found!"
            "Edit [yellow]slingshot.yaml[/yellow] or use [yellow]slingshot add[/yellow] to add an environment template."
        )
        return

    table = Table(title="Environments")
    table.add_column("Environment Name", style="cyan")
    table.add_column("CPU Build Status", style="cyan")
    table.add_column("GPU Build Status", style="cyan")

    for env_spec in envs:
        assert env_spec.environment_instances, "Environment spec should have at least one instance"
        latest_env_instance = env_spec.environment_instances[0]
        cpu_build = latest_env_instance.cpu_build
        gpu_build = latest_env_instance.gpu_build
        row = [
            env_spec.execution_environment_spec_name,
            cpu_build.build_status if cpu_build else "-",
            gpu_build.build_status if gpu_build else "-",
        ]
        table.add_row(*row)
    console.print(table)
