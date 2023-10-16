from __future__ import annotations

import shutil
from pathlib import Path
from typing import Optional

import typer
from rich.table import Table

from ..sdk.errors import SlingshotException
from ..sdk.graphql import fragments
from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from .config.slingshot_cli import SlingshotCLIApp
from .shared import bytes_to_human_readable_size, datetime_to_human_readable, prompt_for_single_choice

MAX_ARTIFACTS_TO_SHOW = 20
LARGE_SIZE_BYTES = 2**30  # 1GB

app = SlingshotCLIApp()


@app.command(name="upload", requires_project=True)
async def upload_artifact(
    file_path: Path = typer.Argument(..., help="Path to file or folder to upload"),
    name: str = typer.Option(..., "--name", "-n", help="Artifact name for selection"),
    tags: list[str] = typer.Option([], "--tags", "-t", help="Artifact tags (optional, defaults to 'latest')"),
    no_zip: bool = typer.Option(False, "--no-zip", "-nz", help="Upload the contents of an artifact without zipping"),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Upload blob artifact"""
    if _artifact_size_checks(file_path):
        no_zip = True

    if file_path.is_dir() and not no_zip:
        # TODO: Add loading animation
        console.print(f"Zipping '{file_path}' before uploading. This could take some time...")
    artifact = await sdk.upload_artifact(
        artifact_path=file_path,
        blob_artifact_name=name,
        blob_artifact_tags=tags,
        as_zip=False if no_zip else None,  # If no_zip is unset, we pass the SDK "None" to use its auto-behavior.
    )
    if not artifact:
        raise SlingshotException(f"Failed to upload artifact: {file_path}")

    web_path_to_artifact = await sdk.web_path_util.blob_artifact(artifact)
    console.print(f"Created blob artifact: [link={web_path_to_artifact}]{artifact.name}[/link]")


def _artifact_size_checks(file_path: Path, bytes_size_to_be_large_file: int = LARGE_SIZE_BYTES) -> bool:
    """
    Returns true if the artifact is larger than LARGE_SIZE_BYTES and should fall back to no-zip mode.
    """
    artifact_size = _get_artifact_size(file_path)
    available_disk_space = _get_available_disk_space()

    # If downloading the artifact would take more space than is available on disk, raise an error
    if artifact_size > available_disk_space:
        raise SlingshotException(
            f"Uploading an artifact requires zipping it into a file first. Make sure you have "
            f"{bytes_to_human_readable_size(artifact_size)} available on disk for a zipped copy of '{file_path}'.\n"
            "Aborting."
        )

    # If the artifact is large enough, warn the user
    if artifact_size > bytes_size_to_be_large_file:
        console.print(
            f"[yellow]Warning! The requested artifact is larger than {bytes_to_human_readable_size(LARGE_SIZE_BYTES)}. "
            f"Slingshot will automatically upload it in parts rather than using archiving.[/yellow]"
        )
        return True

    return False


def _get_available_disk_space() -> int:
    """Return available disk space in bytes"""
    return shutil.disk_usage(".").free


def _get_artifact_size(file_path: Path) -> int:
    if not file_path.exists():
        raise SlingshotException(f"File not found: {file_path}. Please provide a valid file path.")
    # Check if path is a file
    if file_path.is_file():
        return file_path.stat().st_size
    else:
        # Otherwise, return the size of all files in folder
        return sum(f.stat().st_size for f in file_path.glob("**/*") if f.is_file())


def _show_artifacts_table(artifacts: list[fragments.BlobArtifact]) -> None:
    table = Table(title="Artifacts")
    table.add_column("Artifact Name", style="cyan")
    table.add_column("Tag", style="cyan")
    table.add_column("Size", style="cyan")
    table.add_column("Created At", style="cyan")
    table.add_column("Provenance", style="cyan")

    for blob_artifact in artifacts:
        upload_mount = blob_artifact.origin_mount
        provenance = (
            upload_mount
            and (
                # TODO: fetch the deep link to the deployment and provide a link to it by human-friendly name and URI.
                (upload_mount.deployment_id and f"Deployment {upload_mount.deployment_id} ({upload_mount.mount_path})")
                or (upload_mount.run_id and f"Run {upload_mount.run_id} ({upload_mount.mount_path})")
            )
            or "Upload"
        )
        rows = [
            blob_artifact.name,
            ", ".join(blob_artifact.tags),
            bytes_to_human_readable_size(blob_artifact.bytes_size),
            datetime_to_human_readable(blob_artifact.created_at),
            provenance,
        ]
        table.add_row(*rows)
    console.print(table)


@app.command(name="list", requires_project=True)
async def list_artifacts(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Artifact name"),
    *,
    sdk: SlingshotSDK,
    show_system: bool = typer.Option(False, "--system", "-s", help="Show system artifacts"),
    all_: bool = typer.Option(False, "--all", "-a", help="Show all artifacts and more details"),
) -> None:
    """List blob artifacts

    If --name is provided, only blob artifacts with the matching name will be returned.

    By default, only user-generated artifacts are shown. To show system artifacts (code), use --system.
    """
    artifacts = await sdk.list_artifacts(name=name)  # TODO: Paginate in SDK, not CLI
    if not artifacts:
        raise SlingshotException("No artifacts found.")

    if not show_system:
        artifacts = [a for a in artifacts if "code" not in a.tags]

    artifacts_ = artifacts if all_ else artifacts[:MAX_ARTIFACTS_TO_SHOW]
    _show_artifacts_table(artifacts_)
    if not all_ and len(artifacts) > len(artifacts_):
        console.print(f"Showing {len(artifacts_)} of {len(artifacts)} artifacts. Use --all to show all.")


@app.command(name="download", requires_project=True)
async def download_artifact(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Artifact name"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Artifact tag"),
    output_path: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help=(
            "Path to save the artifact contents to. In no-zip mode, this is the directory to save the artifact's "
            "contents into. If unspecified, the name of the artifact will be used to determine an appropriate path."
        ),
    ),
    no_zip: bool = typer.Option(
        False, "--no-zip", "-nz", help="Download the artifact as individual files rather than a single zip"
    ),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Download blob artifact

    If --name is provided, only blob artifacts with the matching name will be shown.
    If --tag is provided, selects the artifact with the matching tag, otherwise defaults to 'latest'.
    """

    if name is None:
        artifacts = await sdk.list_artifacts(name=name)
        if not artifacts:
            raise SlingshotException("No artifacts found")

        # Prompt user to select artifact
        artifact_display_names = [f"{a.name} ({', '.join(a.tags)})" if a.tags else a.name for a in artifacts]
        index = prompt_for_single_choice(
            "Select an artifact to download", artifact_display_names, skip_if_one_value=False
        )
        artifact_id = artifacts[index].blob_artifact_id
    else:
        blob_artifact = await sdk.get_artifact(blob_artifact_name=name, blob_artifact_tag=tag)
        if not blob_artifact:
            raise SlingshotException(f"Could not find artifact '{name}'")
        artifact_id = blob_artifact.blob_artifact_id

    save_filename = await sdk.download_artifact(
        artifact_id, save_path=output_path, prompt_overwrite=True, no_zip=no_zip
    )
    console.print(f"Artifact saved to {save_filename}")
