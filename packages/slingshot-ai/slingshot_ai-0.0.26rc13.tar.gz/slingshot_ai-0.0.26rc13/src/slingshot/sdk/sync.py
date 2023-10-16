from __future__ import annotations

import os
import typing
import zipfile
from io import BytesIO
from logging import getLogger
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

import sh  # type: ignore
import typer
from pathspec import GitIgnoreSpec, PathSpec
from sh import CommandNotFound, ErrorReturnCode

from slingshot import schemas
from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.utils import bytes_to_str, console, md5_hash
from slingshot.shared.utils import enter_path, get_data_or_raise

if typing.TYPE_CHECKING:
    from slingshot.sdk import SlingshotSDK

logger = getLogger(__name__)
app = typer.Typer()

ROOT_SUFFIX_TO_IGNORE = ["__pycache__", ".egg-info", ".slingshot"]

MAX_FILESIZE = 100_000  # 100KiB in bytes

MAX_FILESIZE_LARGE = 1_000_000  # 1MiB in bytes

MAX_TOTAL_SIZE = 10_000_000  # 10MiB in bytes

MAX_NUM_FILES = 1000


def should_skip_root(root: str) -> bool:
    return any(root.endswith(suffix) for suffix in ROOT_SUFFIX_TO_IGNORE)


def _zip_artifact_recursive(
    zf: zipfile.ZipFile, *, quiet: bool, destination_path: Path, exclude_paths: PathSpec
) -> None:
    """
    Zip the files in the current working directory, recursively. Excludes files based on size and git metadata:
      - Ignored files are skipped unless they're committed, in which case they're limited at MAX_FILESIZE
      - Files that are neither ignored nor committed are included, limited at MAX_FILESIZE
      - Otherwise, files are limited at MAX_FILESIZE_LARGE
    """
    try:
        _zip_with_git_ls(quiet, zf, destination_path, exclude_paths=exclude_paths)
    except (CommandNotFound, ErrorReturnCode):
        _zip_legacy(quiet, zf, destination_path, exclude_paths=exclude_paths)


def _zip_legacy(quiet: bool, zf: zipfile.ZipFile, destination_path: Path, exclude_paths: PathSpec) -> None:
    if not quiet:
        console.print("[yellow]Using legacy code push strategy[/yellow]. (Make sure 'git' is on your PATH to resolve.)")

    for root, dirs, files in os.walk("."):
        if should_skip_root(root):
            continue
        if len(files) > MAX_NUM_FILES:
            console.print(f"Sync directory has too many files: '{root}' ⚠️. Skipping this directory.", style="yellow")
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if exclude_paths.match_file(file_path):
                logger.debug(f"Excluding {file_path} as it matched exclude paths")
                continue

            size = os.path.getsize(file_path)
            if size > MAX_FILESIZE:
                relative_path = os.path.relpath(file_path)
                if not quiet:
                    console.print(
                        f"Skipping '{relative_path}' because it is too large ({bytes_to_str(size)}) ⚠️", style="yellow"
                    )
                continue
            zf.write(file_path, arcname=os.path.join(destination_path, file_path))


def _zip_with_git_ls(quiet: bool, zf: zipfile.ZipFile, destination_path: Path, exclude_paths: PathSpec) -> None:
    tracked_files = set(Path(path) for path in sh.git("ls-files").splitlines())
    untracked_files = set(Path(path) for path in sh.git("ls-files", "-o", "--exclude-standard").splitlines())
    for root, dirs, files in os.walk("."):
        if should_skip_root(root):
            continue

        for file in files:
            file_path = Path(os.path.join(root, file))
            if exclude_paths.match_file(file_path):
                logger.debug(f"Excluding {file_path} as it matched exclude paths")
                continue

            size = os.path.getsize(file_path)
            if file_path in tracked_files:
                if size > MAX_FILESIZE_LARGE:
                    relative_path = os.path.relpath(file_path)
                    if not quiet:
                        console.print(
                            f"Skipping '{relative_path}' because it is too large ({bytes_to_str(size)}) ⚠️",
                            style="yellow",
                        )
                    continue
                zf.write(file_path, arcname=os.path.join(destination_path, file_path))
            elif file_path in untracked_files:
                if size > MAX_FILESIZE:
                    relative_path = os.path.relpath(file_path)
                    if not quiet:
                        console.print(
                            f"Skipping '{relative_path}' because it is too large ({bytes_to_str(size)}) ⚠️",
                            style="yellow",
                        )
                    continue
                zf.write(file_path, arcname=os.path.join(destination_path, file_path))


async def push_code(
    sdk: SlingshotSDK,
    source_mappings: list[schemas.SourceMapping],
    description: Optional[str],
    quiet: bool = False,
    prepare_only: bool = False,  # If true, we only produce a local zip file, we do not upload it
) -> tuple[schemas.UploadedSourceCode, bool]:
    source_mappings = normalize_source_mappings(source_mappings)
    zip_bytes = zip_code_artifact(source_mappings)

    if not prepare_only:
        return await upload_source_code_if_modified(sdk, zip_bytes=zip_bytes, description=description, quiet=quiet)
    else:
        console.print("Writing source code to code.zip")
        artifact_path = Path(".") / "code.zip"
        with open(artifact_path, "wb") as f:
            f.write(zip_bytes)
        return schemas.UploadedSourceCode(source_code_id="dry-run", source_code_name="dry-run"), False


async def upload_source_code_if_modified(
    sdk: SlingshotSDK, zip_bytes: bytes, description: Optional[str], quiet: bool = False
) -> tuple[schemas.UploadedSourceCode, bool]:
    # Check if the code is already uploaded
    local_code_hash = md5_hash(zip_bytes)
    project_id = await sdk._get_current_project_id_or_raise()
    latest_source_code = await sdk.api.get_latest_source_codes_for_project(project_id)
    if latest_source_code is not None and latest_source_code.blob_artifact.bytes_hash == local_code_hash:
        console.print(f"Code hasn't changed. Skipping upload.")
        return (
            schemas.UploadedSourceCode(
                source_code_id=latest_source_code.source_code_id, source_code_name=latest_source_code.blob_artifact.name
            ),
            False,
        )

    num_bytes = len(zip_bytes)
    console.print(f"Pushing code to Slingshot ({bytes_to_str(num_bytes)})...")
    # Save zip_bytes to a temporary file
    with TemporaryDirectory() as tmpdir:
        artifact_path = Path(tmpdir) / "code.zip"
        with open(artifact_path, "wb") as f:
            f.write(zip_bytes)
        artifact = await sdk.upload_artifact(
            artifact_path=artifact_path, blob_artifact_name="code", as_zip=True, quiet=quiet
        )
    if not artifact:
        raise SlingshotException("Failed to upload code to Slingshot")
    resp = await sdk.api.upload_source_code(artifact.blob_artifact_id, description, project_id=project_id)
    uploaded_source_code_resp = get_data_or_raise(resp)
    return uploaded_source_code_resp, True


def zip_code_artifact(source_mappings: list[schemas.SourceMapping], *, quiet: bool = False) -> bytes:
    """Zip the files in the current working directory, recursively. If the working directory is within a
    git repository, zip only the files that are in the directory and in the repository."""
    with BytesIO() as zip_io:
        with zipfile.ZipFile(zip_io, "w") as zf:
            for source_mapping in source_mappings:
                logger.debug(f"Zipping up {source_mapping.local_path.absolute()}...")
                if not os.path.isdir(source_mapping.local_path):
                    raise SlingshotException(
                        f"Unable to collect sources, '{source_mapping.local_path}' does not exist or is not a directory ⚠️. "
                    )

                with enter_path(source_mapping.local_path):
                    exclude_paths = GitIgnoreSpec.from_lines(source_mapping.exclude_paths)
                    _zip_artifact_recursive(
                        zf, quiet=quiet, destination_path=source_mapping.remote_path, exclude_paths=exclude_paths
                    )

        bytes_ = zip_io.getvalue()
        if len(bytes_) > MAX_TOTAL_SIZE:
            raise SlingshotException(f"Sync directory is too large ({len(bytes_)} bytes) ⚠️. ")
        return bytes_


def normalize_source_mappings(
    source_mappings: list[schemas.SourceMapping], *, warn_if_present: bool = True
) -> list[schemas.SourceMapping]:
    """
    Normalize source mappings. This applies automatic exclude patterns so that "shadowed" directories are not included
    for push and sync, e.g. if the following mappings are used:

    - path: .:.
    - path: ../other:other

    ... then the first rule is modified to exclude "other", if such a subdirectory exists to avoid conflict. The rule
    with the most specific remote directory takes priority over less specific ones regardless of declared order.
    """
    result: list[schemas.SourceMapping] = []
    remotes_to_exclude: list[Path] = []
    for mapping in sorted(source_mappings, key=lambda sm: len(sm.remote_path.parts), reverse=True):
        # Is this remote path a parent of any of the existing remote paths? If so, exclude the corresponding local
        # directory automatically.
        added_excludes: list[str] = []
        for remote_to_exclude in remotes_to_exclude:
            current_ignore_spec = GitIgnoreSpec.from_lines(mapping.exclude_paths)
            if mapping.remote_path in remote_to_exclude.parents:
                # There's a potential conflict here, exclude this directory from the _source_ of the current path
                rel = remote_to_exclude.relative_to(mapping.remote_path)
                source_path = mapping.local_path / rel

                # Do we already have this directory explicitly excluded? If so don't bother adding a rule and don't
                # complain about it.
                already_excluded = current_ignore_spec.match_file(source_path)

                if not already_excluded:
                    added_excludes.append(str(rel))
                    # Inform the user that we just saved them from themselves, if this file/directory does in fact exist
                    if warn_if_present and os.path.exists(source_path):
                        console.print(
                            f"Detected overlapping source directories, '{source_path}' has been automatically "
                            f"excluded from '{mapping.path}' as it conflicts with another path mapping ⚠️",
                            style="yellow",
                        )
        # Now exclude this one from future ones
        remotes_to_exclude.append(mapping.remote_path)

        # ... and remember our updated definition
        result.append(
            schemas.SourceMapping.model_construct(
                path=mapping.path, exclude_paths=[*mapping.exclude_paths, *added_excludes]
            )
        )

    return result
