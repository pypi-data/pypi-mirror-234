from __future__ import annotations

import asyncio
import inspect
import logging
import textwrap
import traceback
from functools import wraps
from typing import Any, Callable, Coroutine, Mapping, Optional, TypeVar

import sentry_sdk
import typer
from typing_extensions import ParamSpec

from ...sdk import SlingshotSDK
from ...sdk.config import project_config
from ...sdk.errors import SlingshotException, SlingshotUnauthenticatedError
from ...sdk.utils import console
from ..shared.prompt import GLOBAL_Y_AUTO_CONFIRM_REF

PROJECT_ID_OPTION_HELPER_TEXT = "Project name must be specified or configured in .slingshot/config.json."
PROJECT_ID_NOT_FOUND_MSG = (
    f"The current directory is not associated with a Slingshot project. "
    "Ensure that you run 'slingshot' from the directory containing your 'slingshot.yaml', not a sub directory.\n"
    "To associate this directory with a new or existing Slingshot project, run 'slingshot init'."
)
PROJECT_OPTION = typer.Option(None, "--project-id", "--project", "-p", help=PROJECT_ID_OPTION_HELPER_TEXT)


class SlingshotCLICommand:
    PROJECT_ID_PARAM = inspect.Parameter(
        "project_id", kind=inspect.Parameter.KEYWORD_ONLY, annotation=Optional[str], default=PROJECT_OPTION
    )

    def __init__(
        self,
        name: str | None = None,
        top_level: bool = False,
        inject_sdk: bool | None = None,
        requires_project: bool | None = None,
        requires_auth: bool | None = None,
        decorator_kwargs: Mapping[str, Any] | None = None,
    ):
        self._name = name
        self._top_level = top_level
        self._inject_sdk = inject_sdk
        self._requires_project = requires_project
        self._requires_auth = requires_auth
        self._function: Callable[..., Any] | None = None

        self._decorator_kwargs = {**decorator_kwargs} if decorator_kwargs is not None else {}
        if name is not None:
            self._decorator_kwargs["name"] = name

        self._func: Callable[..., Any] | None = None

    @property
    def function(self) -> Callable[..., Any]:
        assert self._function is not None, "CLI command has not been initialized"
        return self._function

    def __call__(self, func: Callable[..., Any]) -> SlingshotCLICommand:
        if self._name is None:
            self._name = getattr(func, "__name__", None)
            assert self._name, "Couldn't identify the name of a CLI command. Please state it manually"
        self._function = func
        try:
            self._func = self._convert_func(func)
        except Exception as e:
            raise Exception(f"Failed to initialize CLI function '{self._name}'") from e
        return self

    def _convert_func(self, func: Callable[..., Any]) -> Callable[..., Any]:
        assert inspect.iscoroutinefunction(func), "CLI commands must be async functions"

        parameters = inspect.signature(func).parameters.copy()
        if self._inject_sdk is None:
            self._inject_sdk = "sdk" in parameters
        if self._requires_project is True:
            self._requires_auth = True

        assert not (
            self._inject_sdk and "sdk" not in parameters
        ), "Cannot inject SDK because `sdk` does not appear in the function's signature"

        @wraps(func)
        async def inner(*args: Any, **kwargs: Any) -> Any:
            from .sentry_setup import sentry_init

            sentry_init()
            with sentry_sdk.push_scope() as scope:
                scope.set_tag("command", self._name)
                scope.set_tag("inject_sdk", self._inject_sdk)
                scope.set_tag("requires_project", self._requires_project)
                scope.set_tag("requires_auth", self._requires_auth)
                scope.set_tag("function", func.__name__)
                scope.set_tag("CLI", True)

                verbose = kwargs.pop("verbose", False)
                scope.set_tag("verbose", verbose)

                if verbose:
                    logging.basicConfig(level=logging.DEBUG)

                y_auto_confirm_ = kwargs.pop("yes", False)
                scope.set_tag("y_auto_confirm", y_auto_confirm_)
                if y_auto_confirm_:
                    GLOBAL_Y_AUTO_CONFIRM_REF.current = True

                sdk = SlingshotSDK(verbose=verbose)
                try:
                    if self._requires_auth is True:
                        if not await sdk.is_signed_in():
                            raise SlingshotUnauthenticatedError()
                        if me := sdk._me:
                            scope.set_user(
                                {
                                    "user_id": me.user.user_id if me.user else None,
                                    "username": me.user.username if me.user else None,
                                    "service_account_id": me.service_account.service_account_id
                                    if me.service_account
                                    else None,
                                }
                            )
                            if me.user and not me.user.is_activated:
                                raise SlingshotException(
                                    "Your account is not yet activated. "
                                    "Contact Slingshot support to move up your spot on the waiting list!"
                                )
                    if self._requires_project is True:
                        project_id = kwargs.pop("project_id", None) or project_config.project_id
                        if not project_id:
                            raise SlingshotException(PROJECT_ID_NOT_FOUND_MSG)

                        await sdk.use_project(project_id)
                        scope.set_tag("project_id", project_id)

                    if self._inject_sdk is True:
                        kwargs["sdk"] = sdk
                        async with sdk.use_session():
                            return await func(*args, **kwargs)
                    return await func(*args, **kwargs)
                except SlingshotException as e:
                    logging.debug(f"Caught SlingshotException: {e}")
                    e.rich_show(console, verbose)
                    await sdk.check_for_updates(force=True)
                    raise typer.Exit(1)
                except Exception as e:
                    await sdk.check_for_updates(force=True)
                    raise e
                finally:
                    GLOBAL_Y_AUTO_CONFIRM_REF.current = False

        inner = make_sync(inner)

        oldsig = inspect.signature(func)

        parameters = oldsig.parameters.copy()
        # Hide parameters from Typer:
        if self._inject_sdk:
            assert "sdk" in parameters, "Cannot inject SDK because `sdk` does not appear in the function's signature"
            del parameters["sdk"]

        if self._requires_project:
            parameters["project_id"] = self.PROJECT_ID_PARAM

        verbose_param = inspect.Parameter(
            "verbose",
            kind=inspect.Parameter.KEYWORD_ONLY,
            annotation=bool,
            default=typer.Option(False, "--verbose", "-v"),
        )

        parameters["verbose"] = verbose_param

        yes_param = inspect.Parameter(
            "yes",
            kind=inspect.Parameter.KEYWORD_ONLY,
            annotation=bool,
            default=typer.Option(False, "--yes", "-y", help="Skip confirmation prompts (will default to 'yes' for all"),
        )

        parameters["yes"] = yes_param

        inner.__signature__ = oldsig.replace(parameters=list(parameters.values()))  # type: ignore

        return inner

    def get_typer_kwargs(self) -> dict[str, Any]:
        kwargs = self._decorator_kwargs
        if self._name is not None:
            kwargs["name"] = self._name
        return kwargs

    def get_typer_func(self) -> Callable[..., Any]:
        func = self._func
        assert func is not None, "CLI command was not initialized"
        return func

    def __repr__(self) -> str:
        kwargs = {k: v for k, v in self._decorator_kwargs.items() if k != 'name'}
        kwargs_str = f"**{kwargs}" if kwargs is not None else ""
        return (
            f"SlingshotCLICommand("
            f"name={repr(self._name)}, "
            f"inject_sdk={repr(self._inject_sdk)}, "
            f"requires_project={repr(self._requires_project)}, "
            f"requires_auth={repr(self._requires_auth)}, {kwargs_str}"
            f")"
        )


class SlingshotCLIApp:
    def __init__(
        self,
        name: str | None = None,
        help: str | None = None,
        no_args_is_help: bool | None = None,
        as_panel: bool = False,
        **kwargs: Any,
    ):
        self._kwargs = {**kwargs, "name": name, "help": help, "no_args_is_help": no_args_is_help}
        self._subcommands: list[SlingshotCLIApp] = []
        self._commands: list[SlingshotCLICommand] = []
        self._as_panel = as_panel

    def command(
        self,
        name: str | None = None,
        inject_sdk: bool | None = None,
        top_level: bool = False,
        requires_project: bool | None = None,
        requires_auth: bool | None = None,
        **decorator_kwargs: Any,
    ) -> SlingshotCLICommand:
        """
        :param name: The command's name. If omitted, the name of the function will be used
        :param inject_sdk: Whether to inject the SDK.
            If omitted, will inject iff `sdk` appears in the command function's signature
        :param top_level: Whether to add the command to the top-level app, i.e. with no a: prefix
        :param requires_project: Whether to require that the project be either specified or available from the context
            (e.g. through `slingshot use`). If true, the `--project` option will be added to the command's signature
        :param requires_auth: Whether to require that a user is authenticated before executing the command.
        :param decorator_kwargs: Any additional keyword arguments to pass to typer.command
        """
        cmd = SlingshotCLICommand(
            name=name,
            inject_sdk=inject_sdk,
            top_level=top_level,
            requires_project=requires_project,
            requires_auth=requires_auth,
            decorator_kwargs=decorator_kwargs,
        )
        self.add_command(cmd)
        return cmd

    def add_command(self, command: SlingshotCLICommand) -> None:
        self._commands.append(command)

    def add_subcommands(
        self,
        slingshot_cli_app: SlingshotCLIApp,
        name: str | None = None,
        help: str | None = None,
        no_args_is_help: bool | None = None,
        hidden: bool | None = None,
        as_panel: bool | None = None,
    ) -> None:
        if name is not None:
            slingshot_cli_app._kwargs["name"] = name
        if help is not None:
            slingshot_cli_app._kwargs["help"] = help
        if no_args_is_help is not None:
            slingshot_cli_app._kwargs["no_args_is_help"] = no_args_is_help
        if hidden is not None:
            slingshot_cli_app._kwargs["hidden"] = hidden
        if hidden and as_panel is None:
            as_panel = False
        if as_panel is not False:
            as_panel = True
        slingshot_cli_app._as_panel = as_panel
        # Wrapper on Typer.add_typer()
        self._subcommands.append(slingshot_cli_app)

    def make_typer_app(self) -> typer.Typer:
        typer_app = typer.Typer(**self._kwargs)
        for c in self._commands:
            typer_app.command(**c.get_typer_kwargs())(c.get_typer_func())
        for a in self._subcommands:
            if not a._as_panel:
                # If it's not a panel, just add it as a subcommand
                typer_app.add_typer(a.make_typer_app())
                for cmd in a._commands:
                    if cmd._top_level:
                        typer_app.command(**cmd.get_typer_kwargs())(cmd.get_typer_func())
            else:
                # If it's a panel, add it as a subcommand, but also add its commands to the top-level app
                typer_app.add_typer(a.make_typer_app(), hidden=True)
                if a._subcommands:
                    raise NotImplementedError("Cannot add subcommands to a panel")
                # Replace names with "{app.name} {command.name}"
                for cmd in a._commands:
                    cmd._decorator_kwargs["rich_help_panel"] = a._kwargs["name"]
                    root = a._kwargs['name']
                    sub = cmd._name
                    if cmd._top_level:
                        # If it's a top-level command, just add it to the top-level app
                        typer_app.command(**cmd.get_typer_kwargs())(cmd.get_typer_func())
                    else:
                        # Otherwise, add it as root:sub
                        cmd._name = f"{root}:{sub}"
                        typer_app.command(**cmd.get_typer_kwargs())(cmd.get_typer_func())

        return typer_app

    def __repr__(self) -> str:
        cmds = '\n,'.join(repr(i) for i in self._commands)
        cmds = cmds and f"\n{cmds}\n"
        cmds = textwrap.indent(cmds, prefix="\t")
        sub = '\n'.join(repr(i) for i in self._subcommands)
        sub = textwrap.indent(sub, prefix="\t")
        b = f"commands=[{cmds}], \n" f"subcommands=[{sub}]"
        return f"SlingshotCLIApp({repr(self._kwargs)}, {b})"


P = ParamSpec('P')
R = TypeVar('R')


def make_sync(func: Callable[P, Coroutine[Any, Any, R]]) -> Callable[P, R]:
    """Typer doesn't support async functions by default
    This wraps the function with a loop so it's seen as
    a non-async function by typer
    """

    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        try:
            return asyncio.run(func(*args, **kwargs))
        except Exception as e:
            # Remove frames from the stacktrace that are not relevant to the user
            if not e.__traceback__:
                sentry_sdk.capture_exception(e)
                raise e

            index = [i for i, f in enumerate(traceback.extract_tb(e.__traceback__)) if f.filename.endswith(__file__)][
                -1
            ]  # Remove all frames up until and including the last frame in this file
            e.__traceback__ = e.__traceback__.tb_next
            for i in range(index):
                if not e.__traceback__:
                    sentry_sdk.capture_exception(e)
                    raise e
                e.__traceback__ = e.__traceback__.tb_next
            del args, kwargs, i, index

            sentry_sdk.capture_exception(e)
            raise e
        finally:
            sentry_sdk.flush()  # Make sure we drain the event queue so that Sentry events are sent

    inner.run_async = func  # type: ignore
    return inner
