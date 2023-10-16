from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from slingshot import schemas

from ..base_graphql import BaseGraphQLQuery
from ..fragments import Run


class RunsForProjectResponse(BaseModel):
    runs: list[Run] = Field(..., alias="runs")


class RunsForProjectQuery(BaseGraphQLQuery[RunsForProjectResponse]):
    _query = """
        query RunsForProject($projectId: String!) {
            runs(where: {project: {projectId: {_eq: $projectId}}, isArchived: { _eq: false }}, orderBy: {createdAt: DESC}) {
                ...Run
            }
        } """

    _depends_on = [Run]

    def __init__(self, project_id: str):
        super().__init__(variables={"projectId": project_id}, response_model=RunsForProjectResponse)


class RunByNameForProjectQuery(BaseGraphQLQuery[RunsForProjectResponse]):
    _query = """
        query RunByNameForProject($projectId: String!, $runName: String!) {
            runs(where: {project: {projectId: {_eq: $projectId}}, trainingRunName: {_eq: $runName}}) {
                ...Run
            }
        } """

    _depends_on = [Run]

    def __init__(self, project_id: str, run_name: str):
        super().__init__(
            variables={"projectId": project_id, "runName": run_name}, response_model=RunsForProjectResponse
        )


class RunByIdResponse(BaseModel):
    run: Optional[Run] = Field(None, alias="runsByPk")


class RunByIdQuery(BaseGraphQLQuery[RunByIdResponse]):
    _query = """
        query RunById($runId: String!) {
          runsByPk(trainingRunId: $runId) {
            ...Run
          }
        } """

    _depends_on = [Run]

    def __init__(self, run_id: str) -> None:
        super().__init__(variables={"runId": run_id}, response_model=RunByIdResponse)


class RunWithStatus(BaseModel):
    run_status: schemas.ComponentInstanceStatus = Field(..., alias="runStatus")


class RunsWithStatusResponse(BaseModel):
    run: Optional[RunWithStatus] = Field(None, alias="runsByPk")


class RunStatusSubscription(BaseGraphQLQuery[RunsWithStatusResponse]):
    _query = """
        subscription RunStatusSubscription($runId: String!) {
          runsByPk(trainingRunId: $runId) {
            runStatus
          }
        }
    """
    _depends_on = []

    def __init__(self, run_id: str):
        super().__init__(variables={"runId": run_id}, response_model=RunsWithStatusResponse)
