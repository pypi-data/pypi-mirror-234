"""
Helper classes to wrap a DeepDiff object into a more usable format, allowing for easier conflict resolution.
"""
from __future__ import annotations

import abc
import re
from copy import deepcopy
from typing import Any, Literal

from deepdiff import DeepDiff
from pydantic import BaseModel

DiffType = Literal[
    "dictionary_item_added",
    "dictionary_item_removed",
    "iterable_item_added",
    "iterable_item_removed",
    "values_changed",
    "type_changes",
]


def perform_diff(base_obj: dict[str, Any], new_obj: dict[str, Any]) -> list[DiffItem]:
    """
    Performs a diff between the given objects, and returns a list of DiffItems representing the changes.

    DiffItems can only be applied to the base object, and not to the new object. This is because the new object may
    have different ordering of list values, and so applying the diff to the new object may result in a different
    result than what was intended.
    """
    diff = DeepDiff(base_obj, new_obj, ignore_order=True)
    result_diff: list[DiffItem] = []
    for key_path in diff.get("dictionary_item_added", []):
        value, path = _key_path_to_path_nodes(base_obj, new_obj, key_path, diff_type='dictionary_item_added')
        result_diff.append(DictionaryItemAdded(value=value, path=path))
    for key_path in diff.get("dictionary_item_removed", []):
        value, path = _key_path_to_path_nodes(base_obj, base_obj, key_path, diff_type='dictionary_item_removed')
        result_diff.append(DictionaryItemRemoved(value=value, path=path))
    for key_path, value in diff.get("iterable_item_added", {}).items():
        value, path = _key_path_to_path_nodes(base_obj, new_obj, key_path, diff_type='iterable_item_added')
        result_diff.append(IterableItemAdded(value=value, path=path))
    for key_path, value in diff.get("iterable_item_removed", {}).items():
        value, path = _key_path_to_path_nodes(base_obj, base_obj, key_path, diff_type='iterable_item_removed')
        result_diff.append(IterableItemRemoved(value=value, path=path))
    for key_path, value in diff.get("values_changed", {}).items():
        new_value, path = _key_path_to_path_nodes(base_obj, new_obj, key_path, diff_type='values_changed')
        old_value, _ = _key_path_to_path_nodes(base_obj, base_obj, key_path, diff_type='values_changed')
        result_diff.append(ValueChanged(new_value=new_value, old_value=old_value, path=path))
    for key_path, value in diff.get("type_changes", {}).items():
        new_value, path = _key_path_to_path_nodes(base_obj, new_obj, key_path, diff_type='type_changes')
        old_value, _ = _key_path_to_path_nodes(base_obj, base_obj, key_path, diff_type='type_changes')
        result_diff.append(TypeChanges(new_value=new_value, old_value=old_value, path=path))
    return result_diff


def _key_path_to_path_nodes(
    base_ref_obj: dict[str, Any], obj_to_walk: dict[str, Any], key_path: str, diff_type: DiffType
) -> tuple[Any, list[PathNode]]:
    """
    Returns the value at the given key path, and the path to that value as a list of PathNodes.

    :param base_ref_obj: The object to use as a reference for the path. This is used to determine the name of the
        resource at each path node if the value is an index, and also to find the relevant index of the value in the
        object to walk, in case the list items are in a different order.
    :param obj_to_walk: The object to walk to find the value at the given key path.
    :param key_path: The key path to walk to find the value.
    """
    keys = _parse_keys(key_path)
    path: list[PathNode] = []

    # We walk both the base ref object and the object to walk at the same time, so that we can get the correct index
    # of the item in the object to walk based on base object index, in case the ordering of list items has changed.
    base_ref_walked_obj: Any = base_ref_obj
    current_walked_obj: Any = obj_to_walk

    total_keys = len(keys)
    for key_idx, current_key in enumerate(keys):
        obj_to_walk_key = current_key
        if isinstance(current_key, str):
            # If this is the last key, and we're adding a dict item, just walk the current object and return
            # so that we don't get a missing key when traversing the base ref object
            if key_idx == total_keys - 1:
                path.append(PathNodeKey(key=current_key))
                return current_walked_obj[current_key], path

            # Otherwise, add to the path and continue traversing
            path.append(PathNodeKey(key=current_key, ref_value=base_ref_walked_obj[current_key]))
        elif isinstance(current_key, int):
            # If this is the last key, and we're adding a list item, walk the current object and return
            # since the base ref object won't have the index yet, and we'd hit an out-of-bounds error
            if key_idx == total_keys - 1:
                name = _get_name(current_walked_obj[current_key])
                path.append(PathNodeIndex(index=current_key, name=name))
                return current_walked_obj[current_key], path

            # The following logic is to handle when the ordering of list items has changed from the base object.
            # In this case, we first get the name of the item at the current index in the base ref object
            name = _get_name(base_ref_walked_obj[current_key])

            # Verify if list order changed by walking the rest of the current object to a deeper level. If a key is not
            # present, we should update the key to the index of the item with the given name.
            copy_current_walked_obj = deepcopy(current_walked_obj)[obj_to_walk_key]
            for key in keys[key_idx + 1 :]:
                if key not in copy_current_walked_obj:
                    obj_to_walk_key = _get_index_from_name(name, current_walked_obj)
                    break
                copy_current_walked_obj = copy_current_walked_obj[key]

            path.append(PathNodeIndex(index=current_key, name=name, ref_value=base_ref_walked_obj[current_key]))
        else:
            raise ValueError(f"Unexpected type {type(current_key)}")

        # Update the walked objects
        base_ref_walked_obj = base_ref_walked_obj[current_key]
        current_walked_obj = current_walked_obj[obj_to_walk_key]

    return current_walked_obj, path


def _get_index_from_name(name: str, obj: list[Any]) -> int:
    """
    Returns the index of the item with the given name in the given list.

    :param name: The name of the item to find.
    :param obj: The list to search.
    """
    for i, item in enumerate(obj):
        if _get_name(item) == name:
            return i
    raise ValueError(f"Could not find item with name {name} in {obj}")


def _get_name(obj: Any) -> str:
    """Returns the name of the given resource, or a hash of the resource if it has no name."""
    if isinstance(obj, str):
        # If it's a string, it's value is the name
        return obj
    if isinstance(obj, int):
        # If it's an int, it's value is the name
        return str(obj)
    if isinstance(obj, list):
        # If it's a list, concat the names of all items
        return "".join([_get_name(item) for item in obj])
    if isinstance(obj, dict):
        # Name is for most resources (app specs, environments, etc.), path is for mounts
        return obj.get("name", None) or obj.get("id", None) or obj.get("path", None) or str(hash(str(obj)))
    raise ValueError(f"Cannot get name from {obj}, unexpected type {type(obj)}")


def _parse_keys(key_path: str) -> list[str | int]:
    """Parses a key path string into a list of keys."""
    """
    >>> _parse_keys("root['key1']['key2']")
    ['key1', 'key2']
    >>> _parse_keys("root['key1'][0]['key2']")
    ['key1', 0, 'key2']
    """
    return [eval(k) for k in re.findall(r"\[([^]]+)]", key_path)]


class PathNodeKey(BaseModel):
    key: str
    ref_value: Any = None  # Reference value at this node, so we can infer default type values when applying changes

    def __str__(self) -> str:
        return self.key

    @property
    def access_key(self) -> str:
        return self.key


class PathNodeIndex(BaseModel):
    index: int
    name: str
    ref_value: Any = None  # Reference value at this node, so we can infer default type values when applying changes

    def __str__(self) -> str:
        return self.name

    @property
    def access_key(self) -> str | int:
        return self.index


PathNode = PathNodeKey | PathNodeIndex


class DiffItem(abc.ABC):
    def __init__(self, value: Any, path: list[PathNode]):
        self.value = value
        self.path = path

    @property
    def identifier(self) -> str:
        id_parts = []
        for path_part in self.path:
            id_parts.append(str(path_part))
        return ".".join(id_parts)

    def has_conflict(self, other: DiffItem) -> bool:
        # If the identifiers are the same, there is a conflict if the values are different
        if self.identifier == other.identifier:
            return type(self) != type(other) or self.value != other.value

        # If the identifiers overlap, there must be a conflict because the same value is being changed in both
        if self.identifier.startswith(other.identifier) or other.identifier.startswith(self.identifier):
            return True

        return False

    @abc.abstractmethod
    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        ...

    def _walk_to_last_path_node(self, root: dict[str, Any] | list[Any]) -> Any:
        current_walked_obj: Any = root
        for path_part in self.path[:-1]:
            key = path_part.access_key

            # If the key is a string and not in the current object, then it must be a new dict value, so we add it
            # to the current object using the default value for the type of the reference value.
            # e.g. we might pull mounts for a component spec from the remote, and the local spec might not have a
            # 'mounts' key yet, so we add it with an empty list as the value before traversing further.
            if isinstance(key, str) and key not in current_walked_obj:
                current_walked_obj[key] = self._get_default_value_for_type(path_part.ref_value)

            current_walked_obj = current_walked_obj[key]
        return current_walked_obj

    @staticmethod
    def _get_default_value_for_type(value: Any) -> Any:
        if isinstance(value, dict):
            return {}
        if isinstance(value, list):
            return []
        raise ValueError(f"Cannot get default value for type {type(value)}")


class DictionaryItemAdded(DiffItem):
    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        current_walked_obj = self._walk_to_last_path_node(root)
        current_walked_obj[self.path[-1].access_key] = self.value


class DictionaryItemRemoved(DiffItem):
    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        current_walked_obj = self._walk_to_last_path_node(root)
        del current_walked_obj[self.path[-1].access_key]


class IterableItemAdded(DiffItem):
    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        current_walked_obj = self._walk_to_last_path_node(root)
        current_walked_obj.append(self.value)


class IterableItemRemoved(DiffItem):
    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        current_walked_obj = self._walk_to_last_path_node(root)
        del current_walked_obj[self.path[-1].access_key]


class ValueChanged(DiffItem):
    def __init__(self, old_value: Any, new_value: Any, path: list[PathNode]):
        super().__init__(new_value, path)
        self.old_value = old_value

    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        current_walked_obj = self._walk_to_last_path_node(root)
        current_walked_obj[self.path[-1].access_key] = self.value


class TypeChanges(DiffItem):
    def __init__(self, old_value: Any, new_value: Any, path: list[PathNode]):
        super().__init__(new_value, path)
        self.old_value = old_value

    def apply_in_place(self, root: dict[str, Any] | list[Any]) -> None:
        current_walked_obj = self._walk_to_last_path_node(root)
        current_walked_obj[self.path[-1].access_key] = self.value
