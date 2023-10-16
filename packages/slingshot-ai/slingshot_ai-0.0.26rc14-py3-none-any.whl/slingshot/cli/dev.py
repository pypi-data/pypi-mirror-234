from pathlib import Path
from typing import Optional

import typer

from slingshot.sdk.config import global_config

from .. import SlingshotSDK
from ..sdk.errors import SlingshotException
from ..sdk.utils import console
from ..shared.config import load_slingshot_project_config
from .config.slingshot_cli import SlingshotCLIApp
from .shared import prompt_for_single_choice

app = SlingshotCLIApp()


_options = ["local", "dev", "prod"]


@app.command(name="be", top_level=True, hidden=True)
async def set_backend_url(url: Optional[str] = typer.Argument(None)) -> None:
    """Set the backend URL"""
    if url is None:
        i = prompt_for_single_choice("Which backend do you want to use?", _options)
        url = _options[i]
    if url == "local":
        url = "http://localhost:8002"
    elif url == "dev":
        url = "https://dev.slingshot.xyz"
    elif url == "prod":
        url = "https://app.slingshot.xyz"
    else:
        url = url.rstrip("/")
    global_config.slingshot_backend_url = url
    console.print(f"Backend URL set to {url}")


@app.command(name="validate", top_level=True, hidden=True)
async def validate_yaml(
    config_file_path: Optional[Path] = typer.Argument(None, exists=True, resolve_path=True)
) -> None:
    """Validates the slingshot.yaml (or a file specified on the command line) without taking further action"""
    load_slingshot_project_config(config_file_path)
    console.print(f"Loaded slingshot.yaml without errors")


@app.command(name="fail", top_level=True, hidden=True)
async def force_error(non_slingshot_error: Optional[bool] = typer.Argument(None)) -> None:
    """Force an exception, to test things like Sentry local error reporting"""
    if non_slingshot_error:
        raise Exception("Something went horribly wrong (but on purpose)")
    else:
        raise SlingshotException("Something went horribly wrong (but on purpose)")


@app.command(name="rebuild-outdated-envs", top_level=True, hidden=True)
async def rebuild_outdated_envs(sdk: SlingshotSDK) -> None:
    """Invalidates builds for outdated environment instances that use old versions of Slingshot"""
    await sdk._api._rebuild_outdated_environments()
    console.print(f"Finished rebuilding outdated environments")
