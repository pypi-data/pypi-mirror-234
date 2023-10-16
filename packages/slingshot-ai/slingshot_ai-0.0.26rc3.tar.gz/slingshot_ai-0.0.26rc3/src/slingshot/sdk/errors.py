from __future__ import annotations

import typing

import sentry_sdk
from aiohttp.client_exceptions import ClientResponse
from rich.console import Console

from .config import client_settings

if typing.TYPE_CHECKING:
    from .graphql import GraphQLError


class SlingshotException(Exception):
    """Base Slingshot Exception"""

    def __init__(self, msg: str, *, cli: str | None = None):
        """
        :param msg: The message to display
        :param cli: The message to display in the CLI. If not provided, defaults to `msg`
        """
        self.cli = cli or msg
        super().__init__(msg)

    def rich_show(self, console: Console, verbose: bool = False) -> None:
        """Return a string representation of the exception"""
        if self.cli:
            console.print(f"[bold][red]Error:[/bold][/red] {self.cli}")
        else:
            console.print(f"[bold][red]Error:[/bold][/red] {self}")
        if verbose:
            console.print_exception()


class SlingshotFileNotFoundException(SlingshotException):
    pass


class SlingshotClientHttpException(SlingshotException):
    def __init__(self, json: dict[str, typing.Any] | None, text: str, status: int, response: ClientResponse):
        self.json = json
        self.text = text
        self.status = status
        self.response = response
        super().__init__(f"Slingshot Client HTTP {status}: {text}")

    @staticmethod
    async def from_response(response: ClientResponse) -> SlingshotClientHttpException:
        try:
            # If we can parse the respone, we do to get more details out. If not, that's OK too.
            response_json = await response.model_dump_json()  # type: ignore
        except Exception:
            response_json = None
        return SlingshotClientHttpException(
            json=response_json, text=await response.text(), status=response.status, response=response
        )

    def rich_show(self, console: Console, verbose: bool = False) -> None:
        msg = self.json['error'] if self.json and 'error' in self.json else self.text
        console.print(f"Slingshot Error ({self.status}): \"{msg}", style="red")
        if verbose and self.json and ("traceback" in self.json):
            console.print(f"Traceback: {self.json['traceback']}")


class SlingshotClientGraphQLException(SlingshotException):
    @staticmethod
    def from_graphql_errors(errors: list["GraphQLError"]) -> SlingshotClientGraphQLException:
        return SlingshotClientGraphQLException(errors)

    def __init__(self, errors: list["GraphQLError"]) -> None:
        messages = [error.message for error in errors]
        self.errors = errors
        self.messages = messages
        super().__init__(f"Slingshot Client GraphQL Error: {messages}")

    def rich_show(self, console: Console, verbose: bool | None = False) -> None:
        console.print(f"Slingshot GraphQL Error: {self.messages}", style="red")
        if verbose:
            for error in self.errors:
                console.print(f"Error: {error.message}", style="red")
                if error.locations:
                    console.print(f"Locations: {error.locations}", style="red")
                if error.path:
                    console.print(f"Path: {error.path}", style="red")
                if error.extensions:
                    console.print(f"Extensions: {error.extensions}", style="red")


class SlingshotConnectionError(SlingshotException, ConnectionError):
    """Could not connect to Slingshot"""

    def __init__(self, url: str):
        self._url = url
        super().__init__(f"Could not connect to url: {url}")

    def rich_show(self, console: Console, verbose: bool = False) -> None:
        console.print(
            f'[bold][red]Could not connect to {self._url}[/bold][/red]\n'
            'If the host is not correct, you can reconfigure the backend url by running '
            '"slingshot be [backend]".'
        )


class SlingshotBackoffError(SlingshotException):
    pass


class SlingshotCodeNotFound(SlingshotException):
    def __init__(self) -> None:
        super().__init__(f"No source code found.")

    def rich_show(self, console: Console, verbose: bool = False) -> None:
        console.print("[red]Error:[/red] No source code found for your project. Please run 'slingshot push'.")


class SlingshotInvalidTokenError(SlingshotException):
    """Invalid token"""

    def __init__(self) -> None:
        super().__init__(f"Your login is invalid, likely expired or invalid.")

    def rich_show(self, console: Console, verbose: bool = False) -> None:
        console.print("[red]Error:[/red] Your auth token is invalid or expired. Please run 'slingshot login'.")


class SlingshotUnauthenticatedError(SlingshotException):
    """User is not signed in, but command requires authentication"""

    graphql_message = "Missing 'Authorization' or 'Cookie' header in JWT authentication mode"

    def __init__(self) -> None:
        if client_settings.is_in_app:
            super().__init__(f"You're not signed in. Did you mean to attach project credentials?")
        else:
            super().__init__(f"You're not signed in.")

    def rich_show(self, console: Console, verbose: bool = False) -> None:
        console.print("[red]Error:[/red] This command requires you to be signed in. Please run 'slingshot login'.")


class SlingshotJWTExpiredError(SlingshotException):
    """JWT token is expired"""

    graphql_message = "Could not verify JWT: JWTExpired"

    def __init__(self) -> None:
        super().__init__(f"Your login token is expired.")

    def rich_show(self, console: Console, verbose: bool = False) -> None:
        console.print("[red]Error:[/red] Your login token is expired. Please run 'slingshot login'.")


class SlingshotJWSInvalidSignature(SlingshotException):
    """JWT token is invalid (e.g. switched to another backend)"""

    graphql_message = "JWSInvalidSignature"

    def __init__(self) -> None:
        super().__init__(f"Your login token is invalid.")

    def rich_show(self, console: Console, verbose: bool = False) -> None:
        console.print("[red]Error:[/red] Your login token is invalid. Please run 'slingshot login'.")


class SlingshotNoProjectSetError(SlingshotException):
    """No project is set"""

    def __init__(self) -> None:
        super().__init__(f"No project is set, and no project could be inferred.")

    def rich_show(self, console: Console, verbose: bool = False) -> None:
        if client_settings.is_in_app:
            # This should never happen!
            with sentry_sdk.push_scope() as scope:
                scope.set_extra("component_type", client_settings.slingshot_component_type)
                scope.set_extra("app_instance_id", client_settings.slingshot_instance_id)
                sentry_sdk.capture_exception(self)
        console.print("[red]Error:[/red] No project is set. Please run 'slingshot project set [project]'.")
