import os
from datetime import timedelta
from logging import getLogger

from tqdm import tqdm

from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.slingshot_api import SlingshotClient

logger = getLogger(__name__)

UPLOAD_TIMEOUT_MIN = 120
MAX_RETRIES = 3
CHUNK_SIZE_BYTES = 1024 * 1024  # 1 MB


async def upload_file_in_parts_to_gcs(
    artifact_path: str, upload_signed_url: str, *, client: SlingshotClient, quiet: bool = False
) -> None:
    logger.debug(f"Uploading {artifact_path} to {upload_signed_url}")
    with open(artifact_path, 'rb') as file:
        # Get the size of the file to be uploaded and create a progress bar for it
        file_size = os.path.getsize(artifact_path)
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Uploading", disable=quiet) as pbar:
            position = 0  # Current position in the file
            while position < file_size:
                chunk = file.read(CHUNK_SIZE_BYTES)
                retries = 0
                while retries < MAX_RETRIES:
                    try:
                        # Upload the chunk with a PUT request to the session URI
                        await client.make_request(
                            upload_signed_url,
                            method="put",
                            response_model=None,
                            data=chunk,
                            headers={
                                'content-type': 'application/octet-stream',
                                'Content-Range': 'bytes %d-%d/%d' % (position, position + len(chunk) - 1, file_size),
                            },
                            timeout=timedelta(minutes=UPLOAD_TIMEOUT_MIN),
                        )

                        # Update the progress bar and position
                        pbar.update(len(chunk))
                        position += len(chunk)
                        break
                    except Exception as e:
                        logger.debug(f"Error during upload: {e}")
                        retries += 1
                        if retries > MAX_RETRIES:
                            raise SlingshotException(f"Maximum retries reached for upload, aborting upload: {e}") from e


async def download_file_in_parts(save_path: str, signed_url: str, *, client: SlingshotClient) -> None:
    logger.debug(f"Downloading {signed_url} to {save_path}")
    async with client.async_http_get_with_unlimited_timeout(signed_url) as response:
        file_size = int(response.headers.get("Content-Length", 0))
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Downloading") as pbar:
            with open(save_path, 'wb') as file:
                # Iterate over the response content in chunks
                async for chunk in response.content.iter_chunked(CHUNK_SIZE_BYTES):
                    file.write(chunk)
                    pbar.update(len(chunk))
