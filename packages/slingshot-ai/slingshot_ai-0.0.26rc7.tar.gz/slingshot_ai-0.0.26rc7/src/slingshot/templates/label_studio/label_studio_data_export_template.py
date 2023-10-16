import os

import label_studio_sdk
from pydantic import BaseModel, ConfigDict

from slingshot.schemas import ExampleResult, Result

ANNOTATIONS_MOUNT_PATH = "/mnt/annotations"

# Data fields will be exported as part of the annotation result data, but should not be included as part of the
# annotations if they are large or irrelevant to the annotations (e.g. image paths)
DATA_FIELDS_TO_EXCLUDE: list[str] = []


class LabelStudioResult(BaseModel):
    example_id: str
    model_config = ConfigDict(extra="allow", populate_by_name=True)


def convert_label_studio_annotations_to_annotations(ls_annotations: list[LabelStudioResult]) -> list[ExampleResult]:
    """Convert Label Studio annotations to the Slingshot ExampleResult schema."""
    example_results: list[ExampleResult] = []
    for ls_annotation in ls_annotations:
        result = Result.model_validate(ls_annotation.model_dump(exclude=set(["example_id"] + DATA_FIELDS_TO_EXCLUDE)))
        annotation = ExampleResult(example_id=ls_annotation.example_id, result=result)
        example_results.append(annotation)
    return example_results


def get_label_studio_annotations(ls_client: label_studio_sdk.Client) -> list[ExampleResult]:
    """Get all annotations from Label Studio and convert them to the Slingshot ExampleResult schema."""
    project = ls_client.get_project(id=1)
    res = project.export_tasks(export_type="JSON-MIN")
    ls_annotations = [LabelStudioResult.model_validate(annotation_obj) for annotation_obj in res]
    examples = convert_label_studio_annotations_to_annotations(ls_annotations)
    print(f"Found {len(examples)} annotated examples on Label Studio")
    return examples


def write_annotations_to_file(slingshot_annotations: list[ExampleResult], filename: str = "annotations.jsonl") -> None:
    """Write annotations to annotations.jsonl file"""
    with open(os.path.join(ANNOTATIONS_MOUNT_PATH, filename), "w") as f:
        for annotation in slingshot_annotations:
            f.write(str(annotation.model_dump()) + "\n")
    print(f"Saved all annotations to '{filename}'")


def main() -> None:
    """Export all annotations from Label Studio and write them to the annotations.jsonl file."""
    assert "LABEL_STUDIO_API_KEY" in os.environ, "Please create a Slingshot Secret for 'LABEL_STUDIO_API_KEY'"
    assert "LABEL_STUDIO_URL" in os.environ, "Please create a Slingshot Secret for 'LABEL_STUDIO_URL'"
    ls_client = label_studio_sdk.Client(api_key=os.environ["LABEL_STUDIO_API_KEY"], url=os.environ["LABEL_STUDIO_URL"])
    all_annotations = get_label_studio_annotations(ls_client)
    write_annotations_to_file(all_annotations)


if __name__ == "__main__":
    main()
