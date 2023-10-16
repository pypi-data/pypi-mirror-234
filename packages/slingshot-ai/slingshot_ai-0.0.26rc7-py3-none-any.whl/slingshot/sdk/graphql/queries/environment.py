from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from ..base_graphql import BaseGraphQLQuery
from ..fragments import ExecutionEnvironmentSpec


class ExecutionEnvironmentSpecByIdResponse(BaseModel):
    execution_environment_specs_by_pk: Optional[ExecutionEnvironmentSpec] = Field(
        None, alias="executionEnvironmentSpecsByPk"
    )


class ExecutionEnvironmentSpecByIdQuery(BaseGraphQLQuery[ExecutionEnvironmentSpecByIdResponse]):
    _query = """
        query ExecutionEnvironmentSpecById($executionEnvironmentSpecId: String!) {
          executionEnvironmentSpecsByPk(executionEnvironmentSpecId: $executionEnvironmentSpecId) {
            ...ExecutionEnvironmentSpec
          }
        } """

    _depends_on = [ExecutionEnvironmentSpec]

    def __init__(self, execution_environment_spec_id: str):
        super().__init__(
            variables={"executionEnvironmentSpecId": execution_environment_spec_id},
            response_model=ExecutionEnvironmentSpecByIdResponse,
        )


class ExecutionEnvironmentSpecsForProjectResponse(BaseModel):
    execution_environment_specs: list[ExecutionEnvironmentSpec] = Field(..., alias="executionEnvironmentSpecs")


class ExecutionEnvironmentSpecsForProjectQuery(BaseGraphQLQuery[ExecutionEnvironmentSpecsForProjectResponse]):
    _query = """
        query ExecutionEnvironmentSpecsForProject($projectId: String!) {
          executionEnvironmentSpecs(where: { project: { projectId: { _eq: $projectId } }, isArchived: { _eq: false } }) {
            ...ExecutionEnvironmentSpec
          }
        } """

    _depends_on = [ExecutionEnvironmentSpec]

    def __init__(self, project_id: str):
        super().__init__(
            variables={"projectId": project_id}, response_model=ExecutionEnvironmentSpecsForProjectResponse
        )


class ExecutionEnvironmentSpecId(BaseModel):
    execution_environment_spec_id: str = Field(..., alias="executionEnvironmentSpecId")


class ArchiveExecutionEnvironmentSpecResponse(BaseModel):
    update_execution_environment_specs_by_pk: Optional[ExecutionEnvironmentSpecId] = Field(
        None, alias="updateExecutionEnvironmentSpecsByPk"
    )


class ArchiveExecutionEnvironmentSpecMutation(BaseGraphQLQuery[ArchiveExecutionEnvironmentSpecResponse]):
    _query = """
        mutation ArchiveExecutionEnvironmentSpec($executionEnvironmentSpecId: String!, $isArchived: Boolean!) {
          updateExecutionEnvironmentSpecsByPk(pkColumns: {executionEnvironmentSpecId: $executionEnvironmentSpecId},
          _set: {isArchived: $isArchived}) {
            executionEnvironmentSpecId
          }
        }"""

    _depends_on = []

    def __init__(self, execution_environment_spec_id: str, is_archived: bool):
        super().__init__(
            variables={"executionEnvironmentSpecId": execution_environment_spec_id, "isArchived": is_archived},
            response_model=ArchiveExecutionEnvironmentSpecResponse,
        )
