from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from slingshot.sdk.graphql import fragments

from ..base_graphql import BaseGraphQLQuery


class UserWithProjectsResponse(BaseModel):
    users_by_pk: Optional[fragments.UserWithProjects] = Field(None, alias="usersByPk")


class UserWithProjectsQuery(BaseGraphQLQuery[UserWithProjectsResponse]):
    _query = """
        query UserWithProjects($userId: String!) {
          usersByPk(userId: $userId) {
            ...UserWithProjects
          }
        } """

    _depends_on = [fragments.UserWithProjects]

    def __init__(self, user_id: str):
        super().__init__(variables={"userId": user_id}, response_model=UserWithProjectsResponse)


class ServiceAccountWithProjectsResponse(BaseModel):
    service_accounts_by_pk: Optional[fragments.ServiceAccountWithProjects] = Field(None, alias="serviceAccountsByPk")


class ServiceAccountWithProjectsQuery(BaseGraphQLQuery[ServiceAccountWithProjectsResponse]):
    _query = """
        query ServiceAccountWithProjects($serviceAccountId: String!) {
          serviceAccountsByPk(serviceAccountId: $serviceAccountId) {
            ...ServiceAccountWithProjects
          }
        } """

    _depends_on = [fragments.ServiceAccountWithProjects]

    def __init__(self, service_account_id: str):
        super().__init__(
            variables={"serviceAccountId": service_account_id}, response_model=ServiceAccountWithProjectsResponse
        )


class ProjectByIdResponse(BaseModel):
    projects_by_pk: Optional[fragments.ProjectFields] = Field(None, alias="projectsByPk")


class ProjectByIdQuery(BaseGraphQLQuery[ProjectByIdResponse]):
    _query = """
        query ProjectById($projectId: String!) {
          projectsByPk(projectId: $projectId) {
            ...ProjectFields
          }
        } """

    _depends_on = [fragments.ProjectFields]

    def __init__(self, project_id: str):
        super().__init__(variables={"projectId": project_id}, response_model=ProjectByIdResponse)


class BillingLineItemsResponse(BaseModel):
    billingLineItems: list[fragments.BillingLineItem] = Field(..., alias="billingLineItems")


class BillingLineItemsByAppIdQuery(BaseGraphQLQuery[BillingLineItemsResponse]):
    _query = """
        query BillingLineItemsByAppIdQuery($appInstanceId: String!) {
          billingLineItems(where: {appInstanceId: {_eq: $appInstanceId}}) {
            ...BillingLineItem
          }
        } """

    _depends_on = [fragments.BillingLineItem]

    def __init__(self, app_instance_id: str):
        super().__init__(variables={"appInstanceId": app_instance_id}, response_model=BillingLineItemsResponse)


class BillingLineItemsByDeploymentIdQuery(BaseGraphQLQuery[BillingLineItemsResponse]):
    _query = """
        query BillingLineItemsByAppIdQuery($deploymentId: String!) {
          billingLineItems(where: {deploymentId: {_eq: $deploymentId}, _and: {startTime: {_isNull: false}}}) {
            ...BillingLineItem
          }
        } """

    _depends_on = [fragments.BillingLineItem]

    def __init__(self, deployment_id: str):
        super().__init__(variables={"deploymentId": deployment_id}, response_model=BillingLineItemsResponse)


class BillingLineItemsByRunIdQuery(BaseGraphQLQuery[BillingLineItemsResponse]):
    _query = """
        query BillingLineItemsByAppIdQuery($runId: String!) {
          billingLineItems(where: {runId: {_eq: $runId}}) {
            ...BillingLineItem
          }
        } """

    _depends_on = [fragments.BillingLineItem]

    def __init__(self, run_id: str):
        super().__init__(variables={"runId": run_id}, response_model=BillingLineItemsResponse)


class ProjectWithSecrets(BaseModel):
    project_secrets: list[fragments.ProjectSecret] = Field(..., alias="projectSecrets")


class ProjectSecretsResponse(BaseModel):
    projects_by_pk: Optional[ProjectWithSecrets] = Field(None, alias="projectsByPk")


class ProjectSecretsQuery(BaseGraphQLQuery[ProjectSecretsResponse]):
    _query = """
        query ProjectSecrets($projectId: String!) {
            projectsByPk(projectId: $projectId) {
                projectSecrets {
                    ...ProjectSecret
                }
            }
        }
    """
    _depends_on = [fragments.ProjectSecret]

    def __init__(self, project_id: str):
        super().__init__(variables={"projectId": project_id}, response_model=ProjectSecretsResponse)


class SourceCodesResponse(BaseModel):
    source_codes: list[fragments.SourceCodeArtifact] = Field(..., alias="sourceCodes")


class SourceCodesForProjectResponse(BaseModel):
    projects_by_pk: Optional[SourceCodesResponse] = Field(None, alias="projectsByPk")


class LatestSourceCodeForProjectQuery(BaseGraphQLQuery[SourceCodesForProjectResponse]):
    _query = """
        query LatestSourceCodeForProject($projectId: String!) {
            projectsByPk(projectId: $projectId) {
                sourceCodes(orderBy: { blobArtifact: { createdAt: DESC } }, limit: 1) {
                    ...SourceCodeArtifact
                }
            }
        } """

    _depends_on = [fragments.SourceCodeArtifact]

    def __init__(self, project_id: str):
        super().__init__(variables={"projectId": project_id}, response_model=SourceCodesForProjectResponse)
