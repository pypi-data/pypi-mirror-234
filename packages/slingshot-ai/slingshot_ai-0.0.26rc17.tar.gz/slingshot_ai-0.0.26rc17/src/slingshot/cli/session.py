from __future__ import annotations

from logging import getLogger
from pathlib import Path
from typing import Optional

import sh  # type: ignore
import typer

from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from ..shared.config import load_slingshot_project_config
from .apps import start_app, sync_app
from .config.slingshot_cli import SlingshotCLIApp
from .shared import filter_for_running_apps, filter_for_sessions, get_default_source_mappings, prompt_for_app_spec
from .shared.code_sync import start_code_sync
from .shared.ssh import ensure_user_is_configured_for_ssh

app = SlingshotCLIApp()
logger = getLogger(__name__)


@app.command(requires_project=True)
async def start(
    name: Optional[str] = typer.Argument(None, help="Session name."),
    do_sync: bool = typer.Option(False, "--sync", "-s"),
    sync_path: Optional[Path] = typer.Option(None, "--sync-path", "-p"),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Start a session app"""
    if sync_path and not do_sync:
        do_sync = True
    if do_sync:
        await ensure_user_is_configured_for_ssh(sdk)

    project = load_slingshot_project_config()
    start_app_name: str = await start_app.function(sdk=sdk, name=name, sessions=True)
    component_spec = await sdk.get_app(start_app_name)
    assert component_spec, "Session app should exist"

    if do_sync:
        sync_path = sync_path or Path.cwd()
        maybe_create_session_notebook(sync_path)
        await start_code_sync(project.sources or get_default_source_mappings(), component_spec, sdk=sdk)
    else:
        console.print(f"To sync code to this session, run 'slingshot session sync {start_app_name}'")


@app.command(requires_project=True)
async def sync(name: Optional[str] = typer.Argument(None, help="Session name."), *, sdk: SlingshotSDK) -> None:
    """Sync a local directory with a session, alias for slingshot app sync --sessions"""
    await sync_app.function(name, True, sdk=sdk)


@app.command(requires_project=True)
async def stop(name: Optional[str] = typer.Argument(None, help="Session name."), *, sdk: SlingshotSDK) -> None:
    """Stop a session app"""
    if not name:
        _, name = await prompt_for_app_spec(
            sdk, filter_for_sessions, filter_for_running_apps, app_display_name="session", skip_if_one_value=False
        )
    await sdk.stop_app(app_name=name)
    console.print(f"[green]Session '{name}' stopped successfully[/green].")


def maybe_create_session_notebook(sync_path: Path) -> None:
    # Create sync_path if it doesn't exist
    sync_path.mkdir(parents=True, exist_ok=True)
    # Let's create a session.ipynb if there isn't any notebook in sync_path]
    if not any(sync_path.glob("*.ipynb")):
        console.print("Creating session.ipynb")
        with open(sync_path / "session.ipynb", "w") as f:
            f.write(SESSION_DEFAULT_NOTEBOOK)


SESSION_DEFAULT_NOTEBOOK = """{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f3d39bea-de51-48a4-adde-0af77fafb211",
   "metadata": {},
   "outputs": [],
   "source": [
    "%load_ext autoreload\\n",
    "%autoreload 2"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}"""
