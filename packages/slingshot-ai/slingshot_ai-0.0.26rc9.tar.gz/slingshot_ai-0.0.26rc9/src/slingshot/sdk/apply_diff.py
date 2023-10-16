from logging import getLogger

import sentry_sdk

from slingshot import schemas
from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.utils import edit_slingshot_yaml, recursive_enum_to_str
from slingshot.sdk.wrapped_diff import (
    DictionaryItemAdded,
    DictionaryItemRemoved,
    DiffItem,
    IterableItemAdded,
    IterableItemRemoved,
    TypeChanges,
    ValueChanged,
    perform_diff,
)
from slingshot.shared.config import load_slingshot_project_config

logger = getLogger(__name__)


def compute_project_manifest_diff(base: schemas.ProjectManifest, reference: schemas.ProjectManifest) -> list[DiffItem]:
    """Computes the diff between two manifests by converting to dicts."""
    try:
        return perform_diff(
            recursive_enum_to_str(base.model_dump(exclude_local_only=True)),
            recursive_enum_to_str(reference.model_dump(exclude_local_only=True)),
        )
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise SlingshotException(f"Error computing diff, please contact Slingshot support for help") from e


def detect_local_remote_diff_conflicts(local_diff: list[DiffItem], remote_diff: list[DiffItem]) -> bool:
    """
    Checks if there are any conflicts between the local and remote diffs. Returns True if there are conflicts.
    Iterates through all pairs of diff items, and checks if any pair has a conflict with each other.
    """
    for local_item in local_diff:
        for remote_item in remote_diff:
            if local_item.has_conflict(remote_item):
                return True
    return False


def apply_diff_to_local_manifest(
    diff: list[DiffItem], reference_manifest: schemas.ProjectManifest, force: bool = False
) -> None:
    """
    Apply a diff to the local slingshot.yaml file in-place.
    If `force`, just use the reference manifest - completely ignore the local slingshot.yaml file.
    """
    if force:
        local_manifest = load_slingshot_project_config()
        diff = compute_project_manifest_diff(local_manifest, reference_manifest)

    with edit_slingshot_yaml(raise_if_absent=False) as local_slingshot_yaml:
        for item in diff:
            item.apply_in_place(local_slingshot_yaml)


def diff_to_str(diff: list[DiffItem]) -> str:
    """Converts a diff to a human-readable string."""
    changes = [item for item in diff if isinstance(item, (ValueChanged, TypeChanges))]
    additions = [item for item in diff if isinstance(item, (DictionaryItemAdded, IterableItemAdded))]
    removals = [item for item in diff if isinstance(item, (DictionaryItemRemoved, IterableItemRemoved))]
    change_lines = (
        "\n".join([f" [blue](~)[/blue] {_diff_item_to_str(change)}" for change in changes]) + "\n" if changes else ""
    )
    addition_lines = (
        "\n".join([f" [green](+)[/green] {_diff_item_to_str(add)}" for add in additions]) + "\n" if additions else ""
    )
    removal_lines = (
        "\n".join([f" [red](-)[/red] {_diff_item_to_str(removal)}" for removal in removals]) + "\n" if removals else ""
    )
    return f"{change_lines}{addition_lines}{removal_lines}"


def _diff_item_to_str(diff_item: DiffItem) -> str:
    """Converts a single diff item to a human-readable string."""
    assert len(diff_item.path) >= 1, "Diff item path must have at least one element"

    component_type = str(diff_item.path[0])
    if len(diff_item.path) == 1:
        return f"Project {diff_item.path[0]} changed"

    name = str(diff_item.path[1])
    rest_strs = [str(path) for path in diff_item.path[2:]]
    rest_change_str = " -> ".join(rest_strs)
    if rest_change_str:
        rest_change_str = f" {rest_change_str}"

    post_change_str = ""
    if isinstance(diff_item, (ValueChanged, TypeChanges)):
        post_change_str = f" changed from '{diff_item.old_value}' to '{diff_item.value}'"
    elif isinstance(diff_item, (DictionaryItemAdded, IterableItemAdded)):
        post_change_str = f" added"
    elif isinstance(diff_item, (DictionaryItemRemoved, IterableItemRemoved)):
        post_change_str = f" deleted"

    if component_type == "environments":
        return f"Environment '{name}' ->{rest_change_str}{post_change_str}"
    elif component_type == "apps":
        return f"App '{name}' ->{rest_change_str}{post_change_str}"
    elif component_type == "deployments":
        return f"Deployment '{name}' ->{rest_change_str}{post_change_str}"
    elif component_type == "runs":
        return f"Run '{name}' ->{rest_change_str}{post_change_str}"

    raise ValueError(f"Unknown change type: {component_type}")
