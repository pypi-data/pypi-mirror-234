from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

from slingshot import SlingshotSDK, schemas
from slingshot.cli.auth import set_ssh_public_key_if_not_set
from slingshot.cli.shared.formatting import describe_component_type
from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.graphql import fragments
from slingshot.sdk.utils import console

ERROR_SSH_KEY_MISSING = (
    "[red]You must add an SSH key to your account before using code sync[/red]"
    "Run [bold green]slingshot auth set-ssh[/bold green] to add an SSH key"
)


@dataclass
class SshConnectionDetails:
    username: str
    hostname: str
    port: int


async def ensure_user_is_configured_for_ssh(sdk: SlingshotSDK) -> None:
    """Check that the user has an SSH key set. If not, prompt to set one."""
    await set_ssh_public_key_if_not_set(sdk)
    me = await sdk.me()
    if not (me and me.user):
        raise SlingshotException("Only users can sync code")
    if not me.user.ssh_public_key:
        raise SlingshotException(ERROR_SSH_KEY_MISSING)


async def start_ssh_for_app(
    app_spec: fragments.ComponentSpec, *, use_case: str | None = None, sdk: SlingshotSDK
) -> SshConnectionDetails:
    """
    Exposes SSH for a running app. This will fail if the app isn't currently running, and returns when the backend
    has confirmed that SSH has been exposed.
    :param app_spec: The app to enable SSH for, must be a "custom" app (not a run, deployment, etc)
    :param use_case a human readable description of the use cased used in messages to the user
    :param sdk: Slingshot SDK
    :return SSH connection details to be used in SSH or SCP commands
    """

    assert app_spec.component_type == schemas.ComponentType.APP, "This method only supports custom apps"

    use_case = use_case or 'SSH'
    formatted_component_type = describe_component_type(app_spec.component_type, app_spec.app_sub_type)
    console.print(f"Starting {use_case} for {formatted_component_type} '{app_spec.spec_name}'")

    if (
        app_spec.app_instance_status is None
        or not app_spec.app_instance_status.is_running
        or app_spec.app_instance_url is None
    ):
        raise SlingshotException(
            f"Cannot {use_case} while {formatted_component_type} is not running. Current status: {app_spec.app_instance_status}"
        )

    app_instance_url = app_spec.app_instance_url

    assert app_spec.app_instances, "App instances should be available"
    app_instance = app_spec.app_instances[0]
    ssh_port: Optional[int] = app_instance.ssh_port

    if not ssh_port:
        console.print(f"Allocating port for {use_case} ...")
        resp = await sdk.start_app_ssh(app_spec.spec_id)
        if resp.error:
            raise SlingshotException(resp.error.message)
        ssh_port = resp.data.ssh_port if resp.data else None

    if not ssh_port:
        raise SlingshotException(f"Failed to allocate port for {use_case}")

    return _get_ssh_connection_details(app_instance_url, ssh_port)


async def start_ssh_for_run(run: fragments.Run, *, sdk: SlingshotSDK) -> SshConnectionDetails:
    """
    Exposes SSH for a running run instance. This will fail if the run isn't currently running, and returns when the
    backend has confirmed that SSH has been exposed.
    :param run: Spec of the run to enable SSH for. Expected to be running (started, not finished)
    :param sdk: Slingshot SDK
    :return SSH connection details to be used in SSH or SCP commands
    """

    console.print(f"Starting SSH for run '{run.run_name}'")

    if not run.run_status.is_active:
        raise SlingshotException(f"Cannot SSH to a run that is not active. Current status: {run.run_status}")

    if not (run_instance_url := run.run_instance_url):
        raise SlingshotException("Run instance URL not found")

    ssh_port = run.ssh_port

    if not ssh_port:
        console.print(f"Allocating port for SSH ...")
        resp = await sdk.start_run_ssh(run.run_id)
        if resp.error:
            raise SlingshotException(resp.error.message)
        ssh_port = resp.data.ssh_port if resp.data else None

    if not ssh_port:
        raise SlingshotException("Failed to allocate port for SSH")

    return _get_ssh_connection_details(run_instance_url, ssh_port)


def _get_ssh_connection_details(instance_url: str, ssh_port: int) -> SshConnectionDetails:
    hostname = urlparse(instance_url).hostname
    assert hostname, "Invalid URL for app or backend"
    return SshConnectionDetails(username="slingshot", hostname=hostname, port=ssh_port)
