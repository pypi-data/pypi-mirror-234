from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.table import Table

from ..sdk.errors import SlingshotException
from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from .config.slingshot_cli import SlingshotCLIApp
from .shared import (
    deployment_spec_id_by_name_or_prompt,
    filter_for_deployments,
    filter_for_running_deployments,
    prompt_for_app_spec,
    prompt_push_code,
)

app = SlingshotCLIApp()


@app.command(requires_project=True, top_level=True, no_args_is_help=True)
async def predict(
    input_path: Path = typer.Argument(
        ..., help="The path to the input file on which you wish to run inference", exists=True
    ),
    name: Optional[str] = typer.Option(None, "--deployment", "-d", help="Deployment name"),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Runs inference on a deployment"""
    if not name:
        _, name = await prompt_for_app_spec(sdk, filter_for_deployments, app_display_name="deployment")
    with open(input_path, "rb") as f:
        example_bytes = f.read()
    resp = await sdk.predict(deployment_name=name, example_bytes=example_bytes)
    console.print(resp)


@app.command("start", requires_project=True)
async def start_deployment(
    name: Optional[str] = typer.Argument(None, help="Deployment name"), *, sdk: SlingshotSDK
) -> None:
    """Deploys a model as an inference deployment"""
    await sdk.apply_project()
    source_code_id = await prompt_push_code(sdk)
    if not name:
        _, name = await prompt_for_app_spec(sdk, filter_for_deployments, app_display_name="deployment")

    assert sdk.project
    deployment_spec = await sdk.api.get_component_spec_by_name(name, sdk.project.project_id)
    if not deployment_spec:
        raise SlingshotException(f"No run found with the name '{name}'")

    deployment_spec = await sdk.start_deployment(deployment_name=name, source_code_id=source_code_id)
    url = await sdk.web_path_util.deployment(deployment_spec)
    console.print(f"[green]Deployment started successfully[/green]! " f"See details here: {url}")


@app.command("stop", requires_project=True)
async def stop_deployment(
    name: Optional[str] = typer.Argument(None, help="Deployment name"), *, sdk: SlingshotSDK
) -> None:
    """Undeploy an inference deployment"""
    if not name:
        _, name = await prompt_for_app_spec(
            sdk,
            filter_for_deployments,
            filter_for_running_deployments,
            app_display_name="deployment",
            skip_if_one_value=False,
        )
    await sdk.stop_deployment(deployment_name=name)
    console.print(f"[green]Deployment stopped successfully[/green]")


@app.command("logs", requires_project=True)
async def deployment_logs(
    name: Optional[str] = typer.Argument(None, help="Deployment name"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow logs"),
    refresh_rate: float = typer.Option(3.0, "--refresh-rate", "-r", help="Refresh rate in seconds"),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Get logs for a deployment."""
    deployment_spec_id = await deployment_spec_id_by_name_or_prompt(sdk, name)
    await sdk.print_logs(spec_id=deployment_spec_id, follow=follow, refresh_rate_s=refresh_rate)


@app.command("open", requires_project=True)
async def open_deployment(
    name: Optional[str] = typer.Argument(None, help="Deployment name"), *, sdk: SlingshotSDK
) -> None:
    """Opens the deployment page in your browser"""
    deployment_spec_id = await deployment_spec_id_by_name_or_prompt(sdk, name)
    link = await sdk.web_path_util.deployment(deployment_spec_id)
    console.print(f"[green]Opening {link}[/green]")
    typer.launch(link)


@app.command("list", requires_project=True)
async def list_deployments(*, sdk: SlingshotSDK) -> None:
    """List all deployments in the current project"""
    deployment_specs = await sdk.list_deployments()
    if not deployment_specs:
        "No deployments found! Edit [yellow]slingshot.yaml[/yellow] or use [yellow]slingshot add[/yellow] to add one."
        return

    table = Table(title="Deployments")
    table.add_column("Deployment Name", style="cyan")
    table.add_column("Status", style="cyan")
    table.add_column("Environment", style="cyan")
    table.add_column("Source Code", style="cyan")
    table.add_column("Machine Size", style="cyan")

    for deployment_spec in deployment_specs:
        source_code = (
            deployment_spec.deployments[0].source_code.blob_artifact.name if deployment_spec.deployments else "-"
        )
        env_spec = deployment_spec.execution_environment_spec
        env_name = env_spec.execution_environment_spec_name if env_spec else "-"
        row = [
            deployment_spec.spec_name,
            deployment_spec.deployment_status,
            env_name,
            source_code,
            deployment_spec.machine_size,
        ]
        table.add_row(*row)
    console.print(table)
