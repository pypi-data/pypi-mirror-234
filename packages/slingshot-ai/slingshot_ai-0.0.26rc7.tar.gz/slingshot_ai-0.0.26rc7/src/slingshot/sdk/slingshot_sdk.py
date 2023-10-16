from __future__ import annotations

import asyncio
import contextlib
import datetime
import functools
import glob
import os
import shutil
import time
import typing
import uuid
from asyncio import wait_for
from functools import wraps
from logging import getLogger
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

import typer
from aiohttp import ClientOSError
from tqdm.auto import tqdm

from slingshot import schemas
from slingshot.sdk import config
from slingshot.sdk.errors import (
    SlingshotCodeNotFound,
    SlingshotException,
    SlingshotNoProjectSetError,
    SlingshotUnauthenticatedError,
)
from slingshot.sdk.sync import normalize_source_mappings
from slingshot.sdk.upload_download_utils import download_file_in_parts, upload_file_in_parts_to_gcs
from slingshot.slingshot_version import __version__

from ..cli.shared import format_logline
from ..schemas import CreateServiceAccountResponse, Hyperparameter, LogLine, Response, SshPort
from ..shared.utils import get_data_or_raise
from .apply import ApplyService
from .auth import login_auth0
from .config import global_config, project_config
from .graphql import fragments
from .slingshot_api import JSONType, SlingshotAPI, SlingshotClient, gather_with_concurrency
from .sync import push_code, zip_code_artifact
from .utils import console, md5_hash
from .web_path_util import WebPathUtil

logger = getLogger(__name__)

Function = typing.TypeVar("Function", bound=typing.Callable[..., typing.Awaitable[typing.Any]])

BYTES_PER_MB = 1024 * 1024


def experimental(f: Function) -> Function:
    """Decorator for experimental functions"""

    @wraps(f)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        # TODO: Implement some kind of warning
        return f(*args, **kwargs)

    return typing.cast(Function, wrapper)


class SlingshotSDK:
    def __init__(self, verbose: bool = False, slingshot_url: str = config.global_config.slingshot_backend_url) -> None:
        self._me: fragments.MeResponse | None = None
        self.verbose = verbose
        self.project_id = project_config.project_id
        self.project: schemas.Project | None = None
        self._client = SlingshotClient(
            auth_token=global_config.auth_token, slingshot_url=slingshot_url, auto_setup_hook=self.setup
        )
        self._api = SlingshotAPI(client=self._client)
        self.web_path_util = WebPathUtil(self, slingshot_url=slingshot_url)

    @property
    def api(self) -> SlingshotAPI:
        # TODO: Remove this
        return self._api

    @contextlib.asynccontextmanager
    async def use_session(self) -> typing.AsyncGenerator[SlingshotSDK, None]:
        """Optional: Use this to reuse a session across multiple requests."""
        async with self._api.use_http_session():
            yield self

    """
    Boilerplate SDK methods
    """

    async def setup(self) -> None:
        """
        This is called automatically when you run certain commands, or in the CLI.
        It checks for updates, sets the project, and signs in service accounts
        Auto setup for scripts, based on env variables. Can safely be called multiple times.
        """
        await self.check_for_updates()
        if not self._client.auth_token and (slingshot_api_key := os.environ.get("SLINGSHOT_API_KEY", None)):
            auth_token = await self._api.sa_login(slingshot_api_key)
            logger.info("Signed in successfully using API key.")
            self._client.auth_token = schemas.AuthTokenUnion.from_service_account_token(auth_token)

        # Get the project from the environment variable, if available
        if (
            self._client.auth_token  # Signed in
            and not self.project
            and (project_id := os.environ.get("SLINGSHOT_PROJECT_ID", None))
        ):
            project = await self._api.get_project_by_id(project_id, _setup=False)
            if project is None:
                logger.debug(f"Project with id {project_id} not found.")
                return
            self.project = project
            self.project_id = project.project_id

    async def check_for_updates(self, *, force: bool = False) -> bool:
        """
        Check if the backend has a newer version of Slingshot than the SDK.
        Returns True if there is a newer version, False otherwise.
        """

        if (
            global_config.last_checked_for_updates is not None
            and (time.time() - global_config.last_checked_for_updates < global_config.check_for_updates_interval)
        ) and not force:
            return False
        global_config.last_checked_for_updates = time.time()
        version = await self._api.get_backend_version()
        logger.debug(f"Current version: {__version__}, backend version: {version}")
        if version != __version__:
            console.print(
                f"🎉 A new version of Slingshot is available, "
                f"run [cyan]pip install slingshot-ai=={version}[/cyan] to install the latest version"
            )
            return True
        return False

    """
    Auth SDK methods
    """

    async def login(self) -> None:
        """Login to Slingshot"""
        me: fragments.MeResponse | None = None
        try:
            me = await self.me()
        except SlingshotUnauthenticatedError:
            pass
        except SlingshotException as e:
            console.print(e.args[0], style="red")

        if me:
            service_account_str = me.service_account and (
                me.service_account.nickname or me.service_account.service_account_id
            )
            me_str = (
                f"{me.user.display_name} ({me.user.username})"
                if me.user
                else f"service account '{service_account_str}'"
            )
            console.print(f"You are already logged in as {me_str}")
            console.print("Run 'slingshot logout' to log out.")
            return

        cli_metadata_resp = await self._api.get_auth0_cli_metadata()
        cli_metadata = get_data_or_raise(cli_metadata_resp)

        token = login_auth0(cli_metadata.auth0_domain, cli_metadata.auth0_client_id)
        auth_token = await self._api.user_login(token)
        self.set_auth_token(auth_token)

    def logout(self) -> None:
        """Logout of Slingshot"""
        if not global_config.auth_token:
            console.print("Not signed in")
            return

        global_config.auth_token = None
        self._client.auth_token = None

    async def is_signed_in(self) -> bool:
        """Check the auth status"""
        if not global_config.auth_token:
            return False
        try:
            self._me = await self.me()
        except SlingshotException:
            return False
        return True

    def set_auth_token(self, auth_token: schemas.AuthToken, update_config: bool = True) -> None:
        """Set the auth token"""
        auth_token_union = schemas.AuthTokenUnion.from_auth_token(auth_token)
        self._client.auth_token = auth_token_union
        if update_config:
            global_config.auth_token = auth_token_union

    async def create_service_account(self) -> CreateServiceAccountResponse:
        """Create a new service account for a project, returning a secure API key used to act on behalf of it"""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.create_service_account(project_id)

    """
    User SDK methods
    """

    async def me(self) -> fragments.MeResponse | None:
        """Get the current user"""
        if not self._client.auth_token:
            return None

        if self._client.auth_token.is_user:
            assert self._client.auth_token.user_id is not None, "User ID is missing"
            return fragments.MeResponse.from_user(await self._api.me_user(user_id=self._client.auth_token.user_id))
        elif self._client.auth_token.is_service_account:
            assert self._client.auth_token.service_account_id is not None, "Service account ID is missing"
            return fragments.MeResponse.from_service_account(
                await self._api.me_service_account(service_account_id=self._client.auth_token.service_account_id)
            )
        else:
            raise SlingshotException("Unknown auth token type")

    async def set_ssh(self, ssh_key: str) -> None:
        """Set the SSH key for the current user"""
        await self._api.update_ssh_public_key(ssh_key)

    """
    Project SDK methods
    """

    async def use_project(self, project_id: str) -> None:
        """Set the current project"""
        project_fields = await self._api.get_project_by_id(project_id)
        if not project_fields:
            raise SlingshotException(
                f"Project '{project_id}' not found on Slingshot. "
                "Run 'slingshot init' to create a project or 'slingshot use' to connect to an existing one."
            )
        self.project = project_fields
        project_config.project_id = project_id

    async def apply_project(self, force: bool = False) -> bool:
        """
        Apply the YAML configuration in the current directory to the current project.

        Returns True if any changes were applied, False otherwise.
        """
        return await ApplyService(self).apply(force=force)

    async def pull_remote_changes(self, force: bool = False) -> bool:
        """
        Pull the YAML configuration from the remote project to the current project.

        Returns True if any changes were pulled.
        """
        return await ApplyService(self).check_conflicts_pull_remote_changes(force=force)

    """
    Source code SDK methods
    """

    async def push_code(
        self,
        source_mappings: list[schemas.SourceMapping],
        description: Optional[str] = None,
        and_print: bool = False,
        prepare_only: bool = False,  # If true, we only produce a local zip file, we do not upload it
    ) -> schemas.UploadedSourceCode:
        """Push source code with the specified mappings to Slingshot."""
        created_source_code, is_new = await push_code(
            self, source_mappings, description, quiet=not and_print, prepare_only=prepare_only
        )
        if and_print and not prepare_only:
            source_code_name = created_source_code.source_code_name
            link = await self.web_path_util.code(created_source_code)
            if is_new:
                console.print(f"Pushed new source code '{source_code_name}', view in browser at {link}")
            else:
                # No changes
                console.print(f"No changes to source code '{source_code_name}', view in browser at {link}")
        return created_source_code

    async def has_code_changed(self, source_mappings: list[schemas.SourceMapping]) -> bool:
        """Check if the code has changed since the last sync"""
        source_mappings = normalize_source_mappings(source_mappings)
        project_id = await self._get_current_project_id_or_raise()
        zip_bytes = zip_code_artifact(source_mappings, quiet=True)
        bytes_hash = md5_hash(zip_bytes)

        latest_source_code = await self._api.get_latest_source_codes_for_project(project_id)
        if not latest_source_code or not latest_source_code.blob_artifact.bytes_hash:
            return True

        latest_bytes_hash = latest_source_code.blob_artifact.bytes_hash
        return latest_bytes_hash != bytes_hash

    """
    Artifact SDK methods
    """

    async def _process_signed_url_download(
        self, url_response: schemas.BlobArtifactSignedURL, *, save_path: str | None, prompt_overwrite: bool = False
    ) -> str:
        signed_url = url_response.signed_url
        blob_filename = url_response.blob_filename
        if save_path:
            download_filepath = save_path

            # TODO: should we consider checking all file-types, i.e. what remains after the final "."?
            if save_path.endswith(".zip") ^ blob_filename.endswith(".zip"):
                console.print(
                    f"[yellow]Warning:[/yellow] downloading artifact to the requested '{save_path}' but detected that "
                    f"this may not match the artifact's type (the remote file is named '{blob_filename}'). You may "
                    f"wish to rename the file before using it. If uncertain, running 'file {save_path}' may be helpful "
                    "for detecting the content-type. This warning can be resolved by omitting the '--output' flag."
                )
        else:
            blob_name = url_response.blob_artifact_name
            download_filepath = f"{blob_name}/{blob_filename}"

        # Check if file already exists for overwriting
        while prompt_overwrite and os.path.exists(download_filepath):
            # Prompt the user to overwrite the file
            overwrite = typer.confirm(f"File {download_filepath} already exists. Do you wish to overwrite?")
            if overwrite:
                break
            download_filepath = typer.prompt("Please enter a new filename")

        Path(download_filepath).parent.mkdir(parents=True, exist_ok=True)
        await download_file_in_parts(download_filepath, signed_url=signed_url, client=self._client)
        return download_filepath

    async def download_artifact(
        self,
        blob_artifact_id: str,
        save_path: str | None = None,
        prompt_overwrite: bool = False,
        no_zip: bool = False,
        no_zip_batch_size: int = 5,
    ) -> str:
        """
        Download an artifact from the current project.

        @param blob_artifact_id: The ID of the blob artifact to download
        @param save_path: The path to save the artifact to. If not provided, the artifact will be saved using the blob
        artifact name and file path.
        @param prompt_overwrite: Whether to prompt the user to overwrite the file if it already exists
        @param no_zip: Whether to download the artifact as individual files rather than a single zip
        @param no_zip_batch_size: The number of files to download in each batch when downloading in no-zip mode
        """
        project_id = await self._get_current_project_id_or_raise()
        if no_zip:
            blob_artifacts_response = await self._api.signed_url_blob_artifact_many(
                blob_artifact_id, project_id=project_id
            )

            list_response = get_data_or_raise(blob_artifacts_response)
            # TODO: Consider using TCPConnector limit to limit the number of concurrent connections rather than using
            #  gather_with_concurrency.
            results = await gather_with_concurrency(
                no_zip_batch_size,
                *[
                    self._process_signed_url_download(
                        url_response,
                        # In no_zip mode, download all the files into a directory. The directory should be the
                        #  blob artifact name if a save_path is not provided. Inside the directory should be each of
                        #  the files. Note that if we get this path wrong, we will blat file chunks arbitrarily and
                        #  not detect corruption or file count variability. TODO: we should compare metadata after
                        #  downloading to ensure we have the right number of files and the right file hashes.
                        save_path=f"{save_path or url_response.blob_artifact_name}/{url_response.file_path}",
                        prompt_overwrite=False,
                    )
                    for url_response in list_response
                ],
            )
            for res in results:
                console.print(f"Completed processing {res}")
            return save_path or (list_response and list_response[0].blob_artifact_name) or ""

        # Check the blob artifact size before proceeding in zipped mode.
        blob_artifact_response = await self._api.get_blob_artifact_by_id(blob_artifact_id)

        if not blob_artifact_response:
            raise SlingshotException(f"Blob artifact {blob_artifact_id} not found")

        if not blob_artifact_response.bytes_size:
            raise SlingshotException(
                f"Blob artifact {blob_artifact_id} may be corrupt -- contact slingshot support for help."
            )

        if blob_artifact_response.bytes_size > 100 * BYTES_PER_MB:
            console.print("Artifact too large to zip -- downloading in non-zip mode.")
            return await self.download_artifact(blob_artifact_id, save_path, prompt_overwrite, no_zip=True)

        blob_artifact_url_response = await self._api.signed_url_blob_artifact(blob_artifact_id, project_id=project_id)

        url_response = get_data_or_raise(blob_artifact_url_response)

        return await self._process_signed_url_download(
            url_response, save_path=save_path, prompt_overwrite=prompt_overwrite
        )

    async def _process_signed_url_upload(
        self,
        *,
        filename: str,
        blob_artifact_name: str,
        blob_artifact_tags: list[str] | None = None,
        as_zip: bool,
        project_id: str,
        artifact_path: Path,
        quiet: bool = False,
    ) -> fragments.BlobArtifact:
        resp = await self._api.upload_signed_url_blob_artifact(
            filename,
            artifact_name=blob_artifact_name,
            artifact_tags=blob_artifact_tags,
            as_zip=as_zip,
            project_id=project_id,
        )
        upload_signed_url_response = get_data_or_raise(resp)
        upload_signed_url = upload_signed_url_response.signed_url
        blob_artifact_id = upload_signed_url_response.blob_artifact_id

        await upload_file_in_parts_to_gcs(
            str(artifact_path), upload_signed_url=upload_signed_url, client=self._client, quiet=quiet
        )

        # Finalize the upload once all parts have been uploaded
        finalize = await self._client.make_request(
            url=f"project/{project_id}/artifact/{blob_artifact_id}/finalize",
            method="post",
            response_model=schemas.ResponseOK,
        )
        if finalize.error:
            raise SlingshotException(finalize.error.message)

        blob_artifact = await self._api.get_blob_artifact_by_id(blob_artifact_id=blob_artifact_id)
        assert blob_artifact, "Blob artifact not found"
        return blob_artifact

    async def upload_artifact(
        self,
        artifact_path: Path,
        blob_artifact_name: str,
        blob_artifact_tags: list[str] | None = None,
        as_zip: bool | None = None,  # Defaults to True if artifact_path is a directory
        quiet: bool = False,
    ) -> fragments.BlobArtifact:
        """Upload an artifact to the current project."""
        project_id = await self._get_current_project_id_or_raise()
        if not artifact_path.exists():
            raise SlingshotException(f"File path {artifact_path} does not exist")

        if artifact_path.is_dir():
            as_zip = True if as_zip is None else as_zip

        filename = os.path.basename(artifact_path)
        if as_zip is None:
            # If filename ends with .zip, and we haven't set as_zip yet, then assume it's a zip file, otherwise must be
            #  a file.
            as_zip = filename.endswith(".zip")

        # Case 1: we are uploading a zip file from a local path
        if as_zip and filename.endswith('.zip'):
            # This is already a zip file, just upload it
            return await self._process_signed_url_upload(
                filename=filename,
                blob_artifact_name=blob_artifact_name,
                blob_artifact_tags=blob_artifact_tags,
                as_zip=as_zip,
                project_id=project_id,
                artifact_path=artifact_path,
                quiet=quiet,
            )
        elif as_zip:  # ... and not filename.endswith('.zip')
            # We're meant to upload this as a zip file, but we've been given a directory. Zip it up first.
            logger.info(f"Zipping directory {artifact_path}")
            with NamedTemporaryFile(suffix='.zip') as zip_file:
                # NOTE: make_archive will add the format suffix to the filename, so we need to remove it...
                filename_minus_format = zip_file.name.rsplit('.', 1)[0]
                shutil.make_archive(filename_minus_format, "zip", root_dir=artifact_path)
                return await self._process_signed_url_upload(
                    filename=filename,
                    blob_artifact_name=blob_artifact_name,
                    blob_artifact_tags=blob_artifact_tags,
                    as_zip=as_zip,
                    project_id=project_id,
                    artifact_path=Path(zip_file.name),
                    quiet=quiet,
                )
        elif not artifact_path.is_dir():
            # Case 2: we are uploading a non-zip of a single file.
            return await self._process_signed_url_upload(
                filename=filename,
                blob_artifact_name=blob_artifact_name,
                blob_artifact_tags=blob_artifact_tags,
                as_zip=as_zip,
                project_id=project_id,
                artifact_path=artifact_path,
                quiet=quiet,
            )
        else:
            # Case 3: we are uploading a directory in non-zipped form but producing just one artifact.
            filename_candidates = glob.glob(f"{filename}/**", recursive=True)
            filenames = [
                os.path.relpath(glob_result, Path(filename))
                for glob_result in filename_candidates
                if Path(glob_result).is_file()
            ]

            resp = await self._api.upload_signed_url_blob_artifact_many(
                filenames, artifact_name=blob_artifact_name, artifact_tags=blob_artifact_tags, project_id=project_id
            )

            upload_url_many_data = get_data_or_raise(resp)
            blob_artifact_id = upload_url_many_data.blob_artifact_id
            filename_to_signed_url = upload_url_many_data.filename_to_signed_url

            # TODO: batch these requests -- currently we are uploading all at once which is not scalable and will probably
            #  cause timeouts.
            for task in asyncio.as_completed(
                [
                    upload_file_in_parts_to_gcs(
                        f"{filename}/{rel_path}", upload_signed_url=upload_signed_url, client=self._client, quiet=quiet
                    )
                    for rel_path, upload_signed_url in filename_to_signed_url.items()
                ]
            ):
                await task

            # Finalize the upload once all parts have been uploaded
            res = await self._client.make_request(
                url=f"project/{project_id}/artifact/{blob_artifact_id}/finalize",
                method="post",
                response_model=schemas.ResponseOK,
            )
            if res.error:
                raise SlingshotException(res.error.message)

            blob_artifact_ = await self._api.get_blob_artifact_by_id(blob_artifact_id=blob_artifact_id)
            assert blob_artifact_, "Blob artifact not found"
            return blob_artifact_

    """
    Logs SDK methods
    """

    # TODO: add pagination for logs
    async def get_logs(self, *, run_id: str | None = None, spec_id: str | None = None) -> list[LogLine]:
        """Get logs for an app, run, or deployment."""
        assert sum(1 if i else 0 for i in [run_id, spec_id]) == 1, "Exactly one id must be specified"
        project_id = await self._get_current_project_id_or_raise()
        if run_id:
            logs_resp = await self._api.get_run_logs(run_id=run_id, project_id=project_id)
        else:
            assert spec_id
            logs_resp = await self._api.get_app_logs(spec_id=spec_id, project_id=project_id)
        logs = get_data_or_raise(logs_resp)
        return sorted([i for i in logs], key=lambda i: i.timestamp)

    async def follow_logs(
        self, *, run_id: str | None = None, spec_id: str | None = None, poll_interval_s: float = 2
    ) -> typing.AsyncIterator[LogLine]:
        """Follow logs for an app, run, or deployment."""
        logs_len = 0
        while True:
            try:
                logs = await self.get_logs(run_id=run_id, spec_id=spec_id)
            # Note: the websocket connection can occasionally get reset or break unexpectedly, so we should retry
            except ClientOSError:
                logger.debug(f"Failed to get logs. Retrying...")
                continue
            if logs_len < len(logs):
                for log in logs[logs_len:]:
                    yield log
                logs_len = len(logs)
            await asyncio.sleep(poll_interval_s)

    @typing.overload
    async def print_logs(self, *, run_id: str, follow: bool = ..., refresh_rate_s: float = ...) -> None:
        ...

    @typing.overload
    async def print_logs(self, *, spec_id: str, follow: bool = ..., refresh_rate_s: float = ...) -> None:
        ...

    async def print_logs(
        self, *, run_id: str | None = None, spec_id: str | None = None, follow: bool = False, refresh_rate_s: float = 3
    ) -> None:
        """Print and optionally follow the latest logs for an app, run, or deployment."""
        if follow:
            async for line in self.follow_logs(run_id=run_id, spec_id=spec_id, poll_interval_s=refresh_rate_s):
                console.print(format_logline(line))
        else:
            for line in await self.get_logs(run_id=run_id, spec_id=spec_id):
                console.print(format_logline(line))

    """
    Prediction SDK methods
    """

    async def predict(
        self, deployment_name: str, example_bytes: bytes, timeout_seconds: int = 60
    ) -> dict[str, typing.Any]:
        """Make a prediction against a deployment."""
        project = await self._get_current_project_or_raise()
        resp = await self._api.predict(
            project_id=project.project_id,
            deployment_name=deployment_name,
            example_bytes=example_bytes,
            timeout_seconds=timeout_seconds,
        )
        return get_data_or_raise(resp)

    @staticmethod
    def _maybe_raise_concrete_openai_error(error: schemas.SlingshotLogicalError) -> None:
        import openai.error

        if error.metadata and (err_type := error.metadata.get("concrete_error_type")):
            openai_concrete_error_types = {
                openai.error.ServiceUnavailableError,
                openai.error.RateLimitError,
                openai.error.AuthenticationError,
                openai.error.APIConnectionError,
                openai.error.APIError,
                openai.error.APIConnectionError,
                openai.error.InvalidAPIType,
                # openai.error.InvalidRequestError,  # TODO: this one takes two parameters so needs extra work
                openai.error.PermissionError,
                # openai.error.SignatureVerificationError,  # TODO: this one takes two parameters so needs extra work
                openai.error.Timeout,
                openai.error.TryAgain,
            }

            def _reducer(accum: dict[str, type], iter_: type) -> dict[str, type]:
                accum[iter_.__name__] = iter_
                return accum

            err_type_mapping: dict[str, type] = functools.reduce(_reducer, openai_concrete_error_types, dict())

            if err_type_ctor := err_type_mapping.get(err_type):
                raise err_type_ctor(error.message)

    @experimental
    async def prompt_openai_chat(
        # TODO: Inline the arguments here
        self,
        openai_request: schemas.OpenAIChatRequest,
        *,
        force_redo: bool = False,
        timeout: datetime.timedelta = datetime.timedelta(seconds=600),
        active_throttling: bool | int = False,
    ) -> schemas.OpenAIChatResponse:
        """Make a prediction to a chat model on OpenAI."""
        project_id = await self._get_current_project_id_or_raise()
        idempotence_key = md5_hash(openai_request.model_dump_json().encode()) if not force_redo else uuid.uuid4().hex

        request = schemas.PromptOpenAIBody(
            openai_request=openai_request, idempotence_key=idempotence_key, active_throttling=active_throttling
        )
        resp = await self._api.prompt_openai(request, timeout=timeout, project_id=project_id)
        if resp.error:
            self._maybe_raise_concrete_openai_error(resp.error)
            raise SlingshotException(resp.error.message)
        if resp.data is None:
            raise SlingshotException("No data returned from server")
        assert isinstance(resp.data, schemas.OpenAIChatResponse)
        return resp.data

    @experimental
    async def prompt_openai_text(
        # TODO: Inline the arguments here
        self,
        openai_request: schemas.OpenAICompletionRequest,
        *,
        force_redo: bool = False,
        timeout: datetime.timedelta = datetime.timedelta(seconds=600),
        active_throttling: bool | int = False,
    ) -> schemas.OpenAICompletionResponse:
        """Make a prediction to a text completion model on OpenAI."""
        project_id = await self._get_current_project_id_or_raise()
        idempotence_key = md5_hash(openai_request.model_dump_json().encode()) if not force_redo else uuid.uuid4().hex
        request = schemas.PromptOpenAIBody(
            openai_request=openai_request, idempotence_key=idempotence_key, active_throttling=active_throttling
        )
        result = await self._api.prompt_openai(request, timeout=timeout, project_id=project_id)
        if result.error:
            self._maybe_raise_concrete_openai_error(result.error)
            raise SlingshotException(result.error.message)
        if result.data is None:
            raise SlingshotException("No data returned from server")
        assert isinstance(result.data, schemas.OpenAICompletionResponse)
        return result.data

    @experimental
    async def prompt_openai_embedding(
        self,
        _input: str | list[str],
        *,
        model: str = "text-embedding-ada-002",
        force_redo: bool = False,
        timeout: datetime.timedelta = datetime.timedelta(seconds=600),
        batch_size: int = 20,
        batch_use_tqdm: bool = True,
        active_throttling: bool | int = False,
    ) -> schemas.OpenAIEmbeddingResponse:
        """
        Make a prediction to an embedding model on OpenAI.

        The response format is a pydantic model with a field called "data" (along with other metadata fields). The data
        field contains a list of embeddings produced from the request. If _input is a list of embeddings, then data will
        contain multiple embeddings, otherwise it will be a list of length 1, with the embedding for just the one input.
        """
        # Use batching for large _input:
        if isinstance(_input, list) and len(_input) > batch_size:
            chunks = [_input[i : i + batch_size] for i in range(0, len(_input), batch_size)]
            if batch_use_tqdm:
                gather_func = tqdm.gather
            else:
                gather_func = asyncio.gather  # type: ignore

            results = await gather_func(
                *[
                    self.prompt_openai_embedding(
                        chunk, model=model, force_redo=force_redo, timeout=timeout, batch_size=batch_size
                    )
                    for chunk in chunks
                ]
            )

            if len(set(result.model for result in results)) != 1:
                print("Warning: Slingshot received OpenAI responses with multiple models in chunked request.")
            if len(set(result.object for result in results)) != 1:
                print("Warning: Slingshot received OpenAI responses with multiple objects in chunked request")
            if any(result.usage.completion_tokens for result in results):
                print("Warning: Slingshot received OpenAI responses with non-zero completion tokens in chunked request")

            # Rebuild the response with the data from each chunk
            return schemas.OpenAIEmbeddingResponse(
                object=results[0].object,
                data=[embedding for result in results for embedding in result.data],
                model=results[0].model,
                usage=schemas.OpenAIUsage(
                    prompt_tokens=sum(result.usage.prompt_tokens for result in results),
                    completion_tokens=None,
                    total_tokens=sum(result.usage.total_tokens for result in results),
                ),
            )

        project_id = await self._get_current_project_id_or_raise()
        openai_request = schemas.OpenAIEmbeddingRequest(model=model, input=_input)
        idempotence_key = md5_hash(openai_request.model_dump_json().encode()) if not force_redo else uuid.uuid4().hex
        request = schemas.PromptOpenAIBody(
            openai_request=openai_request, idempotence_key=idempotence_key, active_throttling=active_throttling
        )
        result = await self._api.prompt_openai(request, timeout=timeout, project_id=project_id)
        if result.error:
            self._maybe_raise_concrete_openai_error(result.error)
            raise SlingshotException(result.error.message)
        if result.data is None:
            raise SlingshotException("No data returned from server")
        assert isinstance(result.data, schemas.OpenAIEmbeddingResponse)
        return result.data

    """
    Start SDK methods
    """

    async def start_app(self, app_name: str, source_code_id: str | None = None) -> fragments.AppInstance:
        """
        Start an app in the current project.
        """
        project_id = await self._get_current_project_id_or_raise()
        component_spec = await self._api.get_component_spec_by_name(spec_name=app_name, project_id=project_id)
        if not component_spec:
            raise SlingshotException(f"Could not find app with name {app_name}")

        if not source_code_id:
            source_code = await self._api.get_latest_source_codes_for_project(project_id=project_id)
            # Custom plugins don't need to have source code
            if not source_code and component_spec.app_sub_type is None:
                raise SlingshotCodeNotFound()
            source_code_id = source_code.source_code_id if source_code else None

        resp = await self._api.start_app(
            component_spec=component_spec, source_code_id=source_code_id, project_id=project_id
        )
        data = get_data_or_raise(resp)
        app_instance = await self._api.get_app_instance(app_instance_id=data.app_instance_id, project_id=project_id)
        if not app_instance:
            raise SlingshotException(f"Could not find app instance")
        return app_instance

    async def start_run(
        self,
        run_template_name: str,
        source_code_id: str | None = None,
        machine_size: schemas.MachineSize | None = None,
        hyperparameters: Hyperparameter | None = None,
        cmd: str | None = None,
        mount_specs: list[schemas.MountSpecUnion] | None = None,
        environment_instance_id: str | None = None,
        debug_mode: bool = False,
    ) -> fragments.Run:
        """
        Start a run in the current project.
        """
        project_id = await self._get_current_project_id_or_raise()
        run_spec = await self._api.get_component_spec_by_name(spec_name=run_template_name, project_id=project_id)
        if not run_spec or run_spec.component_type != schemas.ComponentType.RUN:
            raise SlingshotException(f"Could not find run template with name {run_template_name}")

        if not source_code_id:
            source_code = await self._api.get_latest_source_codes_for_project(project_id=project_id)
            if not source_code:
                raise SlingshotCodeNotFound()
            source_code_id = source_code.source_code_id

        resp = await self._api.start_run(
            run_spec=run_spec,
            source_code_id=source_code_id,
            machine_size=machine_size,
            hyperparameters=hyperparameters,
            cmd=cmd,
            mount_specs=mount_specs,
            environment_instance_id=environment_instance_id,
            project_id=project_id,
            debug_mode=debug_mode,
        )
        data = get_data_or_raise(resp)
        run = await self._api.get_run(run_id=data.run_id, project_id=project_id)
        if not run:
            raise SlingshotException(f"Could not find run with id {data.run_id}")
        return run

    async def start_deployment(
        self, deployment_name: str, source_code_id: str | None = None
    ) -> fragments.ComponentSpec:
        """
        Start a deployment in the current project.
        """
        project_id = await self._get_current_project_id_or_raise()
        deployment_spec = await self._api.get_component_spec_by_name(deployment_name, project_id=project_id)
        if not deployment_spec:
            raise SlingshotException(f"Could not find deployment with name {deployment_name}")

        if not source_code_id:
            source_code = await self._api.get_latest_source_codes_for_project(project_id=project_id)
            if not source_code:
                raise SlingshotCodeNotFound()
            source_code_id = source_code.source_code_id

        resp = await self._api.deploy_model(
            deployment_spec_id=deployment_spec.spec_id, source_code_id=source_code_id, project_id=project_id
        )
        if resp.error:
            raise SlingshotException(f"Could not start deployment: {resp.error.message}")

        deployment_spec = await self._api.get_component_spec_by_name(deployment_name, project_id=project_id)
        if not deployment_spec or not deployment_spec.deployments:
            raise SlingshotException(f"Could not find deployment with name {deployment_name}")
        return deployment_spec

    async def start_app_ssh(self, spec_id: str) -> Response[SshPort]:
        """Starts SSH access for an app."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.start_app_ssh(spec_id=spec_id, project_id=project_id)

    async def start_run_ssh(self, run_id: str) -> Response[SshPort]:
        """Starts SSH access for a run."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.start_run_ssh(run_id=run_id, project_id=project_id)

    """
    Stop SDK methods
    """

    async def stop_app(self, *, app_name: str) -> None:
        """
        Stop an app in the current project.
        """
        project_id = await self._get_current_project_id_or_raise()
        component_spec = await self._api.get_component_spec_by_name(spec_name=app_name, project_id=project_id)
        if not component_spec:
            raise SlingshotException(f"Could not find app with name {app_name}")
        await self._api.stop_app(spec_id=component_spec.spec_id, project_id=project_id)

    async def stop_run(self, *, run_name: str) -> None:
        """
        Stop a run in the current project.
        """
        project_id = await self._get_current_project_id_or_raise()
        run = await self._api.get_run(run_name=run_name, project_id=project_id)
        if not run:
            raise SlingshotException(f"Could not find run with name {run_name}")
        await self._api.cancel_run(run_id=run.run_id, project_id=project_id)

    async def stop_deployment(self, *, deployment_name: str) -> None:
        """
        Stop a deployment in the current project.
        """
        project_id = await self._get_current_project_id_or_raise()
        deployment_spec = await self._api.get_component_spec_by_name(deployment_name, project_id=project_id)
        if not deployment_spec:
            raise SlingshotException(f"Could not find deployment with name {deployment_name}")
        await self._api.stop_deployment(deployment_spec_id=deployment_spec.spec_id, project_id=project_id)

    """
    List SDK methods
    """

    async def list_projects(self) -> list[fragments.ProjectFields]:
        """List all projects."""
        if not await self.is_signed_in():
            raise SlingshotUnauthenticatedError()

        me = await self.me()
        assert me is not None, "User is not signed in"
        return me.projects

    async def list_components(self) -> list[fragments.ComponentSpec]:
        """List all components in the current project."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.list_component_specs(project_id)

    async def list_run_templates(self) -> list[fragments.ComponentSpec]:
        """List all runs templates in the current project."""
        project_id = await self._get_current_project_id_or_raise()
        existing_component_specs = await self._api.list_component_specs(project_id=project_id)
        return [
            component_spec
            for component_spec in existing_component_specs
            if component_spec.component_type == schemas.ComponentType.RUN
        ]

    async def list_runs(self) -> list[fragments.Run]:
        """List all runs in the current project."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.list_runs(project_id)

    async def list_deployments(self) -> list[fragments.ComponentSpec]:
        """List all deployments in the current project."""
        project_id = await self._get_current_project_id_or_raise()
        existing_component_specs = await self._api.list_component_specs(project_id=project_id)
        return [
            component_spec
            for component_spec in existing_component_specs
            if component_spec.component_type == schemas.ComponentType.DEPLOYMENT
        ]

    async def list_environments(self) -> list[fragments.ExecutionEnvironmentSpec]:
        """List all environments in the current project."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.list_environment_specs(project_id=project_id)

    async def list_artifacts(self, name: str | None = None) -> list[fragments.BlobArtifact]:
        """List all artifacts in the current project."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.list_artifacts(name, project_id=project_id)

    async def list_volumes(self) -> list[fragments.Volume]:
        """List all volumes in the current project."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.list_volumes(project_id=project_id)

    async def list_secrets(self) -> list[fragments.ProjectSecret]:
        """List all secrets in the current project."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.list_secrets(project_id=project_id)

    async def list_machine_types(self) -> list[schemas.MachineTypeListItem]:
        """List all machine types."""
        return await self._api.list_machine_types()

    """
    Get SDK methods
    """

    async def get_app(self, app_name: str) -> fragments.ComponentSpec | None:
        """Get an app by name."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.get_component_spec_by_name(app_name, project_id=project_id)

    async def get_run(self, run_name: str) -> fragments.Run | None:
        """Get a run by name."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.get_run(run_name=run_name, project_id=project_id)

    async def get_deployment(self, deployment_name: str) -> fragments.ComponentSpec | None:
        """Get a deployment by name."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.get_deployment(deployment_name, project_id=project_id)

    async def get_deployment_latencies(self, deployment_id: str) -> schemas.UsageBinsLatencyQuantiles:
        """Get a deployment's latencies by deployment id."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.get_deployment_latencies(deployment_id, project_id=project_id)

    async def get_environment(self, environment_id: str) -> fragments.ExecutionEnvironmentSpec | None:
        """Get an environment by id."""
        await self._get_current_project_id_or_raise()
        return await self._api.get_environment_spec(environment_id)

    async def get_artifact(
        self, blob_artifact_name: str, blob_artifact_tag: str | None = None
    ) -> fragments.BlobArtifact | None:
        """Get an artifact by name and optionally tag."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.get_blob_artifact_by_name_and_tag(
            blob_artifact_name, artifact_tag=blob_artifact_tag, project_id=project_id
        )

    """
    Create SDK methods
    """

    async def create_project(self, project_id: str, display_name: str) -> schemas.Response[schemas.ProjectId]:
        """Create a new project with the given ID and display name."""
        return await self._api.create_project(project_id=project_id, project_display_name=display_name)

    async def create_app(
        self,
        name: str,
        command: str | None,
        component_type: schemas.ComponentType,
        exec_env_spec_id: str | None,
        machine_size: schemas.MachineSize,
        mounts: list[schemas.MountSpecUnion],
        attach_project_credentials: bool,
        app_sub_type: schemas.AppSubType | None = None,
        config_variables: JSONType | None = None,
        app_port: int | None = None,
        import_run_spec_id: str | None = None,
        export_run_spec_id: str | None = None,
    ) -> schemas.ComponentSpecIdResponse:
        """Create a new app with the given name and configuration."""
        # TODO: this also supports creating runs/templates, but not sure if we should keep this behavior
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.create_app(
            name=name,
            command=command,
            component_type=component_type,
            app_sub_type=app_sub_type,
            exec_env_spec_id=exec_env_spec_id,
            machine_size=machine_size,
            mounts=mounts,
            attach_project_credentials=attach_project_credentials,
            config_variables=config_variables,
            app_port=app_port,
            project_id=project_id,
            import_run_spec_id=import_run_spec_id,
            export_run_spec_id=export_run_spec_id,
        )

    async def create_run_template(
        self,
        name: str,
        command: str | None,
        exec_env_spec_id: str,
        machine_size: schemas.MachineSize,
        mounts: list[schemas.MountSpecUnion],
        attach_project_credentials: bool,
        config_variables: JSONType | None = None,
    ) -> schemas.ComponentSpecIdResponse:
        """Create a new run template with the given name and configuration."""
        return await self.create_app(
            name=name,
            command=command,
            component_type=schemas.ComponentType.RUN,
            exec_env_spec_id=exec_env_spec_id,
            machine_size=machine_size,
            mounts=mounts,
            attach_project_credentials=attach_project_credentials,
            config_variables=config_variables,
        )

    async def create_deployment(
        self,
        name: str,
        command: str | None,
        exec_env_spec_id: str,
        machine_size: schemas.MachineSize,
        mounts: list[schemas.MountSpecUnion],
        attach_project_credentials: bool,
        config_variables: JSONType | None = None,
    ) -> schemas.ComponentSpecIdResponse:
        """Create a new deployment with the given name and configuration."""
        return await self.create_app(
            name=name,
            command=command,
            component_type=schemas.ComponentType.DEPLOYMENT,
            exec_env_spec_id=exec_env_spec_id,
            machine_size=machine_size,
            mounts=mounts,
            attach_project_credentials=attach_project_credentials,
            config_variables=config_variables,
        )

    async def create_environment(
        self,
        name: str,
        requested_python_requirements: list[schemas.RequestedRequirement] | None = None,
        requested_apt_requirements: list[schemas.RequestedAptPackage] | None = None,
        post_install_command: str | None = None,
        force_create_environment: bool = False,
    ) -> schemas.CreateEnvironmentSpecResponse:
        """Create a new environment with the given name and requirements."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.create_or_update_environment_spec(
            name=name,
            requested_python_requirements=requested_python_requirements,
            requested_apt_requirements=requested_apt_requirements,
            post_install_command=post_install_command or "",
            force_create_environment=force_create_environment,
            project_id=project_id,
        )

    async def create_volume(self, volume_name: str) -> None:
        """
        Create a volume in the current project.
        """
        project_id = await self._get_current_project_id_or_raise()
        resp = await self._api.create_volume(volume_name=volume_name, project_id=project_id)
        if resp.error:
            raise SlingshotException(f"Error creating volume: {resp.error.message}")

    async def create_secret(self, secret_name: str, secret_value: str) -> schemas.ProjectSecret:
        """Create a secret in the current project."""
        project_id = await self._get_current_project_id_or_raise()
        resp = await self._api.put_secret(secret_name=secret_name, secret_value=secret_value, project_id=project_id)
        return get_data_or_raise(resp)

    """
    Update SDK methods
    """

    async def update_app(
        self,
        spec_id: str,
        command: str | None,
        env_spec_id: str | None,
        machine_size: schemas.MachineSize,
        mounts: list[schemas.MountSpecUnion],
        attach_project_credentials: bool,
        config_variables: JSONType | None = None,
        app_port: int | None = None,
        batch_size: int | None = None,
        batch_interval: int | None = None,
        import_run_spec_id: str | None = None,
        export_run_spec_id: str | None = None,
    ) -> schemas.BoolResponse:
        """Updates app with the given id and configuration."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.update_app(
            spec_id=spec_id,
            command=command,
            exec_env_spec_id=env_spec_id,
            machine_size=machine_size,
            mounts=mounts,
            attach_project_credentials=attach_project_credentials,
            config_variables=config_variables,
            app_port=app_port,
            batch_size=batch_size,
            batch_interval=batch_interval,
            project_id=project_id,
            import_run_spec_id=import_run_spec_id,
            export_run_spec_id=export_run_spec_id,
        )

    async def update_environment(
        self,
        name: str,
        requested_python_requirements: list[schemas.RequestedRequirement] | None = None,
        requested_apt_requirements: list[schemas.RequestedAptPackage] | None = None,
        post_install_command: str | None = None,
        force_create_environment: bool = False,
    ) -> schemas.CreateEnvironmentSpecResponse:
        """Updates environment with the given name and configuration."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.create_or_update_environment_spec(
            name=name,
            requested_python_requirements=requested_python_requirements,
            requested_apt_requirements=requested_apt_requirements,
            post_install_command=post_install_command or "",
            force_create_environment=force_create_environment,
            project_id=project_id,
        )

    """
    Delete SDK methods
    """

    async def delete_app(self, spec_id: str) -> schemas.ResponseOK:
        """Delete an app with the given id."""
        project_id = await self._get_current_project_id_or_raise()
        return await self._api.delete_app(spec_id=spec_id, project_id=project_id)

    async def delete_environment(self, environment_id: str) -> None:
        """Delete an environment with the given id."""
        await self._get_current_project_id_or_raise()
        await self._api.delete_environment_spec(execution_environment_spec_id=environment_id)

    async def delete_volume(self, volume_name: str) -> bool:
        """
        Delete a volume in the current project.
        """
        project_id = await self._get_current_project_id_or_raise()
        resp = await self._api.delete_volume(volume_name=volume_name, project_id=project_id)
        return get_data_or_raise(resp)

    async def delete_secret(self, secret_name: str) -> bool:
        """Delete a secret in the current project."""
        project_id = await self._get_current_project_id_or_raise()
        resp = await self._api.delete_secret(secret_name=secret_name, project_id=project_id)
        return get_data_or_raise(resp)

    """
    Private helper methods
    """

    async def _get_current_project_or_raise(self) -> schemas.Project:
        if self.project:
            return self.project
        await self.setup()
        if self.project:
            return self.project

        if not await self.is_signed_in():
            raise SlingshotUnauthenticatedError()

        raise SlingshotNoProjectSetError()

    async def _get_current_project_id_or_raise(self) -> str:
        project = await self._get_current_project_or_raise()
        return project.project_id

    def _get_apply_service(self) -> ApplyService:
        return ApplyService(self)

    async def _wait_for_deployment_status(
        self,
        deployment_spec: schemas.HasComponentSpecId,
        status: schemas.ComponentInstanceStatus,
        *,
        max_wait: float | None = None,
    ) -> None:
        """
        Wait for a deployment to reach a given status.
        If it doesn't reach the status within max_wait seconds, raises a SlingshotException.
        If the status is ERROR, raises a SlingshotException, unless that's the status we're waiting for.
        """

        async def _wait_for_status() -> None:
            async for current_status in self._api.follow_deployment_status(deployment_spec.spec_id):
                if current_status == status:
                    return
                if current_status == schemas.ComponentInstanceStatus.ERROR:
                    raise SlingshotException(f"Deployment status is error : {current_status}")

        try:
            await wait_for(_wait_for_status(), max_wait)
        except asyncio.TimeoutError:
            raise SlingshotException(f"Deployment status timed out waiting for {status} after {max_wait} seconds")

    async def _wait_for_run_status(
        self: SlingshotSDK,
        run: schemas.HasRunId,
        status: schemas.ComponentInstanceStatus,
        *,
        max_wait: float | None = None,
    ) -> None:
        """
        Wait for a run to reach a given status.
        If it doesn't reach the status within max_wait seconds, raises a SlingshotException.
        If the status is ERROR, raises a SlingshotException, unless that's the status we're waiting for.
        """

        async def _wait_for_status() -> None:
            async for current_status in self._api.follow_run_status(run.run_id):
                if current_status == status:
                    return
                if current_status == schemas.ComponentInstanceStatus.ERROR:
                    raise SlingshotException(f"Run status is error : {current_status}")

        try:
            await wait_for(_wait_for_status(), max_wait)
        except asyncio.TimeoutError:
            raise SlingshotException(f"Run status timed out waiting for {status} after {max_wait} seconds")

    async def _wait_for_app_status(
        self: SlingshotSDK,
        app: schemas.HasComponentSpecId,
        status: schemas.ComponentInstanceStatus,
        *,
        max_wait: float | None = None,
    ) -> None:
        """
        Wait for an app to reach a given status.
        If it doesn't reach the status within max_wait seconds, raises a SlingshotException.
        If the status is ERROR, raises a SlingshotException, unless that's the status we're waiting for.
        """

        async def _wait_for_status() -> None:
            async for current_status in self._api.follow_app_status(app.spec_id):
                if current_status == status:
                    return
                if current_status == schemas.ComponentInstanceStatus.ERROR:
                    raise SlingshotException(f"App status is error : {current_status}")

        try:
            await wait_for(_wait_for_status(), max_wait)
        except asyncio.TimeoutError:
            raise SlingshotException(f"App status timed out waiting for {status} after {max_wait} seconds")
