from __future__ import annotations

import asyncio
import contextlib
import datetime
import json
import logging
from typing import (
    Annotated,
    Any,
    AsyncGenerator,
    AsyncIterator,
    Awaitable,
    BinaryIO,
    Callable,
    Coroutine,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)

import aiohttp
import backoff
import sentry_sdk
from aiohttp import ClientTimeout, FormData, WSMessage
from pydantic import BaseModel, Field, TypeAdapter, ValidationError

from .. import schemas
from ..schemas import AuthTokenUnion, CreateServiceAccountResponse, Hyperparameter, MachineSize
from ..shared.utils import get_data_or_raise
from . import config
from .errors import (
    SlingshotBackoffError,
    SlingshotClientHttpException,
    SlingshotConnectionError,
    SlingshotException,
    SlingshotJWSInvalidSignature,
    SlingshotJWTExpiredError,
    SlingshotUnauthenticatedError,
)
from .graphql import BaseGraphQLQuery, base_graphql, fragments, queries
from .graphql.queries import (
    BlobArtifactsForProjectResponse,
    ProjectSecretsQuery,
    ProjectSecretsResponse,
    RunByIdResponse,
    ServiceAccountWithProjectsResponse,
)
from .utils import console

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Union[BaseModel, str, bytes, tuple[Any, ...], list[Any], dict[str, Any]])
ModelT = TypeVar("ModelT", bound=BaseModel)
JSONType = dict[str, Any]
ParamsType = dict[str, Union[str, float, int]]


class Retry(Exception):
    pass


class SlingshotClient:
    def __init__(
        self,
        *,
        auth_token: AuthTokenUnion | None = None,
        slingshot_url: str = config.global_config.slingshot_backend_url,
        hasura_admin_secret: str | None = config.global_config.hasura_admin_secret,
        auto_setup_hook: Callable[[], Awaitable[None]] | None = None,
    ) -> None:
        self._slingshot_url = slingshot_url.rstrip("/")
        self._api_url = slingshot_url.rstrip("/") + "/api"
        self._graphql_url = slingshot_url.rstrip("/") + "/graphql/v1/graphql"
        self.auth_token: AuthTokenUnion | None = auth_token
        self._hasura_admin_secret = hasura_admin_secret

        self._session: aiohttp.ClientSession | None = None
        self._auto_setup_hook = auto_setup_hook
        self._is_setup = not auto_setup_hook  # False, unless auto_setup_hook is None
        self.project: schemas.Project | None = None

    @property
    def _headers(self) -> dict[str, str]:
        if self.auth_token is None:
            headers = {}
        else:
            # We need to set Cookie since Hasura only uses this header for auth
            headers = {"Cookie": f"token={self.auth_token.token}"}
        return headers

    @contextlib.asynccontextmanager
    async def use_http_session(self) -> AsyncGenerator[SlingshotClient, None]:
        """Optional: Use this to reuse a session across multiple requests."""
        async with _maybe_make_http_session(self._session) as session:
            self._session = session
            yield self

    async def _maybe_setup(self) -> None:
        if self._is_setup:
            return
        if self._auto_setup_hook is None:
            return
        await self._auto_setup_hook()

    @backoff.on_exception(backoff.expo, (SlingshotBackoffError,), max_tries=3)
    async def make_request(
        self,
        url: str,
        *,
        method: str,
        response_model: Type[T] | None,
        params: ParamsType | None = None,
        json_data: JSONType | str | None = None,
        data: dict[str, Any] | FormData | BinaryIO | bytes | None = None,
        headers: dict[str, str] | None = None,
        timeout: datetime.timedelta | None = None,
        _setup: bool = True,
    ) -> T:
        # If the url is relative, we need to prepend the base url
        if not url.startswith("http"):
            url = f"{self._api_url.rstrip('/')}/{url.lstrip('/')}"
        if _setup:
            await self._maybe_setup()

        timeout = timeout or datetime.timedelta(seconds=60)
        headers = headers or {}
        headers = {**self._headers, **headers}  # The order matters here, so the caller can override headers
        logger.debug(f"Making a '{method}' request to '{url}'")
        try:
            async with _maybe_make_http_session(self._session) as session:
                async with session.request(
                    url=url,
                    method=method,
                    params=params,
                    json=json_data,
                    data=data,
                    headers=headers,
                    timeout=int(timeout.total_seconds()),
                    max_redirects=0,
                ) as resp:
                    logger.debug(f"Got response from '{url}': {resp.status}")
                    if 400 <= resp.status <= 600:
                        exception = await SlingshotClientHttpException.from_response(resp)
                        if resp.status == 503 or resp.status == 429:
                            raise SlingshotBackoffError(f"Service unavailable: {resp.status}")
                        if 500 <= resp.status <= 600:
                            if self._slingshot_url != config.global_config.slingshot_local_url:
                                sentry_sdk.capture_exception(exception)
                        raise exception
                    if response_model == aiohttp.ClientResponse:
                        # This is safe as response_model is of type T and resp matches
                        return resp  # type: ignore
                    elif response_model is None:
                        return await resp.text()  # type: ignore
                    elif response_model == bytes:
                        # Safe at runtime, response model matches type of T
                        return await resp.content.read()  # type: ignore
                    elif response_model == str:
                        return await resp.json()
                    resp_data: dict[str, Any] | FormData | None = await resp.json()
        except aiohttp.ClientConnectorError as e:
            if self._slingshot_url != config.global_config.slingshot_local_url:
                sentry_sdk.capture_exception(e, api_url=self._api_url)
            raise SlingshotConnectionError(self._api_url) from e
        try:
            return TypeAdapter(response_model).validate_python(resp_data)
        except ValidationError as e:
            if self._slingshot_url != config.global_config.slingshot_local_url:
                with sentry_sdk.push_scope() as scope:
                    scope.set_extra("response", resp_data)
                    scope.set_extra("response_model", response_model)
                    sentry_sdk.capture_exception(e, api_url=self._api_url)
            raise SlingshotException(f"Unexpected response format. {e}: {resp_data}") from e

    async def make_graphql_request(
        self, gql_query: BaseGraphQLQuery[ModelT], _setup: bool = True
    ) -> base_graphql.GraphQLResponse[ModelT]:
        if _setup:
            await self._maybe_setup()
        query = gql_query.query
        variables = gql_query.variables
        response_model = gql_query.response_model
        # We need to instantiate the specific generic type here but MyPy doesn't like it much as we're mixing types
        # and variables. This works though, don't mess with it!
        type_: base_graphql.GraphQLResponse[ModelT] = base_graphql.GraphQLResponse[response_model]  # type: ignore
        headers = self._headers
        if self._hasura_admin_secret:
            headers["x-hasura-admin-secret"] = self._hasura_admin_secret
        logger.debug(f"Making query request to {query.strip()} with variables {variables}")
        return await self.make_request(
            self._graphql_url,
            method="post",
            _setup=_setup,
            response_model=type_,  # type: ignore
            json_data={"query": query, "variables": variables},
            headers=headers,
        )

    # noinspection PyUnresolvedReferences
    async def make_graphql_subscription_request(
        self, gql_query: BaseGraphQLQuery[ModelT]
    ) -> AsyncGenerator[base_graphql.GraphQLResponse[ModelT], None]:
        query = gql_query.query
        variables = gql_query.variables
        response_model = gql_query.response_model
        headers = self._headers
        if self._hasura_admin_secret:
            headers["x-hasura-admin-secret"] = self._hasura_admin_secret
        logger.debug(f"Making query request to {query.strip().splitlines()[0]}")
        # We need to instantiate the specific generic type here but MyPy doesn't like it much as we're mixing types
        # and variables. This works though, don't mess with it!
        type_: base_graphql.GraphQLSubscriptionResponse[T] = base_graphql.GraphQLSubscriptionResponse[response_model]  # type: ignore
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(self._graphql_url) as ws:
                    await ws.send_json({"type": "connection_init", "payload": {"headers": headers}})
                    await ws.send_json(
                        {"id": "1", "type": "start", "payload": {"query": query, "variables": variables}}
                    )
                    msg: WSMessage
                    async for msg in ws:
                        logger.debug(f"Received message: {msg}")
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            if data["type"] == "connection_error":
                                raise SlingshotException(f"WebSocket connection error: {data['payload']}")
                            elif "errors" in data:
                                raise SlingshotException(f"GraphQL error: {data['errors']}")
                            elif data["type"] == "data":
                                yield type_.model_validate(data).payload
                            else:
                                logger.debug(f"Received unexpected message: {data}")
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            raise SlingshotException(f"WebSocket error: {msg.data}")

            logger.info("Websocket connection closed -- retrying")

    @contextlib.asynccontextmanager
    async def async_http_get_with_unlimited_timeout(self, url: str) -> AsyncIterator[aiohttp.ClientResponse]:
        """
        Make an async HTTP GET request to the given URL. This is useful for streaming downloads for large files.
        """
        async with _maybe_make_http_session(self._session) as session:
            async with session.get(url, timeout=ClientTimeout(total=None)) as resp:
                if 400 <= resp.status <= 600:
                    raise await SlingshotClientHttpException.from_response(resp)
                yield resp


class SlingshotAPI:
    def __init__(self, client: SlingshotClient) -> None:
        self._client = client

    @contextlib.asynccontextmanager
    async def use_http_session(self) -> AsyncGenerator[SlingshotAPI, None]:
        """Optional: Use this to reuse a session across multiple requests."""
        async with self._client.use_http_session():
            yield self

    """
    Misc API methods
    """

    async def get_backend_version(self) -> str:
        """Get the current version of the backend."""
        return await self._client.make_request("version", method="get", response_model=str, _setup=False)

    async def list_machine_types(self) -> list[schemas.MachineTypeListItem]:
        """Get a list of available machine types."""
        return await self._client.make_request(
            "machine_types", method="get", response_model=list[schemas.MachineTypeListItem]
        )

    async def project_id_available(self, project_id: str) -> bool:
        """Check if a project ID is available."""
        resp = await self._client.make_request(
            "/project/project_id_available", method="post", json_data=project_id, response_model=schemas.BoolResponse
        )
        return get_data_or_raise(resp)

    """
    Auth API methods
    """

    async def user_login(self, auth0_token: str) -> schemas.AuthToken:
        """Sign in with an Auth0 CLI token."""
        auth_token_resp: schemas.AuthTokenResponse = await self._client.make_request(
            f"auth/token",
            method="post",
            response_model=schemas.AuthTokenResponse,
            _setup=False,
            json_data={"token": auth0_token, "cli": True},
        )
        auth_token = get_data_or_raise(auth_token_resp)
        logger.info("Signed in successfully")
        return auth_token

    async def sa_login(self, api_key: str) -> schemas.ServiceAccountToken:
        """Sign in with a Slingshot project API key. If no API key is provided, the API key will be read from the
        environment variable `SLINGSHOT_API_KEY`"""
        try:
            sa_token_resp: schemas.Response[schemas.ServiceAccountToken] = await self._client.make_request(
                "/auth/service_account/token",
                method="post",
                _setup=False,
                response_model=schemas.Response[schemas.ServiceAccountToken],
                headers={"token": api_key},
            )
        except SlingshotClientHttpException as e:
            if e.status == 401 and (msg := e.json and e.json.get("error")):
                # Usually this means the API key is invalid
                raise SlingshotException(msg)
            raise e
        return get_data_or_raise(sa_token_resp)

    async def get_auth0_cli_metadata(self) -> schemas.Auth0MetadataResponse:
        """Get metadata for the Auth0 CLI."""
        return await self._client.make_request(
            url=f"auth/auth0_cli", method="get", response_model=schemas.Auth0MetadataResponse, _setup=False
        )

    """
    User API methods
    """

    async def me_user(self, user_id: str) -> fragments.UserWithProjects:
        """Get the current user."""
        resp = await self._client.make_graphql_request(queries.UserWithProjectsQuery(user_id=user_id))
        if resp.errors:
            if SlingshotJWTExpiredError.graphql_message in resp.errors[0].message:
                raise SlingshotJWTExpiredError()
            if SlingshotUnauthenticatedError.graphql_message in resp.errors[0].message:
                raise SlingshotUnauthenticatedError()
            if SlingshotJWSInvalidSignature.graphql_message in resp.errors[0].message:
                raise SlingshotJWSInvalidSignature()
            else:
                raise SlingshotException(resp.errors[0].message)
        if not (data := resp.data):
            raise SlingshotException("No user found with given id")
        if not (user := data.users_by_pk):
            raise SlingshotException("No user found with given id")
        return user

    async def me_service_account(self, service_account_id: str) -> fragments.ServiceAccountWithProjects:
        """Get the current service account."""
        resp: base_graphql.GraphQLResponse[
            ServiceAccountWithProjectsResponse
        ] = await self._client.make_graphql_request(
            queries.ServiceAccountWithProjectsQuery(service_account_id=service_account_id)
        )
        if resp.errors:
            if SlingshotJWTExpiredError.graphql_message in resp.errors[0].message:
                raise SlingshotJWTExpiredError()
            if SlingshotUnauthenticatedError.graphql_message in resp.errors[0].message:
                raise SlingshotUnauthenticatedError()
            if SlingshotJWSInvalidSignature.graphql_message in resp.errors[0].message:
                raise SlingshotJWSInvalidSignature()
            else:
                raise SlingshotException(resp.errors[0].message)
        if not (data := resp.data):
            raise SlingshotException("Service account not found")
        if not (service_account := data.service_accounts_by_pk):
            raise SlingshotException("Service account not found")
        return service_account

    async def update_ssh_public_key(self, key: str) -> None:
        """Update the current user's SSH public key."""
        await self._client.make_request(
            url=f"user/me/ssh_public_key",
            method="put",
            json_data={"ssh_public_key": key},
            response_model=schemas.ResponseOK,
        )

    async def create_service_account(self, project_id: str) -> CreateServiceAccountResponse:
        response = await self._client.make_request(
            url=f"project/{project_id}/service_account",
            method="post",
            response_model=schemas.Response[CreateServiceAccountResponse],
        )
        return get_data_or_raise(response)

    """
    Get API methods
    """

    async def get_billing_line_items_by_app_id(self, app_instance_id: str) -> list[fragments.BillingLineItem]:
        query = queries.BillingLineItemsByAppIdQuery(app_instance_id=app_instance_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        return data.billingLineItems

    async def get_billing_line_items_by_deployment_id(self, deployment_id: str) -> list[fragments.BillingLineItem]:
        query = queries.BillingLineItemsByDeploymentIdQuery(deployment_id=deployment_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        return data.billingLineItems

    async def get_billing_line_items_by_run_id(self, run_id: str) -> list[fragments.BillingLineItem]:
        query = queries.BillingLineItemsByRunIdQuery(run_id=run_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        return data.billingLineItems

    async def get_project_by_id(self, project_id: str, *, _setup: bool = True) -> fragments.ProjectFields | None:
        """Get a project by id."""
        query = queries.ProjectByIdQuery(project_id=project_id)
        resp = await self._client.make_graphql_request(query, _setup=_setup)
        if not resp.data:
            return None
        project = resp.data.projects_by_pk
        return project

    async def get_latest_app_instance_for_app_spec(self, spec_id: str) -> fragments.AppInstance | None:
        """Get the latest app instance for a component."""
        query = queries.LatestAppInstanceForComponentQuery(spec_id=spec_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        app_instance = data.app_instances[0] if data and data.app_instances else None
        return app_instance

    async def get_latest_deployment_instance_for_deployment_spec(
        self, deployment_spec_id: str
    ) -> fragments.DeploymentInstance | None:
        """Get the latest deployment instance for a component spec."""
        query = queries.LatestDeploymentInstanceForComponentQuery(spec_id=deployment_spec_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        deployment_instance = data.deployment_instances[0] if data and data.deployment_instances else None
        return deployment_instance

    async def get_app_instance(self, app_instance_id: str, project_id: str) -> fragments.AppInstance | None:
        """Get an app instance by id."""
        query = queries.AppInstanceQuery(app_instance_id=app_instance_id, project_id=project_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        return (data and data.app_instances and data.app_instances[0]) or None

    async def get_component_spec_by_id(self, spec_id: str, project_id: str) -> fragments.ComponentSpec | None:
        """Get a component spec by id."""
        query = queries.ComponentSpecByIdQuery(spec_id=spec_id, project_id=project_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        assert len(data.component_specs) == 1
        return (data and data.component_specs[0]) or None

    async def get_component_spec_by_name(self, spec_name: str, project_id: str) -> fragments.ComponentSpec | None:
        """Get a component spec by name."""
        query = queries.ComponentSpecByNameQuery(spec_name=spec_name, project_id=project_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()

        # If there's no matching app spec for this name, then data.component_specs is an empty list.
        return (data and data.component_specs and data.component_specs[0]) or None

    @overload
    async def get_run(self, *, run_id: str, project_id: str) -> fragments.Run | None:
        ...

    @overload
    async def get_run(self, *, run_name: str, project_id: str) -> fragments.Run | None:
        ...

    async def get_run(
        self, *, run_id: str | None = None, run_name: str | None = None, project_id: str
    ) -> fragments.Run | None:
        """Get a run by id or name."""
        if run_id is None and run_name is None:
            raise ValueError("Either run_id or run_name must be specified")
        if run_id is not None and run_name is not None:
            raise ValueError("Only one of run_id or run_name can be specified")
        if run_id is not None:
            query_by_id: BaseGraphQLQuery[RunByIdResponse] = queries.RunByIdQuery(run_id=run_id)
            resp_by_id = await self._client.make_graphql_request(query_by_id)
            data_by_id: queries.RunByIdResponse = resp_by_id.get_data_or_raise()
            return data_by_id.run
        if run_name is not None:
            query_by_name = queries.RunByNameForProjectQuery(run_name=run_name, project_id=project_id)
            resp_by_name = await self._client.make_graphql_request(query_by_name)
            data_by_name: queries.RunsForProjectResponse = resp_by_name.get_data_or_raise()
            runs = data_by_name.runs
            if len(runs) == 0:
                return None
            if len(runs) > 1:
                raise SlingshotException(f"Found more than one run with name {run_name}")
            return runs[0]
        return None

    async def get_deployment(self, deployment_name: str, *, project_id: str) -> fragments.ComponentSpec | None:
        """Get a deployment by name."""
        query = queries.DeploymentSpecByNameQuery(spec_name=deployment_name, project_id=project_id)

        resp = await self._client.make_graphql_request(query)
        data: queries.ComponentSpecsResponse = resp.get_data_or_raise()
        if not data.component_specs:
            return None
        return data.component_specs[0]

    async def get_deployment_latencies(
        self, deployment_id: str, *, project_id: str
    ) -> schemas.UsageBinsLatencyQuantiles:
        """Get the latencies for a deployment."""
        resp = await self._client.make_request(
            url=f"project/{project_id}/deploy/{deployment_id}/latencies",
            method="get",
            response_model=schemas.UsageBinsLatencyQuantilesResponse,
        )
        return get_data_or_raise(resp)

    async def get_environment_spec(
        self, execution_environment_spec_id: str
    ) -> fragments.ExecutionEnvironmentSpec | None:
        """Get an execution environment spec by id."""
        query = queries.ExecutionEnvironmentSpecByIdQuery(execution_environment_spec_id=execution_environment_spec_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        return data.execution_environment_specs_by_pk if data else None

    async def get_blob_artifact_by_id(self, blob_artifact_id: str) -> fragments.BlobArtifact | None:
        """Get a blob artifact by id."""
        query = queries.BlobArtifactByIdQuery(blob_artifact_id=blob_artifact_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        return data.blob_artifacts_by_pk

    async def get_blob_artifact_by_name_and_tag(
        self, artifact_name: str, *, project_id: str, artifact_tag: str | None = None
    ) -> fragments.BlobArtifact | None:
        """Get a blob artifact by id."""
        query = queries.BlobArtifactByNameAndTagQuery(project_id=project_id, name=artifact_name, tag=artifact_tag)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        return data.blob_artifacts[0] if data.blob_artifacts else None

    async def get_latest_source_codes_for_project(self, project_id: str) -> fragments.SourceCodeArtifact | None:
        """Get the latest source code artifact for a project."""
        query = queries.LatestSourceCodeForProjectQuery(project_id=project_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        if not data or not data.projects_by_pk or not data.projects_by_pk.source_codes:
            return None
        return data.projects_by_pk.source_codes[0]

    """
    List API methods
    """

    async def list_component_specs(self, project_id: str) -> list[fragments.ComponentSpec]:
        """List all app specs for a project."""
        query = queries.ComponentSpecsForProjectQuery(project_id=project_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        return data.component_specs

    async def list_runs(self, project_id: str) -> list[fragments.Run]:
        """List all runs for a project."""
        query = queries.RunsForProjectQuery(project_id=project_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        return data and data.runs or []

    async def list_app_instances_by_sub_type(
        self, app_sub_type: schemas.AppSubType, *, project_id: str
    ) -> list[fragments.AppInstance]:
        """List all app instances for a project with a given type."""
        query = queries.AppInstancesByAppSubTypeQuery(app_sub_type=app_sub_type.value, project_id=project_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        return data and data.app_instances or []

    async def list_environment_specs(self, *, project_id: str) -> list[fragments.ExecutionEnvironmentSpec]:
        """List all execution environment specs for a project."""
        query = queries.ExecutionEnvironmentSpecsForProjectQuery(project_id=project_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        return data and data.execution_environment_specs or []

    async def list_artifacts(self, name: str | None, *, project_id: str) -> list[fragments.BlobArtifact]:
        """Get the latest artifacts for a project."""
        query: BaseGraphQLQuery[BlobArtifactsForProjectResponse]
        if name is not None:
            query = queries.LatestBlobArtifactsForProjectByNameQuery(project_id=project_id, name=name)
        else:
            query = queries.LatestBlobArtifactsForProjectQuery(project_id=project_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        if not data or not data.projects_by_pk or not data.projects_by_pk.blob_artifacts:
            return []

        return data.projects_by_pk.blob_artifacts

    async def list_volumes(self, *, project_id: str) -> list[fragments.Volume]:
        """Get the volumes for a project."""
        query = queries.VolumesForProjectQuery(project_id=project_id)
        resp = await self._client.make_graphql_request(query)
        data = resp.get_data_or_raise()
        return data and data.volumes or []

    async def list_secrets(self, *, project_id: str) -> list[fragments.ProjectSecret]:
        """Get the secrets for a project."""
        query = ProjectSecretsQuery(project_id=project_id)
        resp = await self._client.make_graphql_request(query)
        data: ProjectSecretsResponse = resp.get_data_or_raise()
        return data and data.projects_by_pk and data.projects_by_pk.project_secrets or []

    """
    Follow API methods
    """

    async def follow_app_status(self, spec_id: str) -> AsyncGenerator[schemas.ComponentInstanceStatus, None]:
        """Follow the status of an app spec."""
        query = queries.AppInstanceStatusForSpecSubscription(spec_id=spec_id)
        payload: base_graphql.GraphQLResponse[queries.AppInstancesWithStatusResponse]
        async for payload in self._client.make_graphql_subscription_request(query):
            app_instances = payload.get_data_or_raise().app_instances
            if not app_instances:
                raise SlingshotException("App instances not found")
            yield schemas.ComponentInstanceStatus(app_instances[0].app_instance_status)

    async def follow_run_status(self, run_id: str) -> AsyncGenerator[schemas.ComponentInstanceStatus, None]:
        """Follow the status of a run."""
        query = queries.RunStatusSubscription(run_id=run_id)
        payload: base_graphql.GraphQLResponse[queries.RunsWithStatusResponse]
        async for payload in self._client.make_graphql_subscription_request(query):
            run = payload.get_data_or_raise().run
            if not run:
                raise SlingshotException("Run not found")
            yield schemas.ComponentInstanceStatus(run.run_status)

    async def follow_deployment_status(self, spec_id: str) -> AsyncGenerator[schemas.ComponentInstanceStatus, None]:
        """Follow the status of a deployment."""
        query = queries.DeploymentStatusSubscription(spec_id=spec_id)
        payload: base_graphql.GraphQLResponse[queries.DeploymentInstancesWithStatusResponse]
        async for payload in self._client.make_graphql_subscription_request(query):
            deployment_instances = payload.get_data_or_raise().deployment_instances
            if not deployment_instances:
                raise SlingshotException("Deployment instances not found")
            yield schemas.ComponentInstanceStatus(deployment_instances[0].deployment_instance_status)

    """
    Create API methods
    """

    async def create_project(
        self, project_id: str, project_display_name: Optional[str] = None
    ) -> schemas.Response[schemas.ProjectId]:
        """Create a new project."""
        return await self._client.make_request(
            url=f"project",
            method="post",
            response_model=schemas.Response[schemas.ProjectId],
            json_data=schemas.BodyNewProject(project_id=project_id, display_name=project_display_name).model_dump(),
        )

    async def fork_project(
        self, project_id: str, *, new_project_id: str | None = None, new_display_name: str | None = None
    ) -> schemas.Response[schemas.ProjectId]:
        """
        Create a new project by forking an existing one.

        If new_project_id or new_display_name are omitted, default ones are generated by slingshot based on the source
        project_id.
        """
        return await self._client.make_request(
            url=f"project/{project_id}/fork",
            method="post",
            response_model=schemas.Response[schemas.ProjectId],
            json_data=schemas.BodyForkProject(
                new_project_id=new_project_id, new_display_name=new_display_name
            ).model_dump(),
        )

    async def create_app(
        self,
        name: str,
        command: str | None,
        component_type: schemas.ComponentType,
        app_sub_type: schemas.AppSubType | None,
        exec_env_spec_id: str | None,
        machine_size: schemas.MachineSize,
        mounts: list[schemas.MountSpecUnion],
        attach_project_credentials: bool,
        config_variables: JSONType | None = None,
        app_port: int | None = None,
        import_run_spec_id: str | None = None,
        export_run_spec_id: str | None = None,
        *,
        project_id: str,
    ) -> schemas.ComponentSpecIdResponse:
        """Create an app spec."""
        body = schemas.CreateAppBody(
            name=name,
            command=command,
            component_type=component_type,
            app_sub_type=app_sub_type,
            exec_env_spec_id=exec_env_spec_id,
            machine_size=machine_size,
            mounts=[_mount_spec_to_request(mount) for mount in mounts],
            attach_project_credentials=attach_project_credentials,
            config_variables=config_variables,
            app_port=app_port,
            import_run_spec_id=import_run_spec_id,
            export_run_spec_id=export_run_spec_id,
        ).model_dump()
        body["machine_size"] = machine_size.value

        return await self._client.make_request(
            url=f"project/{project_id}/apps",
            method="post",
            response_model=schemas.ComponentSpecIdResponse,
            json_data=body,
        )

    async def create_or_update_environment_spec(
        self,
        name: str,
        requested_python_requirements: list[schemas.RequestedRequirement] | None = None,
        requested_apt_requirements: list[schemas.RequestedAptPackage] | None = None,
        post_install_command: str | None = None,
        force_create_environment: bool = False,
        *,
        project_id: str,
    ) -> schemas.CreateEnvironmentSpecResponse:
        """Create or update an environment spec."""
        python_packages = [req.model_dump() for req in requested_python_requirements or []]
        apt_packages = [req.model_dump() for req in requested_apt_requirements or []]
        body = schemas.ExecutionEnvironmentSpecRequestBody(
            name=name,
            # The following two fields must be dicts, otherwise we get a parsing error since we override the generated
            # API models with custom validators
            python_packages=python_packages,  # type: ignore
            apt_packages=apt_packages,  # type: ignore
            post_install_command=post_install_command or "",
            force_create_environment=force_create_environment,
        )
        return await self._client.make_request(
            url=f"project/{project_id}/environment",
            method="post",
            response_model=schemas.CreateEnvironmentSpecResponse,
            json_data=body.model_dump(),
        )

    async def create_volume(self, volume_name: str, *, project_id: str) -> schemas.Response[str]:
        """Create a volume."""
        return await self._client.make_request(
            url=f"project/{project_id}/volume",
            method="post",
            response_model=schemas.Response[str],
            json_data={"name": volume_name},
        )

    """
    Update API methods
    """

    async def update_app(
        self,
        spec_id: str,
        command: str | None,
        exec_env_spec_id: str | None,
        machine_size: MachineSize,
        mounts: list[schemas.MountSpecUnion],
        attach_project_credentials: bool,
        config_variables: JSONType | None = None,
        app_port: int | None = None,
        batch_size: int | None = None,
        batch_interval: int | None = None,
        import_run_spec_id: str | None = None,
        export_run_spec_id: str | None = None,
        *,
        project_id: str,
    ) -> schemas.BoolResponse:
        """Update an app spec."""
        body = schemas.UpdateAppBody(
            command=command,
            exec_env_spec_id=exec_env_spec_id,
            machine_size=machine_size,
            mounts=[_mount_spec_to_request(mount) for mount in mounts],
            config_variables=config_variables,
            attach_project_credentials=attach_project_credentials,
            app_port=app_port,
            batch_size=batch_size,
            batch_interval=batch_interval,
            import_run_spec_id=import_run_spec_id,
            export_run_spec_id=export_run_spec_id,
        ).model_dump()
        # TODO: Find a way for pydantic not to convert machine_size to an enum
        body["machine_size"] = machine_size.value
        return await self._client.make_request(
            url=f"project/{project_id}/apps/{spec_id}",
            method="post",
            response_model=schemas.BoolResponse,
            json_data=body,
        )

    async def put_secret(
        self, secret_name: str, secret_value: str, *, project_id: str
    ) -> schemas.ProjectSecretResponse:
        """Update a secret by name."""
        return await self._client.make_request(
            url=f"project/{project_id}/secret/{secret_name}",
            method="put",
            response_model=schemas.ProjectSecretResponse,
            json_data={"secret_value": secret_value},
        )

    """
    Delete API methods
    """

    async def delete_app(self, spec_id: str, project_id: str) -> schemas.ResponseOK:
        """Delete an app spec."""
        return await self._client.make_request(
            url=f"project/{project_id}/apps/{spec_id}", method="delete", response_model=schemas.ResponseOK
        )

    async def delete_environment_spec(self, execution_environment_spec_id: str) -> None:
        """Delete an environment spec."""
        mutation = queries.ArchiveExecutionEnvironmentSpecMutation(
            execution_environment_spec_id=execution_environment_spec_id, is_archived=True
        )
        resp = await self._client.make_graphql_request(mutation)
        resp.get_data_or_raise()
        return None

    async def delete_volume(self, volume_name: str, *, project_id: str) -> schemas.BoolResponse:
        """Delete a volume."""
        return await self._client.make_request(
            url=f"project/{project_id}/volume/{volume_name}", method="delete", response_model=schemas.BoolResponse
        )

    async def delete_secret(self, secret_name: str, *, project_id: str) -> schemas.BoolResponse:
        """Delete a secret by name."""
        return await self._client.make_request(
            url=f"project/{project_id}/secret/{secret_name}", method="delete", response_model=schemas.BoolResponse
        )

    """
    Start API methods
    """

    async def start_app(
        self,
        *,
        component_spec: fragments.ComponentSpec,
        machine_size: schemas.MachineSize | None = None,
        source_code_id: str | None = None,
        cmd: str | None = None,
        mount_specs: list[schemas.MountSpecUnion] | None = None,
        config_variables: JSONType | None = None,
        env_instance_id: str | None = None,
        attach_project_credentials: bool | None = None,
        app_port: int | None = None,
        project_id: str,
    ) -> schemas.HasAppInstanceIdResponse:
        """Start an app."""
        machine_size = machine_size or component_spec.machine_size
        command = cmd or component_spec.command
        if mount_specs is None:
            mount_specs = [schemas.remote_mount_spec_to_local(mount_spec) for mount_spec in component_spec.mount_specs]
        if config_variables is None and component_spec.config_variables is not None:
            config_variables = json.loads(component_spec.config_variables)
        if env_instance_id is None:
            env_spec = component_spec.execution_environment_spec
            env_instance_id = env_spec.environment_instances[0].environment_instance_id if env_spec else None
        attach_project_credentials = (
            attach_project_credentials if attach_project_credentials is not None else component_spec.service_account
        )
        app_port = app_port or component_spec.app_port
        body = schemas.StartAppBody(
            machine_size=machine_size,
            source_code_id=source_code_id,
            cmd=command,
            mounts=[_mount_spec_to_request(mount) for mount in mount_specs],
            config_variables=config_variables,
            environment_instance_id=env_instance_id,
            attach_project_credentials=attach_project_credentials,
            app_port=app_port,
        )

        return await self._client.make_request(
            url=f"project/{project_id}/apps/{component_spec.spec_id}/start",
            method="post",
            response_model=schemas.HasAppInstanceIdResponse,
            json_data=body.model_dump(),
        )

    async def start_run(
        self,
        run_spec: fragments.ComponentSpec,
        source_code_id: str | None = None,
        machine_size: Optional[schemas.MachineSize] = None,
        hyperparameters: Hyperparameter | None = None,
        cmd: str | None = None,
        mount_specs: list[schemas.MountSpecUnion] | None = None,
        environment_instance_id: str | None = None,
        attach_project_credentials: bool | None = None,
        debug_mode: bool = False,  # TODO: maybe don't expose this to the user
        *,
        project_id: str,
    ) -> schemas.RunCreateResponse:
        """Start a run."""
        machine_size = machine_size or run_spec.machine_size
        if not hyperparameters and run_spec.config_variables:
            hyperparameters = json.loads(run_spec.config_variables)
        command = cmd or run_spec.command
        if environment_instance_id is None:
            env_spec = run_spec.execution_environment_spec
            assert env_spec is not None, "Run must have environment"
            environment_instance_id = env_spec.environment_instances[0].environment_instance_id

        should_attach_project_credentials = (
            attach_project_credentials if attach_project_credentials is not None else run_spec.service_account
        )

        mount_specs = mount_specs or [
            schemas.remote_mount_spec_to_local(mount_spec) for mount_spec in run_spec.mount_specs
        ]
        download_mount_specs: list[schemas.DownloadMountSpec] = [
            spec for spec in mount_specs if isinstance(spec, schemas.DownloadMountSpec)
        ]
        for mount in download_mount_specs:
            artifact_name = mount.selector.name
            artifact_tag = mount.selector.tag
            artifact_project_id = mount.selector.project or project_id
            artifacts = await self.get_blob_artifact_by_name_and_tag(
                artifact_name=artifact_name, artifact_tag=artifact_tag, project_id=artifact_project_id
            )
            if not artifacts:
                console.print(
                    f"[yellow]Warning[/yellow]: No artifacts found for artifact '{artifact_project_id + '/' if mount.selector.project else ''}{artifact_name}:{artifact_tag}' "
                    f"-- this will cause '{mount.path}' to be mounted as an empty directory."
                )

        body = schemas.StartAppBody(
            source_code_id=source_code_id,
            machine_size=machine_size,
            config_variables=hyperparameters,
            cmd=command,
            mounts=[_mount_spec_to_request(mount) for mount in mount_specs],
            environment_instance_id=environment_instance_id,
            attach_project_credentials=should_attach_project_credentials,
        )
        return await self._client.make_request(
            url=f"project/{project_id}/run/{run_spec.spec_id}/start",
            method="post",
            response_model=schemas.RunCreateResponse,
            params={"debug_mode": json.dumps(debug_mode)},
            json_data=body.model_dump(),
        )

    async def deploy_model(
        self,
        source_code_id: str,
        deployment_spec_id: str,
        machine_size: schemas.MachineSize | None = None,
        config_variables: JSONType | None = None,
        mount_specs: list[schemas.MountSpecUnion] | None = None,
        environment_instance_id: str | None = None,
        cmd: str | None = None,
        *,
        project_id: str,
    ) -> schemas.DeploymentInstanceIdResponse:
        """Start a deployment."""
        deployment_spec = await self.get_component_spec_by_id(deployment_spec_id, project_id=project_id)
        if not deployment_spec:
            raise SlingshotException(f"Deployment not found: {deployment_spec_id}")
        machine_size = machine_size or deployment_spec.machine_size
        if not config_variables and deployment_spec.config_variables:
            config_variables = json.loads(deployment_spec.config_variables)
        mount_specs = mount_specs or [
            schemas.remote_mount_spec_to_local(mount_spec) for mount_spec in deployment_spec.mount_specs
        ]
        if not environment_instance_id:
            env_spec = deployment_spec.execution_environment_spec
            assert env_spec is not None, "Deployment must have environment"
            environment_instance_id = env_spec.environment_instances[0].environment_instance_id
        cmd = cmd or deployment_spec.command
        should_attach_project_credentials = deployment_spec.service_account

        body = schemas.StartAppBody(
            source_code_id=source_code_id,
            machine_size=machine_size,
            config_variables=config_variables,
            mounts=[_mount_spec_to_request(mount) for mount in mount_specs],
            environment_instance_id=environment_instance_id,
            cmd=cmd,
            attach_project_credentials=should_attach_project_credentials,
        )
        return await self._client.make_request(
            url=f"project/{project_id}/deploy/{deployment_spec_id}/start",
            method="post",
            response_model=schemas.DeploymentInstanceIdResponse,
            json_data=body.model_dump(),
        )

    async def start_app_ssh(self, spec_id: str, *, project_id: str) -> schemas.Response[schemas.SshPort]:
        """Start SSH for an app, exposing it on a port that we can access from the public Internet."""
        return await self._client.make_request(
            url=f"project/{project_id}/apps/{spec_id}/ssh/start",
            method="post",
            response_model=schemas.Response[schemas.SshPort],
        )

    async def start_run_ssh(self, run_id: str, *, project_id: str) -> schemas.Response[schemas.SshPort]:
        """Start SSH for a run, exposing it on a port that we can access from the public Internet."""
        return await self._client.make_request(
            url=f"project/{project_id}/run/{run_id}/ssh/start",
            method="post",
            response_model=schemas.Response[schemas.SshPort],
        )

    """
    Stop API methods
    """

    async def stop_app(self, spec_id: str, project_id: str) -> schemas.ResponseOK:
        """Stop an app."""
        return await self._client.make_request(
            url=f"project/{project_id}/apps/{spec_id}/stop", method="post", response_model=schemas.ResponseOK
        )

    async def cancel_run(self, run_id: str, *, project_id: str) -> schemas.ResponseOK:
        """Cancel a run."""
        return await self._client.make_request(
            url=f"project/{project_id}/run/{run_id}/cancel", method="post", response_model=schemas.ResponseOK
        )

    async def stop_deployment(self, deployment_spec_id: str, *, project_id: str) -> schemas.ResponseOK:
        """Stop a deployment."""
        return await self._client.make_request(
            url=f"project/{project_id}/deploy/{deployment_spec_id}/stop",
            method="post",
            response_model=schemas.ResponseOK,
        )

    """
    Logs API methods
    """

    async def get_app_logs(self, spec_id: str, project_id: str) -> schemas.ListLogLineResponse:
        """Get logs for an app spec."""
        return await self._client.make_request(
            url=f"project/{project_id}/apps/{spec_id}/logs", method="get", response_model=schemas.ListLogLineResponse
        )

    async def get_run_logs(self, run_id: str, *, project_id: str) -> schemas.ListLogLineResponse:
        """Get logs for a run."""
        return await self._client.make_request(
            url=f"project/{project_id}/run/{run_id}/logs", method="get", response_model=schemas.ListLogLineResponse
        )

    """
    Predict API methods
    """

    async def predict(
        self, project_id: str, deployment_name: str, example_bytes: bytes, timeout_seconds: int = 60
    ) -> schemas.PredictionResponse:
        """Make a prediction."""
        return await self._client.make_request(
            url=f"predict/{project_id}/{deployment_name}",
            method="post",
            response_model=schemas.PredictionResponse,
            timeout=datetime.timedelta(seconds=timeout_seconds),
            data={"example": example_bytes},
        )

    @backoff.on_exception(backoff.expo, (Retry,), max_tries=3)
    async def prompt_openai(
        self,
        request: schemas.PromptOpenAIBody,
        timeout: datetime.timedelta = datetime.timedelta(seconds=600),
        *,
        project_id: str,
    ) -> schemas.OpenAIResponse:
        """Make a prediction to an OpenAI model."""
        # TODO: Add idempotence key. If the client wants to cache, they can set idempotence_key to hash of prompt.
        try:
            return await self._client.make_request(
                url=f"project/{project_id}/prompt/openai",
                method="post",
                response_model=schemas.OpenAIResponse,
                json_data=request.model_dump(),
                timeout=timeout,
            )
        except SlingshotClientHttpException as e:
            if e.status == 429 or e.status == 503:
                raise Retry(e)
            raise e

    """
    Artifact API methods
    """

    async def signed_url_blob_artifact_many(
        self, blob_artifact_id: str, expiration: datetime.timedelta = datetime.timedelta(hours=1), *, project_id: str
    ) -> schemas.ListBlobArtifactSignedURLResponse:
        """Get signed URLs for an artifact's contents."""
        params: dict[str, float | str] = {"expiration_s": expiration.total_seconds()}
        return await self._client.make_request(
            url=f"project/{project_id}/artifact/{blob_artifact_id}/signed_url_many",
            params=params,
            method="get",
            response_model=schemas.ListBlobArtifactSignedURLResponse,
        )

    async def signed_url_blob_artifact(
        self,
        blob_artifact_id: str,
        file_path: str | None = None,
        expiration: datetime.timedelta = datetime.timedelta(hours=1),
        *,
        project_id: str,
    ) -> schemas.BlobArtifactSignedURLResponse:
        """Get a signed URL for an artifact."""
        params: dict[str, float | str] = {"expiration_s": expiration.total_seconds()}
        if file_path:
            params["file_path"] = file_path
        return await self._client.make_request(
            url=f"project/{project_id}/artifact/{blob_artifact_id}/signed_url",
            params=params,
            method="get",
            response_model=schemas.BlobArtifactSignedURLResponse,
        )

    async def upload_signed_url_blob_artifact_many(
        self, filenames: list[str], *, project_id: str, artifact_name: str, artifact_tags: list[str] | None = None
    ) -> schemas.BlobArtifactUploadSignedURLManyResponse:
        """Get signed URLs for an artifact's contents."""
        return await self._client.make_request(
            url=f"project/{project_id}/artifact/upload_signed_url_many",
            method="post",
            json_data=schemas.UploadBlobArtifactManyBody(
                filenames=filenames, artifact_name=artifact_name, artifact_tags=artifact_tags
            ).model_dump(),
            response_model=schemas.BlobArtifactUploadSignedURLManyResponse,
        )

    async def upload_signed_url_blob_artifact(
        self,
        filename: str,
        as_zip: bool,  # Defaults to True if artifact_path is a directory
        *,
        project_id: str,
        artifact_name: str,
        artifact_tags: list[str] | None = None,
    ) -> schemas.BlobArtifactUploadSignedURLResponse:
        """Get a signed URL for uploading an artifact."""
        return await self._client.make_request(
            url=f"project/{project_id}/artifact/upload_signed_url",
            method="post",
            json_data=schemas.UploadBlobArtifactBody(
                filename=filename, artifact_name=artifact_name, artifact_tags=artifact_tags, is_zipped_directory=as_zip
            ).model_dump(),
            response_model=schemas.BlobArtifactUploadSignedURLResponse,
        )

    """
    Source code API methods
    """

    async def upload_source_code(
        self, artifact_id: str, code_description: str | None = None, *, project_id: str
    ) -> schemas.Response[schemas.UploadedSourceCode]:
        """Upload source code."""
        params: ParamsType = {"blob_artifact_id": artifact_id}
        if code_description is not None:
            params["description"] = code_description
        return await self._client.make_request(
            url=f"project/{project_id}/source_code",
            method="post",
            response_model=schemas.Response[schemas.UploadedSourceCode],
            params=params,
        )

    """Admin API methods"""

    async def _rebuild_outdated_environments(self) -> schemas.ResponseOK:
        """Rebuild all outdated environments."""
        return await self._client.make_request(
            url="admin/rebuild_outdated_environments", method="post", response_model=schemas.ResponseOK
        )


MountSpecRequestUnion = Annotated[
    Union[schemas.DownloadMountSpecRequest, schemas.UploadMountSpecRequest, schemas.VolumeMountSpecRequest],
    Field(..., title="Mount Spec", discriminator="mode"),
]


def _mount_spec_to_request(mount_spec: schemas.MountSpecUnion) -> MountSpecRequestUnion:
    if isinstance(mount_spec, schemas.DownloadMountSpec):
        return schemas.DownloadMountSpecRequest(
            mode=mount_spec.mode,
            path=mount_spec.path,
            name=mount_spec.selector.name,
            tag=mount_spec.selector.tag or "latest",
            project=mount_spec.selector.project,
        )
    elif isinstance(mount_spec, schemas.UploadMountSpec):
        return schemas.UploadMountSpecRequest(
            mode=mount_spec.mode, path=mount_spec.path, name=mount_spec.target.name, tags=mount_spec.target.tags
        )
    elif isinstance(mount_spec, schemas.VolumeMountSpec):
        return schemas.VolumeMountSpecRequest(mode=mount_spec.mode, path=mount_spec.path, name=mount_spec.name)
    raise SlingshotException(f"Unknown mount mode: {mount_spec.mode}")


@contextlib.asynccontextmanager
async def _maybe_make_http_session(session: aiohttp.ClientSession | None) -> AsyncIterator[aiohttp.ClientSession]:
    if session is None or session.closed:
        # TODO: Consider TCPConnector(limit, limit_per_host) to reduce parallelism during artiact no-zip download. Left
        #  as a todo because making this change would have a wide blast radius and could affect unexpected concurrent
        #  requests, e.g. on predictions. The default TCPConnector has parallelism of 100. For artifact downloads though
        #  we'd ideally use at most 10.
        async with aiohttp.ClientSession() as session:
            yield session
    else:
        yield session


# See https://stackoverflow.com/a/61478547/14338504 for more context on how this works and what problem it solves.
async def gather_with_concurrency(n: int, *coros: Coroutine[Any, Any, Any]) -> list[Any]:
    semaphore = asyncio.Semaphore(n)

    async def sem_coro(coro: Coroutine[Any, Any, Any]) -> Any:
        async with semaphore:
            return await coro

    return await asyncio.gather(*(sem_coro(c) for c in coros))
