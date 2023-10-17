from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from ..base_graphql import BaseGraphQLQuery
from ..fragments import BlobArtifact, Volume


class BlobArtifactsResponse(BaseModel):
    blob_artifacts: list[BlobArtifact] = Field(..., alias="blobArtifacts")


class BlobArtifactsForProjectResponse(BaseModel):
    projects_by_pk: Optional[BlobArtifactsResponse] = Field(None, alias="projectsByPk")


class LatestBlobArtifactsForProjectQuery(BaseGraphQLQuery[BlobArtifactsForProjectResponse]):
    _query = """
        query LatestBlobArtifactsForProjectQuery($projectId: String!) {
            projectsByPk(projectId: $projectId) {
                blobArtifacts(orderBy: {createdAt: DESC}, where: {isDraft: {_eq: false}}) {
                    ...BlobArtifact
                }
            }
        } """

    _depends_on = [BlobArtifact]

    def __init__(self, project_id: str):
        super().__init__(variables={"projectId": project_id}, response_model=BlobArtifactsForProjectResponse)


class LatestBlobArtifactsForProjectByNameQuery(BaseGraphQLQuery[BlobArtifactsForProjectResponse]):
    _query = """
        query LatestBlobArtifactsForProjectQuery($projectId: String!, $name: String!) {
            projectsByPk(projectId: $projectId) {
                blobArtifacts(orderBy: {createdAt: DESC}, where: {name: {_eq: $name}, isDraft: {_eq: false}}) {
                    ...BlobArtifact
                }
            }
        } """

    _depends_on = [BlobArtifact]

    def __init__(self, project_id: str, name: str):
        super().__init__(
            variables={"projectId": project_id, "name": name}, response_model=BlobArtifactsForProjectResponse
        )


class BlobArtifactByIdResponse(BaseModel):
    blob_artifacts_by_pk: Optional[BlobArtifact] = Field(None, alias="blobArtifactsByPk")


class BlobArtifactByIdQuery(BaseGraphQLQuery[BlobArtifactByIdResponse]):
    _query = """
        query BlobArtifactById($blobArtifactId: String!) {
          blobArtifactsByPk(blobArtifactId: $blobArtifactId) {
            ...BlobArtifact
          }
        } """

    _depends_on = [BlobArtifact]

    def __init__(self, blob_artifact_id: str):
        super().__init__(variables={"blobArtifactId": blob_artifact_id}, response_model=BlobArtifactByIdResponse)


class BlobArtifactByNameAndTagResponse(BaseModel):
    blob_artifacts: list[BlobArtifact] = Field(..., alias="blobArtifacts")


class BlobArtifactByNameAndTagQuery(BaseGraphQLQuery[BlobArtifactByNameAndTagResponse]):
    _query = """
        query BlobArtifactByName($projectId: String!, $name: String!, $tag: String!) {
          blobArtifacts(where: {
              _and: {name: {_eq: $name}, tags: {_contains: [$tag]}, projectId: {_eq: $projectId}}
          }) {
            ...BlobArtifact
          }
        }
    """

    _depends_on = [BlobArtifact]

    def __init__(self, project_id: str, name: str, tag: str | None = None):
        super().__init__(
            variables={"projectId": project_id, "name": name, "tag": tag or "latest"},
            response_model=BlobArtifactByNameAndTagResponse,
        )


class VolumesForProjectResponse(BaseModel):
    volumes: list[Volume] = Field(..., alias="volumes")


class VolumesForProjectQuery(BaseGraphQLQuery[VolumesForProjectResponse]):
    _query = """
        query VolumesForProject($projectId: String!) {
          volumes(where: {_and: {isArchived: {_eq: false}, projectId: {_eq: $projectId}}}) {
            ...Volume
          }
        } """

    _depends_on = [Volume]

    def __init__(self, project_id: str):
        super().__init__(variables={"projectId": project_id}, response_model=VolumesForProjectResponse)
