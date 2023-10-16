from __future__ import annotations

import abc
from typing import Any, ClassVar, Generic, Literal, Optional, Type, TypeVar

from pydantic import BaseModel

from slingshot.sdk.errors import SlingshotClientGraphQLException

T = TypeVar("T")

ResponseType = TypeVar("ResponseType", bound=BaseModel)


class GraphQLError(BaseModel):
    message: str
    locations: Optional[list[dict[str, int]]] = None
    path: Optional[list[str]] = None
    extensions: Optional[dict[str, str]] = None


class GraphQLResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    errors: Optional[list[GraphQLError]] = None

    def as_exception(self) -> SlingshotClientGraphQLException:
        if not self.errors:
            raise ValueError("Cannot create exception from GraphQLResponse with no errors")
        return SlingshotClientGraphQLException.from_graphql_errors(self.errors)

    def get_data_or_raise(self) -> T:
        if self.errors:
            raise self.as_exception()
        if self.data is None:
            raise ValueError("Cannot get data from GraphQL (unexpected)")
        return self.data


class GraphQLSubscriptionResponse(BaseModel, Generic[T]):
    type: Literal['data']
    id: str
    payload: GraphQLResponse[T]


class BaseGraphQLEntity(BaseModel, abc.ABC):
    _fragment: ClassVar[str]  # Abstract
    _depends_on: ClassVar[list[Type[BaseGraphQLEntity]]]  # Abstract

    def _get_dependencies_ext(self, visited: set[Type[BaseGraphQLEntity]]) -> set[Type[BaseGraphQLEntity]]:
        # Recursively get all dependencies
        dependencies = set()

        for dependency in self._depends_on:
            dependencies.add(dependency)
            # This is hacky. This is bc we can't declare _fragment or _depends_on as abstract class properties
            if dependency not in visited:
                visited.add(dependency)
                dependencies = dependencies.union(dependency._get_dependencies_ext(dependency, visited))  # type: ignore
        return dependencies.union(visited)

    def _get_dependencies(self) -> list[Type[BaseGraphQLEntity]]:
        return list(self._get_dependencies_ext(set()))

    def get_fragment_string(self) -> str:
        """Get the GraphQL fragment string for this entity, including all dependencies"""
        dependencies = set(self._get_dependencies())
        fragments: list[str] = [dependency._fragment for dependency in dependencies]
        fragments.append(self._fragment)
        return "\n".join(fragments)


class BaseGraphQLQuery(BaseGraphQLEntity, Generic[ResponseType]):
    query: str
    variables: Optional[dict[str, Any]] = None
    response_model: Type[ResponseType]
    _query: ClassVar[str]  # Abstract

    @property
    def _fragment(self) -> str:  # type: ignore[override]
        return self._query

    def get_query(self, **kwargs: Any) -> str:
        return self.get_fragment_string()

    def __init__(self, variables: Optional[dict[str, Any]], response_model: Type[ResponseType]):
        # Mypy doesn't like this though we inherit from a BaseModel, which should accept named params
        # If we change it though, things break horribly.
        super().__init__(query=self.get_query(), variables=variables, response_model=response_model)  # type: ignore
