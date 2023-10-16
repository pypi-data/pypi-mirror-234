import asyncio
import datetime
import os
from typing import Any

import label_studio_sdk
from pydantic import BaseModel

from slingshot import SlingshotSDK
from slingshot.schemas import Example, ExampleResult

DATASET_MOUNT_PATH = "/mnt/data"
ANNOTATIONS_MOUNT_PATH = "/mnt/annotations"

DATASET_ARTIFACT_NAME = "dataset"
DATASET_ARTIFACT_TAG = "latest"

# Add data field names here that contain paths to media files here
# e.g. if your data is shaped like {"example_id": "1", "data": {"image_path": "path/to/image.jpg"}}, add "image_path"
MEDIA_PATH_FIELDS = []


def read_slingshot_examples(path: str) -> list[str]:
    """Read examples from a file as a list of raw JSON strings."""
    if not os.path.exists(path):
        return []

    examples = []
    with open(path, "r") as f:
        for line in f:
            if line := line.strip():
                examples.append(line)
    return examples


async def import_label_studio_tasks(
    ls_client: label_studio_sdk.Client, sdk: SlingshotSDK, examples: list[Example], annotations: list[ExampleResult]
) -> None:
    """Import examples to Label Studio as tasks."""
    latest_artifact = await sdk.get_artifact(
        blob_artifact_name=DATASET_ARTIFACT_NAME, blob_artifact_tag=DATASET_ARTIFACT_TAG
    )
    assert latest_artifact, f"No artifact found with name {DATASET_ARTIFACT_NAME} and tag 'latest'"
    assert sdk.project_id, "Slingshot SDK Project ID is not set"

    print(f"Importing {len(examples)} examples as tasks")
    tasks = []
    for example in examples:
        data = example.data
        if isinstance(data, BaseModel):
            data = data.model_dump()
        data = await convert_media_paths_to_signed_urls(
            sdk=sdk, data=data, blob_artifact_id=latest_artifact.blob_artifact_id, project_id=sdk.project_id
        )
        tasks.append({"data": {**data, "example_id": example.example_id}})

    print("Importing tasks")
    project = ls_client.get_project(id=1)
    task_ids: list[int] = project.import_tasks(tasks=tasks)

    print(f"Importing {len(annotations)} existing annotations")
    example_ids_to_task_id = {example.example_id: task_id for example, task_id in zip(examples, task_ids)}
    for annotation in annotations:
        task_id = example_ids_to_task_id[annotation.example_id]
        project.create_annotation(task_id=task_id, result=annotation.result.model_dump())


async def convert_media_paths_to_signed_urls(
    sdk: SlingshotSDK, data: dict[str, Any], blob_artifact_id: str, project_id: str
) -> dict[str, Any]:
    """Convert media paths inside your dataset into signed URLs for Label Studio to load from."""
    for field in MEDIA_PATH_FIELDS:
        image_url_resp = await sdk.api.signed_url_blob_artifact(
            blob_artifact_id=blob_artifact_id,
            file_path=data[field],
            expiration=datetime.timedelta(days=7),
            project_id=project_id,
        )
        assert not image_url_resp.error, f"Error getting signed url: {image_url_resp.error}"
        assert image_url_resp.data, "No signed url returned"
        data[field] = image_url_resp.data.signed_url
    return data


async def main():
    """Import the dataset from the mounted path to Label Studio."""
    assert "LABEL_STUDIO_API_KEY" in os.environ, "Please create a Slingshot Secret for 'LABEL_STUDIO_API_KEY'"
    assert "LABEL_STUDIO_URL" in os.environ, "Please create a Slingshot Secret for 'LABEL_STUDIO_URL'"
    sdk = SlingshotSDK()
    await sdk.setup()

    # Load all examples and annotations from the mounted paths
    example_json_strings = read_slingshot_examples(os.path.join(DATASET_MOUNT_PATH, "dataset.jsonl"))
    annotation_json_strings = read_slingshot_examples(os.path.join(ANNOTATIONS_MOUNT_PATH, "annotations.jsonl"))

    examples = [Example.model_validate_json(example) for example in example_json_strings]
    annotations = [ExampleResult.model_validate_json(annotation) for annotation in annotation_json_strings]

    ls_client = label_studio_sdk.Client(api_key=os.environ["LABEL_STUDIO_API_KEY"], url=os.environ["LABEL_STUDIO_URL"])
    await import_label_studio_tasks(ls_client, sdk=sdk, examples=examples, annotations=annotations)


if __name__ == "__main__":
    asyncio.run(main())
