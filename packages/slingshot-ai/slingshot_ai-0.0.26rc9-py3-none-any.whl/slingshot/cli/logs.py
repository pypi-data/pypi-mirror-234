from __future__ import annotations

from datetime import datetime

import typer

from .. import schemas
from ..sdk.graphql import fragments
from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from .config.slingshot_cli import SlingshotCLIApp
from .shared import datetime_to_human_readable, prompt_for_single_choice

app = SlingshotCLIApp()


@app.command(name="logs", requires_project=True)
async def logs(
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow logs"),
    refresh_rate: float = typer.Option(3.0, "--refresh-rate", "-r", help="Refresh rate in seconds"),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Get logs for all active Slingshot apps/runs/deployments"""
    spec_id = None
    run_id = None

    # List all active apps, runs, and deployments
    app_deployment_specs = await sdk.list_components()
    runs = await sdk.list_runs()

    app_deployment_specs_expanded: list[tuple[fragments.ComponentSpec, datetime, str]] = [
        (component_spec, component_spec.last_created_at, component_spec.component_type)
        for component_spec in app_deployment_specs
        if component_spec.last_created_at is not None and component_spec.component_type != schemas.ComponentType.RUN
    ]
    runs_expanded: list[tuple[fragments.Run, datetime, str]] = [
        (run, run.created_at, schemas.ComponentType.RUN) for run in runs
    ]

    # Note: this is on multiple lines for typing purposes
    all_specs_runs: list[tuple[fragments.ComponentSpec | fragments.Run, datetime, str]] = [
        *app_deployment_specs_expanded
    ]
    all_specs_runs.extend(runs_expanded)

    # Sort by created_at descending
    all_specs_runs.sort(key=lambda x: x[1], reverse=True)

    if len(all_specs_runs) == 0:
        console.print("No active apps, runs, or deployments found", style="yellow")
        return

    idx = prompt_for_single_choice(
        "Select an app, run, or deployment",
        [_app_spec_or_run_tuple_to_prompt_name(app_spec_or_run) for app_spec_or_run in all_specs_runs],
    )
    selected_spec_or_run = all_specs_runs[idx]
    if isinstance(selected_spec_or_run[0], fragments.ComponentSpec):
        spec_id = selected_spec_or_run[0].spec_id
    else:
        run_id = selected_spec_or_run[0].run_id

    if run_id:
        await sdk.print_logs(run_id=run_id, follow=follow, refresh_rate_s=refresh_rate)
    elif spec_id:
        await sdk.print_logs(spec_id=spec_id, follow=follow, refresh_rate_s=refresh_rate)


def _app_spec_or_run_tuple_to_prompt_name(
    app_spec_or_run_tuple: tuple[fragments.ComponentSpec | fragments.Run, datetime, str]
) -> str:
    app_spec_or_run, created_at, component_type = app_spec_or_run_tuple
    if isinstance(app_spec_or_run, fragments.ComponentSpec):
        if component_type == schemas.ComponentType.DEPLOYMENT:
            return f"deployment:{app_spec_or_run.spec_name} (Last started {datetime_to_human_readable(created_at)})"
        return f"app:{app_spec_or_run.spec_name} (Last started {datetime_to_human_readable(created_at)})"
    else:
        return f"run:{app_spec_or_run.run_name} (Created {datetime_to_human_readable(created_at)})"
