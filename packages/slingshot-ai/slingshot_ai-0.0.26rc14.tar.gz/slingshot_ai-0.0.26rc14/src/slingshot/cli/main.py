import typer

from slingshot.cli.config.slingshot_cli import SlingshotCLIApp
from slingshot.sdk.utils import console
from slingshot.slingshot_version import __version__

from ..sdk import slingshot_sdk
from . import (
    add,
    apply,
    apps,
    artifact,
    auth,
    code,
    deployment,
    dev,
    environment,
    logs,
    machine,
    project,
    run,
    secret,
    session,
    volume,
)

cli = SlingshotCLIApp(no_args_is_help=True, help=f"Slingshot AI CLI 🚀 ({__version__})")

cli.add_command(add.add_component)
cli.add_command(add.init)
cli.add_command(apply.apply)
cli.add_command(apply.pull)
cli.add_command(logs.logs)
cli.add_command(machine.list_machines)

cli.add_subcommands(auth.app, name="auth", help="Authenticate with Slingshot 👋", no_args_is_help=True)
cli.add_subcommands(artifact.app, name="artifact", help="Manage artifacts 💾", no_args_is_help=True)
cli.add_subcommands(code.app, name="code", help="Manage and push code 👩‍💻", no_args_is_help=True)
cli.add_subcommands(environment.app, name="environment", help="Manage environments 🌱", no_args_is_help=True)
cli.add_subcommands(project.app, name="project", help="Manage your Slingshot project 📊", no_args_is_help=True)
cli.add_subcommands(secret.app, name="secret", help="Create and manage secrets 🔐", no_args_is_help=True)
cli.add_subcommands(volume.app, name="volume", help="Create and manage volumes 📁", no_args_is_help=True, hidden=True)
cli.add_subcommands(run.app, name="run", help="Train ML models 🧠", no_args_is_help=True)
cli.add_subcommands(deployment.app, name="deployment", help="Deploy ML models for inference 🏃‍♀️", no_args_is_help=True)
cli.add_subcommands(session.app, name="session", help="Start an interactive session 🕹️", no_args_is_help=True)
cli.add_subcommands(apps.app, name="app", help="Start an app 🖥️", no_args_is_help=True)
cli.add_subcommands(dev.app, name="dev", help="Developer commands", no_args_is_help=True, hidden=True)


@cli.command("open", requires_auth=False, inject_sdk=True)
async def open_slingshot_homepage(sdk: slingshot_sdk.SlingshotSDK) -> None:
    """
    Opens the project in your default browser.
    """
    url = sdk.web_path_util.homepage
    console.print(f"Opening in browser: [link={url}]{url}[/link]")
    typer.launch(url)


@cli.command("list-commands", hidden=True, requires_auth=False, requires_project=False)
async def list_commands() -> None:
    console.print(repr(cli))


app = cli.make_typer_app()

# NOTE: CLI auto-completion is not supported for local development because it doesn't seem to work in
# editable mode. However, it does work when installed from the Slingshot Client wheel via pip.
if __name__ == "__main__":
    app()
