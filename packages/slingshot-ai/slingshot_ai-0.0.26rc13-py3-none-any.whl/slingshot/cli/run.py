from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, Optional

import typer
from rich.table import Table

from .. import schemas
from ..schemas import remote_mount_spec_to_local
from ..sdk.errors import SlingshotException
from ..sdk.graphql.fragments import MountSpec
from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from .config.slingshot_cli import SlingshotCLIApp
from .shared import (
    filter_for_runs,
    follow_run_logs_until_done,
    get_hyperparameter_config_from_file,
    parse_extra_args,
    prompt_for_app_spec,
    prompt_push_code,
    run_by_name_or_prompt,
    seconds_to_human_readable,
)
from .shared.ssh import ensure_user_is_configured_for_ssh, start_ssh_for_run

app = SlingshotCLIApp()


@app.command(
    "start",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    requires_auth=True,
    requires_project=True,
)
async def start_run(
    ctx: typer.Context,
    *,
    sdk: SlingshotSDK,
    name: Optional[str] = typer.Argument(None, help="Name of the run template to use."),
    config_file: Optional[str] = typer.Option(None, "--config", "-C", help="Path to config file for run."),
    debug: bool = typer.Option(False, "--debug", "-d", help="Run in debug mode.", hidden=True),
) -> None:
    """Start a run"""
    if debug:
        console.log("Debug mode enabled.")

    await sdk.apply_project()
    source_code_id = await prompt_push_code(sdk)

    cli_args = parse_extra_args(ctx.args)
    config = await get_hyperparameter_config_from_file(Path(config_file)) if config_file else {}
    config = {**config, **cli_args}

    if not name:
        _, name = await prompt_for_app_spec(sdk, filter_for_runs, app_display_name="run")

    assert sdk.project
    run_spec = await sdk.api.get_component_spec_by_name(name, sdk.project.project_id)
    if not run_spec:
        raise SlingshotException(f"No run found with the name '{name}'")

    new_run = await sdk.start_run(run_template_name=name, source_code_id=source_code_id, hyperparameters=config)
    link = await sdk.web_path_util.run(new_run)
    console.print(f"Run created with name '{new_run.run_name}', view in browser at {link}")
    console.print(
        f"Following logs. Ctrl-C to stop, and run 'slingshot run logs {new_run.run_name} --follow' to follow again"
    )
    await follow_run_logs_until_done(sdk, run_id=new_run.run_id)


@app.command("continue", requires_project=True)
async def continue_run(name: Optional[str] = typer.Argument(None, help="Run name"), *, sdk: SlingshotSDK) -> None:
    """Continue a run"""
    run = await run_by_name_or_prompt(
        sdk,
        name=name,
        allowed_status={
            schemas.ComponentInstanceStatus.COMPLETED,
            schemas.ComponentInstanceStatus.ERROR,
            schemas.ComponentInstanceStatus.STOPPED,
        },
        error_message='No terminated runs found to continue from',
    )
    run_specs = await sdk.list_run_templates()
    reference_run_spec = next((run_spec for run_spec in run_specs if run_spec.spec_id == run.spec_id), None)
    if not reference_run_spec:
        raise SlingshotException(f"Could not find template for run {run.run_name}")

    # We only allow one mount per (path, mode) combo to avoid collisions
    reference_mounts: dict[tuple[str, str], MountSpec] = {
        (mount_spec.path, mount_spec.mode): mount_spec for mount_spec in reference_run_spec.mount_specs
    }
    restored_run_mounts: dict[tuple[str, Literal["DOWNLOAD"]], MountSpec] = {
        (mount.mount_path, "DOWNLOAD"): MountSpec(
            path=mount.mount_path, mode="DOWNLOAD", name=mount.uploaded_blob_artifact.name, tag=None
        )
        for mount in run.mounts
        if mount.mount_mode == "UPLOAD" and mount.uploaded_blob_artifact
    }

    console.print(
        f"Restoring {len(restored_run_mounts)} mounts from previous run: {list(restored_run_mounts.values())}"
    )
    all_mounts_: dict[Any, MountSpec] = {**reference_mounts, **restored_run_mounts}  # Restored mounts take priority
    all_mounts: list[MountSpec] = list(all_mounts_.values())
    console.print(f"Run will start with {len(all_mounts)} mounts: {all_mounts}")
    hyperparameters: dict[str, Any] | None = None
    if run.hyperparameters:
        hyperparameters = json.loads(run.hyperparameters)

    new_run = await sdk.start_run(
        run_template_name=reference_run_spec.spec_name,
        machine_size=schemas.MachineSize(run.machine_size),
        hyperparameters=hyperparameters,
        cmd=run.cmd,
        mount_specs=[remote_mount_spec_to_local(mount) for mount in all_mounts],
        environment_instance_id=run.environment_instance.environment_instance_id,
    )

    assert sdk.project
    link = await sdk.web_path_util.run(new_run)
    console.print(f"Run created with name '{new_run.run_name}', view in browser at {link}")
    console.print(
        f"Following logs. Ctrl-C to stop, and run 'slingshot run logs {new_run.run_name} --follow' to follow again"
    )
    await follow_run_logs_until_done(sdk=sdk, run_id=new_run.run_id)


@app.command("stop", requires_project=True)
async def stop_run(name: Optional[str] = typer.Argument(None, help="Run name"), *, sdk: SlingshotSDK) -> None:
    """Stop a run"""
    run = await run_by_name_or_prompt(
        sdk,
        name=name,
        allowed_status=set(schemas.ComponentInstanceStatus.active_statuses()),
        error_message='No active runs found to stop',
        skip_if_one_value=False,
    )
    await sdk.stop_run(run_name=run.run_name)
    console.print("Run stopped successfully!")


@app.command(name="logs", requires_project=True)
async def run_logs(
    name: Optional[str] = typer.Argument(None, help="Run name"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow logs"),
    refresh_rate: float = typer.Option(3.0, "--refresh-rate", "-r", help="Refresh rate in seconds"),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Get logs for a run."""
    run = await run_by_name_or_prompt(sdk, name=name)
    await sdk.print_logs(run_id=run.run_id, follow=follow, refresh_rate_s=refresh_rate)


@app.command("open", requires_project=True)
async def open_run(name: Optional[str] = typer.Argument(None, help="Run name"), *, sdk: SlingshotSDK) -> None:
    """Open a run in the browser."""
    run = await run_by_name_or_prompt(sdk, name=name)
    assert sdk.project
    link = await sdk.web_path_util.run(run)
    console.print(f"[green]Opening {link}[/green]")
    typer.launch(link)


@app.command("list", requires_project=True)
async def list_runs(sdk: SlingshotSDK) -> None:
    """List all runs in the project."""
    runs = await sdk.list_runs()
    if not runs:
        run_templates = await sdk.list_run_templates()
        if not run_templates:
            console.print(
                "No runs found! "
                "Edit [yellow]slingshot.yaml[/yellow] or use [yellow]slingshot add[/yellow] to add a run template."
            )
            return
        console.print("No runs found! Use [yellow]slingshot run start[/yellow] to start a run.")
        console.print("Available run templates:")
        console.print("\n".join(f"    - [cyan]{run_template.spec_name}[/cyan]" for run_template in run_templates))
        return

    table = Table(title="Runs")
    table.add_column("Run Name", style="cyan")
    table.add_column("Status", style="cyan")
    table.add_column("Environment", style="cyan")
    table.add_column("Source Code", style="cyan")
    table.add_column("Machine Size", style="cyan")
    table.add_column("Duration", style="cyan")
    for run in runs:
        duration_seconds = None
        if run.start_time and not run.end_time:
            duration_seconds = (datetime.utcnow() - run.start_time).total_seconds()
        elif run.start_time and run.end_time:
            duration_seconds = (run.end_time - run.start_time).total_seconds()

        row = [
            run.run_name,
            run.run_status,
            run.environment_instance.execution_environment_spec.execution_environment_spec_name,
            run.source_code.blob_artifact.name,
            run.machine_size,
            f"{seconds_to_human_readable(duration_seconds)}" if duration_seconds is not None else "N/A",
        ]
        table.add_row(*row)
    console.print(table)


@app.command("enter", requires_auth=True, requires_project=True, hidden=True)
async def enter_run(
    *, sdk: SlingshotSDK, name: Optional[str] = typer.Argument(None, help="Name of the run use.")
) -> None:
    """Enters the environment of an active run by SSH:ing into it."""

    await ensure_user_is_configured_for_ssh(sdk)
    run = await run_by_name_or_prompt(
        sdk,
        name=name,
        allowed_status={schemas.ComponentInstanceStatus.RUNNING},
        error_message='No active runs found to enter',
    )

    ssh_connection_details = await start_ssh_for_run(run, sdk=sdk)
    console.print(
        f"Connecting to {ssh_connection_details.username}@{ssh_connection_details.hostname}:{ssh_connection_details.port}"
    )
    ssh_cmd = (
        f"ssh {ssh_connection_details.username}@{ssh_connection_details.hostname} -p {ssh_connection_details.port}"
    )
    subprocess.run(ssh_cmd, shell=True)
