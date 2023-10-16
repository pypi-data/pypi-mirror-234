from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from slingshot.sdk import SlingshotSDK
from slingshot.sdk.config import client_settings, global_config

from .. import schemas
from ..sdk.errors import SlingshotException
from ..sdk.utils import console
from . import project
from .config.slingshot_cli import SlingshotCLIApp
from .shared import prompt_confirm, prompt_for_single_choice

app = SlingshotCLIApp()


@app.command("login", requires_auth=False, requires_project=False, top_level=True)
async def login(sdk: SlingshotSDK, api_key: Optional[str] = typer.Argument(None, envvar="SLINGSHOT_API_KEY")) -> None:
    """Login to Slingshot

    This command will open a browser window to authenticate you with Slingshot"""

    # TODO: Move all of this logic to the SDK
    if api_key:
        console.print("Logging in with API key...")
        service_account_token_response = await sdk.api.sa_login(api_key=api_key)
        auth_token = schemas.AuthTokenUnion.from_service_account_token(service_account_token_response)
        global_config.auth_token = auth_token
        console.print("Logged in successfully!")
        return

    await sdk.login()

    me = await sdk.me()
    if not me:
        raise SlingshotException("Could not get user info after login")

    user = me.user
    if not user:
        raise SlingshotException("Unexpected response from server")

    console.print(f"Logged in successfully as {user.username}!")
    if not user.ssh_public_key:
        console.print(
            "You don't have an SSH public key set. You can set one by running 'slingshot auth set-ssh'", style="yellow"
        )

    await sdk.setup()

    console.print(f"Using local project at {client_settings.project_config_folder}")

    if sdk.project_id and any(p.project_id == sdk.project_id for p in user.projects):
        await sdk.use_project(sdk.project_id)
        console.print(f"Project is set to '{sdk.project_id}'.")
        return

    choice = prompt_confirm(f"Do you want to track an existing project?", default=False)
    if choice:
        await project.list_and_set_project_id(sdk)
    else:
        console.print("You can run `slingshot open` to create a new project from the UI")


@app.command("logout", requires_auth=False, requires_project=False, top_level=True)
async def logout(sdk: SlingshotSDK) -> None:
    """Log out of Slingshot"""
    sdk.logout()
    console.print("Logged out successfully")


@app.command("set-ssh", requires_auth=True, requires_project=False, top_level=True)
async def set_ssh_public_key(
    sdk: SlingshotSDK, filename: Optional[str] = typer.Argument(None, help="Path to the SSH public key file")
) -> None:
    """Set the SSH public key for the logged-in user

    Provide the path to the SSH public key file. If no path is provided, the default location
    will be used (usually ~/.ssh)."""

    await _set_ssh_public_key(sdk, filename)


async def set_ssh_public_key_if_not_set(sdk: SlingshotSDK) -> None:
    """Set the SSH public key for the logged-in user if it's not set"""
    me = await sdk.me()
    if not (user := me and me.user):
        return None
    if not user.ssh_public_key:
        console.print(
            "You don't have an SSH public key set. Without it you won't be able to use sync or remote access."
        )
        choice = prompt_confirm("Do you want to set SHH public key", default=True)
        if choice:
            await _set_ssh_public_key(sdk, filename=None)
        else:
            console.print("Set a public key by running `slingshot auth set-ssh <key.pub>`", style="yellow")


async def _set_ssh_public_key(sdk: SlingshotSDK, filename: str | None) -> None:
    """Set the SSH public key for the logged-in user"""
    me = await sdk.me()
    if not me or not me.user:
        raise SlingshotException("Must be signed in as a user to set SSH public key")
    user = me.user
    if user.ssh_public_key:
        console.print(f"[yellow]Warning[/yellow]: You already have SSH public key set to: {user.ssh_public_key}")
        choice = prompt_confirm("This will overwrite your existing key. Do you want to continue?", default=False)
        if not choice:
            return

    if not filename:
        # Try to infer the public key
        ssh_dir = Path.home() / ".ssh"
        if not ssh_dir.exists() or not (pub_key_files := list(ssh_dir.glob("*.pub"))):
            raise SlingshotException(
                "Could not infer a public key. If none exist, you can create one with "
                "'ssh-keygen -t ed25519 -C \"your_email@example.com\".'\n"
                "Or specify a path to your public key by running 'slingshot auth set-ssh <path/to/key.pub>'"
            )
        i = prompt_for_single_choice(
            "Found public key files. Which one do you want to use?",
            [str(f) for f in pub_key_files],
            skip_if_one_value=True,
        )
        filename = str(pub_key_files[i])

    if not filename.endswith(".pub"):
        raise typer.BadParameter("SSH public key file must end with .pub")

    with open(filename) as f:
        key = f.read()

    await sdk.set_ssh(key)

    # Strip .pub to get to the name of the private key, safe as we're already confirmed ending in .pub
    private_key_filename = filename[: -len(".pub")]
    console.print(
        f"[green]Success[/green]: SSH public key has been set to {key}\n"
        f"Note: Please make sure your SSH key is added to the SSH agent. You can do this by running "
        + f"'ssh-add {private_key_filename}'\n"
        + f"[yellow]Warning[/yellow]: Sessions that have already started won't get the updated key."
    )
