from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

from slingshot import schemas

from .base_graphql import BaseGraphQLEntity


class BlobArtifactShallow(BaseGraphQLEntity):
    _depends_on = []
    _fragment = """
        fragment BlobArtifactShallow on BlobArtifacts {
          blobArtifactId
          createdAt
          updatedAt
          bytesHash
          bytesSize
          name
          description
          tags
          isDraft
        } """

    blob_artifact_id: str = Field(..., alias="blobArtifactId")
    name: str = Field(..., alias="name")
    tags: list[str] = Field(..., alias="tags")
    description: Optional[str] = Field(None, alias="description")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    bytes_hash: Optional[str] = Field(None, alias="bytesHash")
    bytes_size: Optional[int] = Field(None, alias="bytesSize")


class Mount(BaseGraphQLEntity):
    _fragment = """
        fragment Mount on Mount {
          mountId
          deploymentId
          trainingRunId
          mountPath
          mountMode
          mountName
          mountTag
          downloadedBlobArtifact {
            ...BlobArtifactShallow
          }
          uploadedBlobArtifact {
            ...BlobArtifactShallow
          }
        } """

    _depends_on = [BlobArtifactShallow]

    mount_id: str = Field(..., alias="mountId")
    deployment_id: Optional[str] = Field(None, alias="deploymentId")
    run_id: Optional[str] = Field(None, alias="trainingRunId")
    mount_path: str = Field(..., alias="mountPath")
    mount_mode: Literal["DOWNLOAD", "UPLOAD", "VOLUME", "EMPTY"] = Field(..., alias="mountMode")
    mount_name: str = Field(..., alias="mountName")
    mount_tag: Optional[str] = Field(None, alias="mountTag")
    downloaded_blob_artifact: Optional[BlobArtifactShallow] = Field(None, alias="downloadedBlobArtifact")
    uploaded_blob_artifact: Optional[BlobArtifactShallow] = Field(None, alias="uploadedBlobArtifact")


class BlobArtifact(BaseGraphQLEntity):
    _fragment = """
        fragment BlobArtifact on BlobArtifacts {
          ...BlobArtifactShallow
          originMount {
            ...Mount
          }
        } """
    _depends_on = [BlobArtifactShallow, Mount]

    blob_artifact_id: str = Field(..., alias="blobArtifactId")
    name: str = Field(..., alias="name")
    tags: list[str] = Field(..., alias="tags")
    description: Optional[str] = Field(None, alias="description")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    bytes_hash: Optional[str] = Field(None, alias="bytesHash")
    bytes_size: Optional[int] = Field(None, alias="bytesSize")
    origin_mount: Optional[Mount] = Field(None, alias="originMount")
    is_draft: bool = Field(..., alias="isDraft")


class SourceCodeArtifact(BaseGraphQLEntity):
    _depends_on = [BlobArtifactShallow]
    _fragment = """
        fragment SourceCodeArtifact on SourceCodes {
          sourceCodeId
          projectId
          blobArtifact {
            ...BlobArtifactShallow
          }
        } """

    source_code_id: str = Field(..., alias="sourceCodeId")
    project_id: str = Field(..., alias="projectId")
    blob_artifact: BlobArtifactShallow = Field(..., alias="blobArtifact")


class Deployment(BaseGraphQLEntity):
    _depends_on = [BlobArtifact, SourceCodeArtifact]
    _fragment = """
        fragment Deployment on Deployments {
          createdAt
          deploymentId
          deploymentStatus
          projectId
          machineSize
          sourceCode {
            ...SourceCodeArtifact
          }
        } """

    deployment_id: str = Field(..., alias="deploymentId")
    created_at: datetime = Field(..., alias="createdAt")
    deployment_status: schemas.ComponentInstanceStatus = Field(..., alias="deploymentStatus")
    project_id: str = Field(..., alias="projectId")
    source_code: SourceCodeArtifact = Field(..., alias="sourceCode")


class Build(BaseGraphQLEntity):
    _depends_on = []
    _fragment = """
        fragment Build on Builds {
          buildId
          buildStatus
        } """
    build_id: str = Field(..., alias="buildId")
    build_status: str = Field(..., alias="buildStatus")  # TODO: Replace with enum or Literal


class ExecutionEnvironmentSpecName(BaseGraphQLEntity):
    _depends_on = []
    _fragment = """
        fragment ExecutionEnvironmentSpecName on ExecutionEnvironmentSpecs {
          executionEnvironmentSpecName
        } """
    execution_environment_spec_name: str = Field(..., alias="executionEnvironmentSpecName")


class EnvironmentInstance(BaseGraphQLEntity):
    _depends_on = [Build, ExecutionEnvironmentSpecName]
    _fragment = """
        fragment EnvironmentInstance on EnvironmentInstances {
            environmentInstanceId
            executionEnvironmentSpecId
            createdAt
            requestedAptPackages
            requestedPythonRequirements
            postInstallCommand
            executionEnvironmentSpec {
                ...ExecutionEnvironmentSpecName
            }
            cpuBuild {
                ...Build
            }
            gpuBuild {
                ...Build
            }
        }"""

    environment_instance_id: str = Field(..., alias="environmentInstanceId")
    execution_environment_spec_id: str = Field(..., alias="executionEnvironmentSpecId")
    created_at: datetime = Field(..., alias="createdAt")
    requested_apt_packages: list[dict[str, str]] = Field(..., alias="requestedAptPackages")
    requested_python_requirements: list[dict[str, Optional[str]]] = Field(
        ..., alias="requestedPythonRequirements", repr=False
    )
    post_install_command: str = Field("", alias="postInstallCommand")
    cpu_build: Optional[Build] = Field(..., alias="cpuBuild")
    gpu_build: Optional[Build] = Field(..., alias="gpuBuild")
    execution_environment_spec: ExecutionEnvironmentSpecName = Field(..., alias="executionEnvironmentSpec")


class ExecutionEnvironmentSpec(BaseGraphQLEntity):
    _depends_on = [EnvironmentInstance]
    _fragment = """
        fragment ExecutionEnvironmentSpec on ExecutionEnvironmentSpecs {
            executionEnvironmentSpecId
            executionEnvironmentSpecName
            createdAt
            isArchived
            environmentInstances(orderBy: { createdAt: DESC }, limit: 1) {
                ...EnvironmentInstance
            }
        }"""

    execution_environment_spec_id: str = Field(..., alias="executionEnvironmentSpecId")
    execution_environment_spec_name: str = Field(..., alias="executionEnvironmentSpecName")
    created_at: datetime = Field(..., alias="createdAt")
    is_archived: bool = Field(..., alias="isArchived")
    environment_instances: list[EnvironmentInstance] = Field(..., alias="environmentInstances")


class Run(BaseGraphQLEntity):
    _depends_on = [EnvironmentInstance, Mount, SourceCodeArtifact]
    _fragment = """
        fragment Run on Runs {
          trainingRunId
          specId
          trainingRunName
          runStatus
          createdAt
          startTime
          endTime
          machineSize
          hyperparameters
          cmd
          runInstanceUrl,
          sshPort
          fromRunId,
          restartCounter,
          sourceCode {
            ...SourceCodeArtifact
          }
          environmentInstance {
            ...EnvironmentInstance
          }
          mounts {
            ...Mount
          }
        }
        """
    run_id: str = Field(..., alias="trainingRunId")
    spec_id: str = Field(..., alias="specId")
    run_name: str = Field(..., alias="trainingRunName")
    run_status: schemas.ComponentInstanceStatus = Field(..., alias="runStatus")
    created_at: datetime = Field(..., alias="createdAt")
    start_time: Optional[datetime] = Field(None, alias="startTime")
    end_time: Optional[datetime] = Field(None, alias="endTime")
    machine_size: schemas.MachineSize = Field(..., alias="machineSize")
    hyperparameters: Optional[str] = None
    cmd: Optional[str] = None
    source_code: SourceCodeArtifact = Field(..., alias="sourceCode")
    environment_instance: EnvironmentInstance = Field(..., alias="environmentInstance")
    mounts: list[Mount] = Field(..., alias="mounts")
    ssh_port: Optional[int] = Field(..., alias="sshPort")
    run_instance_url: Optional[str] = Field(..., alias="runInstanceUrl")
    from_run_id: Optional[str] = Field(..., alias="fromRunId")
    restart_counter: Optional[int] = Field(..., alias="restartCounter")


class Volume(BaseGraphQLEntity):
    _depends_on = []
    _fragment = """
        fragment Volume on Volumes {
          volumeId
          volumeName
          createdAt
        }
        """
    volume_id: str = Field(..., alias="volumeId")
    volume_name: str = Field(..., alias="volumeName")
    created_at: datetime = Field(..., alias="createdAt")


class ProjectFields(BaseGraphQLEntity):
    _depends_on = []
    _fragment = """
        fragment ProjectFields on Projects {
          projectId
          displayName
        } """
    project_id: str = Field(..., alias="projectId")
    display_name: str = Field(..., alias="displayName")


class BillingLineItem(BaseGraphQLEntity):
    _depends_on = []
    _fragment = """
        fragment BillingLineItem on BillingLineItems {
          appInstanceId
          deploymentId
          runId
          computeCostCredits
          computeCostCreditsInProgress
        } """
    app_instance_id: Optional[str] = Field(None, alias="appInstanceId")
    deployment_id: Optional[str] = Field(None, alias="deploymentId")
    run_id: Optional[str] = Field(None, alias="runId")
    compute_cost_credits: Optional[int] = Field(None, alias="computeCostCredits")
    compute_cost_credits_in_progress: int = Field(..., alias="computeCostCreditsInProgress")


class ProjectProjection(BaseModel):
    project: Optional[ProjectFields] = None


class UserWithProjects(BaseGraphQLEntity):
    _depends_on = [ProjectFields]
    _fragment = """
        fragment UserWithProjects on Users {
          displayName
          username
          sshPublicKey
          userId
          isActivated
          userProjectAcls(where: {project: {isArchived: {_eq: false}}}) {
            project {
              ...ProjectFields
            }
          }
        } """
    display_name: str = Field(..., alias="displayName")
    username: str = Field(..., alias="username")
    ssh_public_key: Optional[str] = Field(None, alias="sshPublicKey")
    user_id: str = Field(..., alias="userId")
    user_project_acls: list[ProjectProjection] = Field(..., alias="userProjectAcls")
    is_activated: bool = Field(..., alias="isActivated")

    @property
    def projects(self) -> list[ProjectFields]:
        return [acl.project for acl in self.user_project_acls if acl.project]  # Filter out None values


class ServiceAccount(BaseGraphQLEntity):
    _depends_on = []
    _fragment = """
        fragment ServiceAccount on ServiceAccounts {
              serviceAccountId
              nickname
              lastFour
              apiKeyHash
              createdAt
        } """
    service_account_id: str = Field(..., alias="serviceAccountId")
    nickname: Optional[str] = Field(None, alias="nickname")
    last_four: str = Field(..., alias="lastFour")
    api_key_hash: str = Field(..., alias="apiKeyHash")
    created_at: datetime = Field(..., alias="createdAt")


class ServiceAccountWithProjects(ServiceAccount):
    _depends_on = [ProjectFields, ServiceAccount]
    _fragment = """
        fragment ServiceAccountWithProjects on ServiceAccounts {
          ...ServiceAccount
          serviceAccountProjectAcls {
            project {
              ...ProjectFields
            }
          }
        } """

    service_account_project_acls: list[ProjectProjection] = Field(..., alias="serviceAccountProjectAcls")

    @property
    def projects(self) -> list[ProjectFields]:
        return [acl.project for acl in self.service_account_project_acls if acl.project]  # Filter out None values


class MeResponse(BaseModel):
    projects: list[ProjectFields]
    user: Optional[UserWithProjects] = None
    service_account: Optional[ServiceAccountWithProjects] = None

    @classmethod
    def from_user(cls, user: UserWithProjects) -> MeResponse:
        return cls(projects=user.projects, user=user)

    @classmethod
    def from_service_account(cls, service_account: ServiceAccountWithProjects) -> MeResponse:
        return cls(projects=service_account.projects, service_account=service_account)


class MountSpec(BaseGraphQLEntity):
    _depends_on = []
    _fragment = """
        fragment MountSpec on MountSpecs {
            path
            mode
            name
            tag
            referencedProjectId
        }
    """
    path: str = Field(..., alias="path")
    mode: Literal["DOWNLOAD", "UPLOAD", "VOLUME"] = Field(..., alias="mode")
    name: str = Field(..., alias="name")
    tag: Optional[str] = Field(None, alias="tag")
    referenced_project_id: Optional[str] = Field(None, alias="referencedProjectId")


class _ComponentSpecAppInstanceProjection(BaseModel):
    app_instance_status: schemas.ComponentInstanceStatus = Field(..., alias="appInstanceStatus")
    app_instance_url: Optional[str] = Field(None, alias="appInstanceUrl")
    created_at: datetime = Field(..., alias="createdAt")
    ssh_port: Optional[int] = Field(None, alias="sshPort")


class _ComponentSpecRunProjection(BaseModel):
    training_run_id: str = Field(..., alias="trainingRunId")
    created_at: datetime = Field(..., alias="createdAt")
    ssh_port: Optional[int] = Field(None, alias="sshPort")
    run_status: schemas.ComponentInstanceStatus = Field(..., alias="runStatus")


class ComponentSpec(BaseGraphQLEntity):
    _depends_on = [ExecutionEnvironmentSpec, MountSpec, Deployment, Run]
    _fragment = """
        fragment ComponentSpec on ComponentSpecs {
            specId
            specName
            command
            componentType
            appSubType
            projectId
            machineSize
            configVariables
            serviceAccount
            appPort
            batchSize
            batchInterval
            executionEnvironmentSpec {
                ...ExecutionEnvironmentSpec
            }
            mountSpecs {
                ...MountSpec
            }
            appInstances(orderBy:{ createdAt:DESC }, limit: 1) {
                appInstanceStatus
                appInstanceUrl
                createdAt
                sshPort
            }
            deployments(orderBy:{ createdAt:DESC }, limit:1) {
                ...Deployment
            }
            runs(orderBy:{ createdAt:DESC }, limit: 1) {
                trainingRunId
                createdAt
                runStatus
                sshPort
                runInstanceUrl
            }
        }
    """
    spec_id: str = Field(..., alias="specId")
    spec_name: str = Field(..., alias="specName")
    command: Optional[str] = Field(None, alias="command")
    component_type: schemas.ComponentType = Field(..., alias="componentType")
    app_sub_type: Optional[schemas.AppSubType] = Field(None, alias="appSubType")
    app_port: Optional[int] = Field(None, alias="appPort")
    config_variables: Optional[str] = Field(None, alias="configVariables")
    batch_size: Optional[int] = Field(None, alias="batchSize")
    batch_interval: Optional[int] = Field(None, alias="batchInterval")
    project_id: str = Field(..., alias="projectId")
    machine_size: schemas.MachineSize = Field(..., alias="machineSize")
    service_account: bool = Field(..., alias="serviceAccount")
    execution_environment_spec: Optional[ExecutionEnvironmentSpec] = Field(None, alias="executionEnvironmentSpec")
    mount_specs: list[MountSpec] = Field(..., alias="mountSpecs")
    app_instances: list[_ComponentSpecAppInstanceProjection] = Field(..., alias="appInstances")
    deployments: list[Deployment] = Field(..., alias="deployments")
    runs: list[_ComponentSpecRunProjection] = Field(..., alias="runs")

    @property
    def app_instance_status(self) -> schemas.ComponentInstanceStatus | None:
        if self.app_instances:
            return self.app_instances[0].app_instance_status
        return None

    @property
    def app_instance_url(self) -> str | None:
        if self.app_instances:
            return self.app_instances[0].app_instance_url
        return None

    @property
    def last_created_at(self) -> datetime | None:
        if self.app_instances:
            return self.app_instances[0].created_at
        if self.deployments:
            return self.deployments[0].created_at
        return None

    @property
    def deployment_status(self) -> schemas.ComponentInstanceStatus | None:
        if self.deployments:
            return self.deployments[0].deployment_status
        return None

    @property
    def friendly_component_type(self) -> str:
        return (self.app_sub_type or self.component_type).value.lower()


class AppInstance(BaseGraphQLEntity):
    _depends_on = [ComponentSpec]
    _fragment = """
        fragment AppInstance on AppInstances {
            appInstanceId
            appInstanceStatus
            appInstanceUrl
            appSubType
            appPort
            sshPort
            environmentInstanceId
            createdAt
            command
            specId
            componentSpec {
                ...ComponentSpec
            }
        }
    """
    app_instance_id: str = Field(..., alias="appInstanceId")
    app_instance_status: schemas.ComponentInstanceStatus = Field(..., alias="appInstanceStatus")
    app_instance_url: Optional[str] = Field(None, alias="appInstanceUrl")
    app_sub_type: Optional[schemas.AppSubType] = Field(None, alias="appSubType")
    app_port: Optional[int] = Field(None, alias="appPort")
    ssh_port: Optional[int] = Field(None, alias="sshPort")
    environment_instance_id: Optional[str] = Field(None, alias="environmentInstanceId")
    created_at: datetime = Field(..., alias="createdAt")
    command: Optional[str] = Field(None, alias="command")
    spec_id: str = Field(..., alias="specId")
    component_spec: ComponentSpec = Field(..., alias="componentSpec")


class ProjectSecret(BaseGraphQLEntity):
    _depends_on = []
    _fragment = """
        fragment ProjectSecret on ProjectSecrets {
          secretName
        }
    """
    secret_name: str = Field(..., alias="secretName")


class DeploymentInstance(BaseGraphQLEntity):
    _depends_on = [ComponentSpec, SourceCodeArtifact]
    _fragment = """
        fragment DeploymentInstance on Deployments {
          createdAt
          deploymentId
          deploymentStatus
          projectId
          machineSize
          environmentInstanceId
          specId
          sourceCode {
            ...SourceCodeArtifact
          }
          componentSpec {
            ...ComponentSpec
          }
        } """

    deployment_id: str = Field(..., alias="deploymentId")
    created_at: datetime = Field(..., alias="createdAt")
    deployment_status: schemas.ComponentInstanceStatus = Field(..., alias="deploymentStatus")
    project_id: str = Field(..., alias="projectId")
    source_code: SourceCodeArtifact = Field(..., alias="sourceCode")
    machine_size: schemas.MachineSize = Field(..., alias="machineSize")
    environment_instance_id: str = Field(..., alias="environmentInstanceId")
    spec_id: str = Field(..., alias="specId")
    component_spec: ComponentSpec = Field(..., alias="componentSpec")
