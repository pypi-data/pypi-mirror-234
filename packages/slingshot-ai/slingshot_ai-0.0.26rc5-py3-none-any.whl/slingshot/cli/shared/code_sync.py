from __future__ import annotations

import asyncio
import contextlib
import os
import platform
import re
import shutil
import sys
import uuid
from asyncio import create_subprocess_exec
from asyncio.subprocess import Process  # noqa
from logging import getLogger
from time import sleep
from typing import Any, Iterator

import sh  # type: ignore
import typer
from pathspec.patterns import GitWildMatchPattern

from slingshot import schemas
from slingshot.cli.config.slingshot_cli import SlingshotCLIApp
from slingshot.cli.shared.formatting import describe_component_type
from slingshot.cli.shared.ssh import start_ssh_for_app
from slingshot.sdk.config import client_settings
from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.graphql import fragments
from slingshot.sdk.slingshot_sdk import SlingshotSDK
from slingshot.sdk.sync import normalize_source_mappings
from slingshot.sdk.utils import console, flatten

app = SlingshotCLIApp()
logger = getLogger(__name__)


async def start_code_sync(
    source_mappings: list[schemas.SourceMapping], component_spec: fragments.ComponentSpec, *, sdk: SlingshotSDK
) -> None:
    """
    Starts code sync with a remote app. The app should already be running, or this will fail with an error.
    :param source_mappings: Rules describing the path(s) to sync to the remote.
    :param component_spec: Spec of the app to sync against (may be a session or other app such as a web app)
    :param sdk: Slingshot SDK
    """

    # Apply automatic rules for excluding overlapping directories
    source_mappings = normalize_source_mappings(source_mappings)
    ssh_connection_details = await start_ssh_for_app(component_spec, use_case='code sync', sdk=sdk)
    ssh_connection_str = (
        f"{ssh_connection_details.username}@{ssh_connection_details.hostname}:{ssh_connection_details.port}"
    )
    formatted_component_type = describe_component_type(component_spec.component_type, component_spec.app_sub_type)
    target_sync_path = (
        "/slingshot/session" if component_spec.app_sub_type == schemas.AppSubType.SESSION else "/mnt/slingshot/code"
    )

    unison_jobs = [
        _run_unison(formatted_component_type, ssh_connection_str, source_mapping, target_sync_path, verbose=sdk.verbose)
        for source_mapping in source_mappings
    ]

    await asyncio.gather(*unison_jobs)


async def _run_unison(
    component_type: str,
    ssh_connection_str: str,
    source_mapping: schemas.SourceMapping,
    target_sync_path: str,
    verbose: bool = False,
) -> None:
    unison_path = _find_unison_if_installed()
    if not unison_path:
        _print_unison_install_instructions()
        raise typer.Exit(1)

    # TODO: poll until sshd is available. For now, we can assume it takes <1s.
    sleep(1)
    remote_ssh = f"ssh://{ssh_connection_str}/{target_sync_path}"
    logger.debug(remote_ssh)

    with _open_log_file(verbose) as (stdout, stderr, logfile):
        for _ in range(3):  # retry 3 times
            console.print(
                f"[blue]Syncing {os.path.realpath(source_mapping.local_path.absolute())} to {source_mapping.remote_path} in your {component_type}...[/blue]"
            )
            try:
                # run unison command in a subprocess
                # assumes ssh key is already added to the server authorized_keys
                # TODO: support explicit selection of the SSH key
                #  unison /local/path ssh://remote/path -sshcmd 'ssh -i /path/to/your_specific_key'
                process = await _start_unison(unison_path, remote_ssh, source_mapping, stdout=stdout, stderr=stderr)
                await process.wait()
            except sh.ErrorReturnCode:
                # TODO consider parsing the unison.log to e.g. automatically identify if it's a `Permission denied
                #  (publickey)` error
                console.print("[yellow]An error occurred while syncing your code. Retrying...[/yellow]")
                console.print(
                    "[yellow]Please make sure the SSH key used for code sync has been added to the SSH agent[/yellow]"
                )
                await asyncio.sleep(1)  # wait for a second before retrying
        raise SlingshotException(f"Error running unison, please check {logfile or 'above output'} for more details")


async def _start_unison(
    unison_path: str, remote_root: str, source_mapping: schemas.SourceMapping, *, stdout: Any, stderr: Any
) -> Process:
    unison_exclude_rules = flatten([_unison_exclude_rule(exclude) for exclude in source_mapping.exclude_paths])

    # NOTE: Unison bails if we try to start it with watch support against a remote root that does not yet exist.
    # If we let it sync the initial state _once_ first through without watches, it's happy, hence the double call here.
    initial_sync_process = await create_subprocess_exec(
        unison_path,
        str(source_mapping.local_path),
        f"{remote_root}/{source_mapping.remote_path}",
        "-batch=true",  # batch mode: ask no questions at all
        "-prefer=newer",  # choose newer version for conflicting changes
        "-copyonconflict=true",  # keep copies of conflicting files
        "-sshargs=-o StrictHostKeyChecking=no",  # skip known_hosts check
        *unison_exclude_rules,
        stdout=stdout,
        stderr=stderr,
    )
    await initial_sync_process.wait()
    if initial_sync_process.returncode != 0:
        return initial_sync_process

    return await create_subprocess_exec(
        unison_path,
        str(source_mapping.local_path),
        f"{remote_root}/{source_mapping.remote_path}",
        "-batch=true",  # batch mode: ask no questions at all
        "-repeat=watch",  # synchronize repeatedly (using unison-fsmonitor process to detect changes)
        "-prefer=newer",  # choose newer version for conflicting changes
        "-copyonconflict=true",  # keep copies of conflicting files
        "-sshargs=-o StrictHostKeyChecking=no",  # skip known_hosts check
        *unison_exclude_rules,
        stdout=stdout,
        stderr=stderr,
    )


def _unison_exclude_rule(exclude: str) -> list[str]:
    regex, is_exclude = GitWildMatchPattern.pattern_to_regex(exclude)
    flag = '-ignore' if is_exclude else '-ignorenot'
    # NOTE: Python uses a special syntax for named capture groups. Unison also doesn't care about non capturing
    # groups, so strip these features. Really thought there would be a library method for this ...
    sane_regex = re.sub(r'\(\?:', '(', re.sub(r'\(\?P<[^>]+>', '(', str(regex))).replace("\\-", "-")
    return [flag, f"Regex {sane_regex}"]


def _find_unison_if_installed() -> str | None:
    _unison = shutil.which("unison")
    if not _unison:
        console.print("[red]Unison is not installed[/red]")
    _fsmonitor = shutil.which("unison-fsmonitor")
    if not _fsmonitor:
        console.print("[red]Unison-fsmonitor is not installed[/red]")
    if _unison and _fsmonitor:
        return _unison
    else:
        return None


def _print_unison_install_instructions() -> None:
    uname = platform.uname()

    console.print("[yellow] We use unison and unison-fsmonitor for code sync, please install [/yellow]")
    if uname.system == "Darwin":
        console.print("[yellow] Using homebrew:[/yellow]")
        console.print("[yellow]  brew install unison[/yellow]")
        console.print("[yellow]  brew install eugenmayer/dockersync/unox[/yellow]")
    elif uname.system == "Linux":
        console.print("[yellow] Manually from official releases:[/yellow]")
        console.print(
            "[yellow]  wget -qO- "
            "https://github.com/bcpierce00/unison/releases/download/v2.53.0/"
            "unison-v2.53.0+ocaml-4.13.1+x86_64.linux.tar.gz"
            " | sudo tar -zxvf - -C /usr bin/[/yellow]"
        )
    console.print("[yellow] For more information see:[/yellow]")
    console.print("[yellow]  https://github.com/bcpierce00/unison/blob/master/INSTALL.md [/yellow]")


@contextlib.contextmanager
def _open_log_file(verbose: bool) -> Iterator[tuple[Any, Any, str | None]]:  # stdout, stderr
    log_file = client_settings.global_config_folder / f"unison-{uuid.uuid4().hex[:4]}.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    # If verbose, print to stdout/stderr, otherwise write to log file
    if verbose:
        yield sys.stdout, sys.stderr, None
    else:
        with open(log_file, "w") as f:
            yield f, f, str(log_file)
