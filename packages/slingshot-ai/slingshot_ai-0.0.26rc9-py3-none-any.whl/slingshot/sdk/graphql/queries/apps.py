from __future__ import annotations

from pydantic import BaseModel, Field

from slingshot import schemas

from ..base_graphql import BaseGraphQLQuery
from ..fragments import AppInstance, ComponentSpec


class ComponentSpecsForProjectResponse(BaseModel):
    component_specs: list[ComponentSpec] = Field(..., alias="componentSpecs")


class ComponentSpecsForProjectQuery(BaseGraphQLQuery[ComponentSpecsForProjectResponse]):
    _query = """
        query ComponentSpecsForProject($projectId: String!) {
            componentSpecs(where: {
                project: { projectId: {_eq: $projectId} },
                isArchived: {_eq: false}
            }) {
                ...ComponentSpec
            }
        } """

    _depends_on = [ComponentSpec]

    def __init__(self, project_id: str):
        super().__init__(variables={"projectId": project_id}, response_model=ComponentSpecsForProjectResponse)


class AppInstancesResponse(BaseModel):
    app_instances: list[AppInstance] = Field(..., alias="appInstances")


class AppInstancesByAppSubTypeQuery(BaseGraphQLQuery[AppInstancesResponse]):
    _query = """
        query AppInstancesByAppSubType($appSubType: AppTypeEnumEnum!, $projectId: String!) {
            appInstances(where: {_and: {appSubType: {_eq: $appSubType}, projectId: {_eq: $projectId}}}) {
                ...AppInstance
            }
        }
    """

    _depends_on = [AppInstance]

    def __init__(self, app_sub_type: str, project_id: str):
        super().__init__(
            variables={"appSubType": app_sub_type, "projectId": project_id}, response_model=AppInstancesResponse
        )


class LatestAppInstanceForComponentQuery(BaseGraphQLQuery[AppInstancesResponse]):
    _query = """
        query LatestAppInstanceForComponentQuery($specId: String!) {
            appInstances(where: {specId: {_eq: $specId}}, orderBy: {createdAt: DESC}, limit: 1) {
                ...AppInstance
            }
        } """

    _depends_on = [AppInstance]

    def __init__(self, spec_id: str):
        super().__init__(variables={"specId": spec_id}, response_model=AppInstancesResponse)


class AppInstanceQuery(BaseGraphQLQuery[AppInstancesResponse]):
    _query = """
        query AppInstance($appInstanceId: String!, $projectId: String!) {
            appInstances(where: {_and: {appInstanceId: {_eq: $appInstanceId}, componentSpec: {projectId: {_eq: $projectId}}}}) {
                ...AppInstance
           }
        }
    """

    _depends_on = [AppInstance]

    def __init__(self, app_instance_id: str, project_id: str):
        super().__init__(
            variables={"appInstanceId": app_instance_id, "projectId": project_id}, response_model=AppInstancesResponse
        )


class ComponentSpecsResponse(BaseModel):
    component_specs: list[ComponentSpec] = Field(..., alias="componentSpecs")


class ComponentSpecByIdQuery(BaseGraphQLQuery[ComponentSpecsResponse]):
    _query = """
        query ComponentSpecQueryByIdQuery($specId: String!, $projectId: String!) {
            componentSpecs(where: {_and: {specId: {_eq: $specId}, projectId: {_eq: $projectId}}}) {
                ...ComponentSpec
           }
        }
    """

    _depends_on = [ComponentSpec]

    def __init__(self, spec_id: str, project_id: str):
        super().__init__(variables={"specId": spec_id, "projectId": project_id}, response_model=ComponentSpecsResponse)


class ComponentSpecByNameQuery(BaseGraphQLQuery[ComponentSpecsResponse]):
    _query = """
        query ComponentSpecByName($specName: String!, $projectId: String!) {
            componentSpecs(where: {_and: {specName: {_eq: $specName}, projectId: {_eq: $projectId}}}) {
                ...ComponentSpec
           }
        }
    """

    _depends_on = [ComponentSpec]

    def __init__(self, spec_name: str, project_id: str):
        super().__init__(
            variables={"specName": spec_name, "projectId": project_id}, response_model=ComponentSpecsResponse
        )


class DeploymentSpecByNameQuery(BaseGraphQLQuery[ComponentSpecsResponse]):
    _query = """
        query DeploymentSpecByName($specName: String!, $projectId: String!) {
            componentSpecs(where: {_and: {
                specName: {_eq: $specName},
                projectId: {_eq: $projectId},
                componentType: {_eq: DEPLOYMENT}
            }}) {
                ...ComponentSpec
           }
        }
    """

    _depends_on = [ComponentSpec]

    def __init__(self, spec_name: str, project_id: str):
        super().__init__(
            variables={"specName": spec_name, "projectId": project_id}, response_model=ComponentSpecsResponse
        )


class AppInstanceWithStatus(BaseModel):
    app_instance_status: schemas.ComponentInstanceStatus = Field(..., alias="appInstanceStatus")


class AppInstancesWithStatusResponse(BaseModel):
    app_instances: list[AppInstanceWithStatus] = Field(..., alias="appInstances")


class AppInstanceStatusForSpecSubscription(BaseGraphQLQuery[AppInstancesWithStatusResponse]):
    _query = """
        subscription AppInstanceStatusForSpecSubscription($specId: String!) {
          appInstances(where: {componentSpec: {specId: {_eq: $specId}}}, orderBy: {createdAt: DESC}, limit: 1) {
            appInstanceStatus
          }
        }
    """
    _depends_on = []

    def __init__(self, spec_id: str):
        super().__init__(variables={"specId": spec_id}, response_model=AppInstancesWithStatusResponse)
