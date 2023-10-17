from __future__ import annotations

from pydantic import BaseModel, Field

from slingshot import schemas

from ..base_graphql import BaseGraphQLQuery
from ..fragments import DeploymentInstance


class DeploymentInstanceWithStatus(BaseModel):
    deployment_instance_status: schemas.ComponentInstanceStatus = Field(..., alias="deploymentStatus")


class DeploymentInstancesWithStatusResponse(BaseModel):
    deployment_instances: list[DeploymentInstanceWithStatus] = Field(..., alias="deployments")


class DeploymentInstancesResponse(BaseModel):
    deployment_instances: list[DeploymentInstance] = Field(..., alias="deployments")


class DeploymentStatusSubscription(BaseGraphQLQuery[DeploymentInstancesWithStatusResponse]):
    _query = """
        subscription DeploymentStatusSubscription($specId: String!) {
          deployments(where: {componentSpec: {specId: {_eq: $specId}}}, orderBy: {createdAt: DESC}, limit: 1) {
            deploymentStatus
          }
        }
    """
    _depends_on = []

    def __init__(self, spec_id: str):
        super().__init__(variables={"specId": spec_id}, response_model=DeploymentInstancesWithStatusResponse)


class LatestDeploymentInstanceForComponentQuery(BaseGraphQLQuery[DeploymentInstancesResponse]):
    _query = """
        query LatestDeploymentInstanceForComponentQuery($specId: String!) {
            deployments(where: {specId: {_eq: $specId}}, orderBy: {createdAt: DESC}, limit: 1) {
                ...DeploymentInstance
            }
        } """

    _depends_on = [DeploymentInstance]

    def __init__(self, spec_id: str):
        super().__init__(variables={"specId": spec_id}, response_model=DeploymentInstancesResponse)
