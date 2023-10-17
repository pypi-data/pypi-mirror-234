from __future__ import annotations

import json
import os
import typing
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from ruamel import yaml as r_yaml

from slingshot import schemas
from slingshot.sdk.errors import SlingshotException

yaml = r_yaml.YAML()

T = typing.TypeVar("T")


class ResponseProtocol(typing.Protocol[T]):
    data: typing.Optional[T]
    error: typing.Optional[schemas.SlingshotLogicalError]


def get_data_or_raise(resp: ResponseProtocol[T]) -> T:
    if resp.error:
        raise SlingshotException(resp.error.message)
    if resp.data is None:
        raise SlingshotException("No data returned from server")
    return resp.data


_machine_size_to_machine_type_gpu_count: dict[schemas.MachineSize, tuple[schemas.MachineType, int]] = {
    schemas.MachineSize.CPU_1X: (schemas.MachineType.CPU_TINY, 0),
    schemas.MachineSize.CPU_2X: (schemas.MachineType.CPU_SMALL, 0),
    schemas.MachineSize.CPU_4X: (schemas.MachineType.CPU_MEDIUM, 0),
    schemas.MachineSize.CPU_8X: (schemas.MachineType.CPU_LARGE, 0),
    schemas.MachineSize.T4: (schemas.MachineType.T4, 1),
    schemas.MachineSize.L4: (schemas.MachineType.L4, 1),
    schemas.MachineSize.A100: (schemas.MachineType.A100, 1),
    schemas.MachineSize.A100_8X: (schemas.MachineType.A100, 8),
}

_machine_type_gpu_count_to_machine_size: dict[tuple[schemas.MachineType, int], schemas.MachineSize] = {
    v: k for k, v in _machine_size_to_machine_type_gpu_count.items()
}


def machine_size_to_machine_type_gpu_count(machine_size: schemas.MachineSize) -> tuple[schemas.MachineType, int]:
    if machine_size not in _machine_size_to_machine_type_gpu_count:
        raise ValueError(f"Unknown machine size {machine_size}")
    return _machine_size_to_machine_type_gpu_count[machine_size]


def machine_type_gpu_count_to_machine_size(
    machine_type: schemas.MachineType, gpu_count: int | None
) -> schemas.MachineSize:
    if gpu_count is None:
        gpu_count = 0
    if (machine_type, gpu_count) not in _machine_type_gpu_count_to_machine_size:
        raise ValueError(f"Unknown machine type {machine_type} with {gpu_count} GPUs")
    return _machine_type_gpu_count_to_machine_size[(machine_type, gpu_count)]


def get_default_num_gpu(machine_type: schemas.MachineType) -> int:
    cpu_machine_types = {
        schemas.MachineType.CPU_TINY,
        schemas.MachineType.CPU_SMALL,
        schemas.MachineType.CPU_MEDIUM,
        schemas.MachineType.CPU_LARGE,
    }
    # CPU machines have no GPUs
    if machine_type in cpu_machine_types:
        return 0
    return 1


def pydantic_to_dict(pydantic: BaseModel, *, exclude_unset: bool = True) -> dict[str, Any]:
    # Convert enums to strings
    return json.loads(pydantic.model_dump_json(exclude_none=True, exclude_unset=exclude_unset))


@contextmanager
def enter_path(path: Path | str) -> typing.Generator[None, None, None]:
    """
    Changes the working directory to the specified, restoring it back to the original one when the context manager closes.
    """
    cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cwd)
