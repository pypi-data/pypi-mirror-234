from __future__ import annotations

from typing import Optional

import typer

from .. import schemas
from ..sdk.slingshot_sdk import SlingshotSDK
from ..shared.config import load_slingshot_project_config
from .config.slingshot_cli import SlingshotCLIApp
from .shared import get_default_source_mappings

app = SlingshotCLIApp()


@app.command("push", requires_project=True, top_level=True)
async def push(
    description: Optional[str] = typer.Option(None, help="A short description of your code (for reference purposes)."),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Push a new version of your code to Slingshot by creating a new code artifact."""
    project = load_slingshot_project_config()
    await _prepare_and_push(project, sdk=sdk, description=description)
    await sdk.apply_project()


@app.command("prepare", requires_project=False)
async def package(*, sdk: SlingshotSDK) -> None:
    """Package up the source code that would normally be pushed to Slingshot in a local code.zip file."""
    project = load_slingshot_project_config()
    await _prepare_and_push(project, sdk=sdk, prepare_only=True)


async def _prepare_and_push(
    project: schemas.ProjectManifest,
    *,
    sdk: SlingshotSDK,
    description: Optional[str] = None,
    prepare_only: bool = False,
) -> None:
    source_mappings = project.sources if project.sources is not None else get_default_source_mappings()
    await sdk.push_code(
        source_mappings=source_mappings, description=description, prepare_only=prepare_only, and_print=True
    )
