from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console

from slingshot.sdk import SlingshotSDK

from .config.slingshot_cli import SlingshotCLIApp
from .shared import prompt_confirm

app = SlingshotCLIApp()
console: Console = Console()

OPENAI_API_KEY_NAME = "OPENAI_API_KEY"


@app.command("list", requires_project=True)
async def list_secrets(*, sdk: SlingshotSDK) -> None:
    """Lists all secrets in the current project."""
    resp = await sdk.list_secrets()
    if not resp:
        console.print("[yellow]No secrets found[/yellow]")
        return

    secrets_formatted = '\n'.join(['  [green]-[/green] ' + secret.secret_name for secret in resp])
    console.print(
        f"These secrets are set in this project, and will be injected into training runs, deployments, and sessions:\n"
        f"{secrets_formatted}"
    )


@app.command("put", requires_project=True)
async def put(
    secret_name: Optional[str] = typer.Argument(None),
    secret_value: Optional[str] = typer.Argument(None),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Sets a secret in the current project."""
    secret_name_ = secret_name or typer.prompt("Secret name")
    secret_value_ = secret_value or typer.prompt("Secret value", hide_input=True)
    secret = await sdk.create_secret(secret_name=secret_name_, secret_value=secret_value_)
    console.print(f"[green]Secret {secret.secret_name} put successfully[/green]")


@app.command("wandb", requires_project=True)
async def put_wandb_creds(sdk: SlingshotSDK) -> None:
    """Sets the W&B API key for the current project."""
    names_resp = [i.secret_name for i in await sdk.list_secrets()]
    if "WANDB_API_KEY" in names_resp:
        console.print("[yellow]W&B API key already set for this project[/yellow]")
        y = prompt_confirm("Do you want to overwrite it?", default=True)
        if not y:
            return
    s = (
        "wandb: You can find your API key in your browser here: https://wandb.ai/authorize\n"
        "Paste an API key from your profile and hit enter"
    )
    api_key = typer.prompt(s, hide_input=True)
    secret = await sdk.create_secret(secret_name="WANDB_API_KEY", secret_value=api_key)
    console.print(f"[green]Secret {secret.secret_name} put successfully[/green]")


@app.command("openai", requires_project=True)
async def put_openai_creds(sdk: SlingshotSDK) -> None:
    """Sets the OpenAI API key for the current project."""
    names_resp = [i.secret_name for i in await sdk.list_secrets()]
    if OPENAI_API_KEY_NAME in names_resp:
        console.print("[yellow]OpenAI API key already set for this project[/yellow]")
        y = prompt_confirm("Do you want to overwrite it?", default=True)
        if not y:
            return
    s = (
        "OpenAI: You can find your API key in your browser here: https://beta.openai.com/account/api-keys\n"
        "Paste an API key from your profile and hit enter"
    )
    api_key = typer.prompt(s, hide_input=True)
    secret = await sdk.create_secret(secret_name=OPENAI_API_KEY_NAME, secret_value=api_key)
    console.print(f"[green]Secret {secret.secret_name} put successfully[/green]")


@app.command("delete", requires_project=True)
async def delete(secret_name: str, *, sdk: SlingshotSDK) -> None:
    """Deletes a secret in the current project."""
    deleted = await sdk.delete_secret(secret_name=secret_name)
    if not deleted:
        console.print(f"[red]Secret {secret_name} not found[/red]")
    else:
        console.print(f"[yellow]Secret {secret_name} deleted[/yellow]")
