from __future__ import annotations

import base64
import contextlib
import copy
import hashlib
import json
import os
from datetime import datetime
from enum import Enum
from functools import reduce
from pathlib import Path
from typing import Any, Iterator, Type, TypeVar

from pydantic.main import BaseModel
from rich.console import Console
from ruamel import yaml as r_yaml
from ruamel.yaml.representer import RepresenterError

from slingshot.sdk.config import client_settings
from slingshot.sdk.errors import SlingshotException
from slingshot.shared.config import mark_slingshot_project_config_dirty

console = Console()
yaml = r_yaml.YAML()

T = TypeVar("T", bound=BaseModel)


def time_since_string(then: datetime) -> str:
    """Compute the time since a given datetime as a pretty string"""
    now = datetime.utcnow()
    diff = now - then
    if diff.total_seconds() < 0:
        # Lol this should never happen, but it was helpful for debugging! We should remove in prod.
        return f"in the future, negative {time_since_string(now + diff)}"
    if diff.days > 0:
        return f"{diff.days} days, {diff.seconds // 3600} hours ago"
    if diff.seconds > 3600:
        return f"{diff.seconds // 3600} hours, {diff.seconds % 3600 // 60} minutes ago"
    if diff.seconds > 60:
        return f"{diff.seconds // 60} minutes, {diff.seconds % 60} seconds ago"
    return f"{diff.seconds} seconds ago"


def bytes_to_str(num: int | float) -> str:
    """Convert bytes to a human-readable string"""
    for x in ["bytes", "KiB", "MiB", "GiB", "TiB", "PiB"]:
        if num < 1024:
            if num == int(num):
                return f"{int(num)} {x}"
            return f"{num:.2f} {x}"
        num /= 1024
    return f"{num:.2f} Really Big Units"


def md5_hash(input_bytes: bytes) -> str:
    m = hashlib.md5()
    m.update(input_bytes)
    hash_digest = m.digest()
    return base64.b64encode(hash_digest).decode("utf-8")


@contextlib.contextmanager
def edit_slingshot_yaml(raise_if_absent: bool = True, filename: str | None = None) -> Iterator[dict[str, Any]]:
    file = (Path(os.getcwd()) / filename) if filename else client_settings.slingshot_config_path

    try:
        text = file.read_text()
    except FileNotFoundError as e:
        if raise_if_absent:
            raise e

        text = "{}"

    doc = yaml.load(text)
    original = copy.deepcopy(doc)
    yield doc
    # Ensure that we don't use a cached value of the slingshot.yaml as we'll be changing it
    mark_slingshot_project_config_dirty()
    # there might be enums in here. if there are, we need to convert them to strings
    doc = recursive_enum_to_str(doc)
    yaml.indent(mapping=2, sequence=4, offset=2)
    with file.open("w") as f:
        try:
            yaml.dump(doc, f)
        except RepresenterError as e:
            yaml.dump(original, f)
            raise SlingshotException(f"Error while editing slingshot.yaml: {e.args[0]}") from e


def recursive_enum_to_str(value: Any) -> Any:
    """
    Recursively converts all enums in an object to strings, as long as the object consists of dicts, lists, and plain
    values.

    >>> recursive_enum_to_str({"foo": schemas.MachineType.CPU_TINY})
    {'foo': 'CPU_TINY'}
    >>> recursive_enum_to_str([schemas.MachineType.CPU_TINY])
    ['CPU_TINY']
    >>> recursive_enum_to_str(schemas.MachineType.CPU_TINY)
    'CPU_TINY'
    >>> recursive_enum_to_str({"foo": {"bar": schemas.MachineType.CPU_TINY}})
    {'foo': {'bar': 'CPU_TINY'}}
    >>> recursive_enum_to_str({"foo": [schemas.MachineType.CPU_TINY]})
    {'foo': ['CPU_TINY']}
    >>> recursive_enum_to_str([{"foo": schemas.MachineType.CPU_TINY}])
    [{'foo': 'CPU_TINY'}]
    """
    if isinstance(value, dict):
        for key, v in value.items():
            value[key] = recursive_enum_to_str(v)
    elif isinstance(value, list):
        value = [recursive_enum_to_str(x) for x in value]
    elif isinstance(value, Enum):
        value = value.value
    else:
        value = value
    return value


def get_config(config_class: Type[T] | None = None) -> dict[str, Any] | T:
    """Get the config from the environment, or return the default config if none is set"""
    config_dict = json.loads(os.environ.get("CONFIG", "{}"))
    if config_class is None:
        return config_dict
    return config_class.model_validate(config_dict)


U = TypeVar("U")


def flatten(values: list[list[U]]) -> list[U]:
    """
    [1, 2, 3, 4, 5, 6]

    >>> flatten([['a', 'b'], ['c'], ['d', 'e']])
    ['a', 'b', 'c', 'd', 'e']

    >>> flatten([[1, 2], [], [3]])
    [1, 2, 3]

    >>> flatten([])
    []
    """
    return reduce(lambda a, b: a + b, values, [])
