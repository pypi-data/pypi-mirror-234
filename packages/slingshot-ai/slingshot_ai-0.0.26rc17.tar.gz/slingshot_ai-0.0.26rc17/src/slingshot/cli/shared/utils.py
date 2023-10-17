from __future__ import annotations

import asyncio
import json
import math
import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import typer

from slingshot import schemas
from slingshot.cli.shared import prompt_confirm
from slingshot.cli.shared.handle_interrupts import handle_interrupts
from slingshot.schemas import slingshot_schema as slingshot_yaml_schemas
from slingshot.sdk.config import client_settings
from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.slingshot_api import JSONType
from slingshot.sdk.utils import console, yaml
from slingshot.shared.config import load_slingshot_project_config, mark_slingshot_project_config_dirty
from slingshot.shared.utils import pydantic_to_dict

if TYPE_CHECKING:
    from slingshot.sdk.slingshot_sdk import SlingshotSDK


def format_logline(logline: schemas.LogLine) -> str:
    return logline.log


def merge_loglines(loglines: list[schemas.LogLine]) -> str:
    return "\n".join(format_logline(logline) for logline in loglines)


async def quietly_cancel(task: asyncio.Task[Any]) -> None:
    """Cancels a task and ignores the CancelledError exception"""
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


async def follow_run_logs_until_done(sdk: SlingshotSDK, run_id: str) -> None:
    interrupt_event: asyncio.Event
    with handle_interrupts() as interrupt_event:
        task_logs = asyncio.create_task(sdk.print_logs(run_id=run_id, follow=True))
        task_status = asyncio.create_task(_wait_for_run_finished(sdk=sdk, run_id=run_id))
        task_interrupt = asyncio.create_task(interrupt_event.wait())
        # Wait for either task to finish
        await asyncio.wait([task_logs, task_status, task_interrupt], return_when=asyncio.FIRST_COMPLETED)

        # Case 1: task_status finished first. Either the run finished or task_status exception'd
        if task_status.done():
            await quietly_cancel(task_logs)
            await task_status  # This should raise an exception iff the task_status exception'd
            return

        # Case 2: task_interrupt finished first. User ctrl-c'd
        if interrupt_event.is_set():
            await quietly_cancel(task_status)
            await quietly_cancel(task_logs)
            console.print("\nNo longer following logs. If you want to stop the run, run 'slingshot run stop'.")
            exit(-1)

        # Case 3: task_logs finished first. Something went wrong in task_logs. Let's raise the relevant exception

        await quietly_cancel(task_status)  # task_status is no longer relevant, let's cancel it quietly
        await quietly_cancel(task_interrupt)
        await task_logs  # This should raise an exception iff the task_logs exception'd

        # Case 3: This should never happen. If it does, something is wrong
        raise SlingshotException("Something went wrong while following logs. Please try again.")


async def follow_app_logs_until_ready(sdk: SlingshotSDK, spec_id: str) -> schemas.ComponentInstanceStatus:
    interrupt_event: asyncio.Event
    with handle_interrupts() as interrupt_event:
        task_logs = asyncio.create_task(sdk.print_logs(spec_id=spec_id, follow=True))
        task_status = asyncio.create_task(_wait_for_app_ready(sdk=sdk, spec_id=spec_id))
        task_interrupt = asyncio.create_task(interrupt_event.wait())
        # Wait for either task to finish
        await asyncio.wait([task_logs, task_status, task_interrupt], return_when=asyncio.FIRST_COMPLETED)

        # Case 1: task_status finished first. Either the run finished or task_status exception'd
        if task_status.done():
            await quietly_cancel(task_logs)
            await quietly_cancel(task_interrupt)
            return await task_status  # This should raise an exception iff the task_status exception'd

        # Case 2: task_interrupt finished first. User ctrl-c'd
        if interrupt_event.is_set():
            assert interrupt_event
            await quietly_cancel(task_status)
            await quietly_cancel(task_logs)
            console.print("\nNo longer following logs. If you want to stop the app, run 'slingshot app stop'.")
            exit(-1)

        # Case 3: task_logs finished first.
        await quietly_cancel(task_status)  # task_status is no longer relevant, let's cancel it quietly
        await quietly_cancel(task_interrupt)
        await task_logs  # This should raise an exception if the task_logs exception'd

        # Case 4: This should never happen. If it does, something is wrong
        raise SlingshotException("Something went wrong while following logs. Please try again.")


def datetime_to_human_readable(dt: datetime) -> str:
    """Assumes UTC datetime and converts to local time in the format of: Mar 2, 2021 1:30AM EST"""
    date_str = dt.strftime('%b %d, %Y %I:%M:%S %p')
    return f'{date_str} UTC'


def seconds_to_human_readable(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.0f}s"
    if seconds < 3600:
        # In the format 10m 30s
        return f"{int(seconds // 60)}m {seconds_to_human_readable(seconds % 60)}"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h {seconds_to_human_readable(seconds % 3600)}"
    return f"{seconds // 86400}d {seconds_to_human_readable(seconds % 86400)}"


def bytes_to_human_readable_size(size: int | None, precision: int = 1) -> str:
    if size is None:
        return ""

    if size == 0:
        return "0 Bytes"
    k = 1024
    sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

    i = int(math.log(size) // math.log(k))
    return f"{size / k ** i:.{precision}f} {sizes[i]}"


def parse_extra_args(extra_args: list[str]) -> JSONType:
    # We prepend an empty string to detect loose args
    # We append -- to parse args correctly when the last arg is a flag
    extra_args = [""] + extra_args + ["--"]
    extra_args_pairs = list(zip(extra_args, extra_args[1:]))
    # Checks if there are loose args and raises an error if there are
    loose_args = [
        next_arg for arg, next_arg in extra_args_pairs if not next_arg.startswith("--") and not arg.startswith("--")
    ]
    if loose_args:
        raise typer.BadParameter(f"Extra args must start with -- . Got loose values {loose_args}")
    # All args have to start with -- so we can iterate only on `.startswith("--")`
    # If the arg is a key-value arg, we add it by using the first position of the tuple as key and second as value
    # If the arg is a flag, then the second position of the tuple will start with --. We instead set the value to True
    return {k[2:]: (True if v.startswith("--") else _infer_type(v)) for k, v in extra_args_pairs if k.startswith("--")}


async def prompt_push_code(sdk: SlingshotSDK) -> str | None:
    """Prompts the user to push code if it has changed since last push."""
    project = load_slingshot_project_config()
    source_mappings = project.sources if project.sources is not None else get_default_source_mappings()

    if not await sdk.has_code_changed(source_mappings) or not prompt_confirm(
        "Code has changed since last push. Do you want to push now?", default=True
    ):
        return None
    source_code = await sdk.push_code(source_mappings, and_print=False)
    source_code_id = source_code.source_code_id
    return source_code_id


def get_default_source_mappings() -> list[schemas.SourceMapping]:
    default_path_mapping = f"{os.path.dirname(client_settings.slingshot_config_path)}:."
    return [schemas.SourceMapping(path=default_path_mapping)]


async def get_hyperparameter_config_from_file(config_file: Path) -> JSONType:
    if not config_file.is_file():
        raise SlingshotException(
            f"Config file {config_file.name} could not be found or is not a file ({config_file.absolute()})"
        )
    with open(config_file, "r") as f:
        return json.load(f)


def _infer_type(value: str) -> Any:
    # noinspection GrazieInspection
    """Tries to infer the type of a string. If it can't, just returns the string."""
    try:
        return json.loads(value)
    except ValueError:
        return value


async def _wait_for_run_finished(sdk: SlingshotSDK, run_id: str) -> schemas.ComponentInstanceStatus:
    async for status in sdk.api.follow_run_status(run_id):
        if status.is_terminal:
            return status
    raise AssertionError("Unreachable")


async def _wait_for_app_ready(sdk: SlingshotSDK, spec_id: str) -> schemas.ComponentInstanceStatus:
    async for status in sdk.api.follow_app_status(spec_id):
        if status.is_ready or status.is_terminal:
            return status
    raise AssertionError("Unreachable")


def create_empty_project_manifest(manifest_path: Path) -> None:
    # Touch the file
    manifest_path.touch()

    # Ensure that we don't use a cached value of the slingshot.yaml as we'll be changing it
    mark_slingshot_project_config_dirty()

    # Insert an empty project manifest
    doc = pydantic_to_dict(slingshot_yaml_schemas.ProjectManifest(), exclude_unset=False)
    yaml.indent(mapping=2, sequence=4, offset=2)
    with manifest_path.open("w") as f:
        yaml.dump(doc, f)
