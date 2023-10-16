"""Contains all the services."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto

from link.domain.custom_types import Identifier
from link.domain.link import process as process_domain_service
from link.domain.link import start_delete, start_pull
from link.domain.state import InvalidOperation, Operations, Update, states

from .gateway import LinkGateway


class Request:
    """Base class for all request models."""


class Response:
    """Base class for all response models."""


@dataclass(frozen=True)
class PullRequest(Request):
    """Request model for the pull use-case."""

    requested: frozenset[Identifier]


@dataclass(frozen=True)
class PullResponse(Response):
    """Response model for the pull use-case."""

    requested: frozenset[Identifier]
    errors: frozenset[InvalidOperation]


def pull(
    request: PullRequest,
    *,
    process_to_completion_service: Callable[[ProcessToCompletionRequest], ProcessToCompletionResponse],
    start_pull_process_service: Callable[[StartPullProcessRequest], OperationResponse],
    output_port: Callable[[PullResponse], None],
) -> None:
    """Pull entities across the link."""
    process_to_completion_service(ProcessToCompletionRequest(request.requested))
    response = start_pull_process_service(StartPullProcessRequest(request.requested))
    errors = (error for error in response.errors if error.state is states.Deprecated)
    process_to_completion_service(ProcessToCompletionRequest(request.requested))
    output_port(PullResponse(request.requested, errors=frozenset(errors)))


@dataclass(frozen=True)
class DeleteRequest(Request):
    """Request model for the delete use-case."""

    requested: frozenset[Identifier]


@dataclass(frozen=True)
class DeleteResponse(Response):
    """Response model for the delete use-case."""

    requested: frozenset[Identifier]


def delete(
    request: DeleteRequest,
    *,
    process_to_completion_service: Callable[[ProcessToCompletionRequest], ProcessToCompletionResponse],
    start_delete_process_service: Callable[[StartDeleteProcessRequest], OperationResponse],
    output_port: Callable[[DeleteResponse], None],
) -> None:
    """Delete pulled entities."""
    process_to_completion_service(ProcessToCompletionRequest(request.requested))
    start_delete_process_service(StartDeleteProcessRequest(request.requested))
    process_to_completion_service(ProcessToCompletionRequest(request.requested))
    output_port(DeleteResponse(request.requested))


@dataclass(frozen=True)
class ProcessToCompletionRequest(Request):
    """Request model for the process to completion use-case."""

    requested: frozenset[Identifier]


@dataclass(frozen=True)
class ProcessToCompletionResponse(Response):
    """Response model for the process to completion use-case."""

    requested: frozenset[Identifier]


def process_to_completion(
    request: ProcessToCompletionRequest,
    *,
    process_service: Callable[[ProcessRequest], OperationResponse],
    output_port: Callable[[ProcessToCompletionResponse], None],
) -> None:
    """Process entities until their processes are complete."""
    while process_service(ProcessRequest(request.requested)).updates:
        pass
    output_port(ProcessToCompletionResponse(request.requested))


@dataclass(frozen=True)
class OperationResponse(Response):
    """Response model for all use-cases that operate on entities."""

    operation: Operations
    requested: frozenset[Identifier]
    updates: frozenset[Update]
    errors: frozenset[InvalidOperation]


@dataclass(frozen=True)
class StartPullProcessRequest(Request):
    """Request model for the start-pull-process service."""

    requested: frozenset[Identifier]


def start_pull_process(
    request: StartPullProcessRequest,
    *,
    link_gateway: LinkGateway,
    output_port: Callable[[OperationResponse], None],
) -> None:
    """Start the pull process for the requested entities."""
    result = start_pull(link_gateway.create_link(), requested=request.requested)
    link_gateway.apply(result.updates)
    output_port(OperationResponse(result.operation, request.requested, result.updates, result.errors))


@dataclass(frozen=True)
class StartDeleteProcessRequest(Request):
    """Request model for the start-delete-process service."""

    requested: frozenset[Identifier]


def start_delete_process(
    request: StartDeleteProcessRequest,
    *,
    link_gateway: LinkGateway,
    output_port: Callable[[OperationResponse], None],
) -> None:
    """Start the delete process for the requested entities."""
    result = start_delete(link_gateway.create_link(), requested=request.requested)
    link_gateway.apply(result.updates)
    output_port(OperationResponse(result.operation, request.requested, result.updates, result.errors))


@dataclass(frozen=True)
class ProcessRequest(Request):
    """Request model for the process use-case."""

    requested: frozenset[Identifier]


def process(
    request: ProcessRequest, *, link_gateway: LinkGateway, output_port: Callable[[OperationResponse], None]
) -> None:
    """Process entities."""
    result = process_domain_service(link_gateway.create_link(), requested=request.requested)
    link_gateway.apply(result.updates)
    output_port(OperationResponse(result.operation, request.requested, result.updates, result.errors))


@dataclass(frozen=True)
class ListIdleEntitiesRequest(Request):
    """Request model for the use-case that lists idle entities."""


@dataclass(frozen=True)
class ListIdleEntitiesResponse(Response):
    """Response model for the use-case that lists idle entities."""

    identifiers: frozenset[Identifier]


def list_idle_entities(
    request: ListIdleEntitiesRequest,
    *,
    link_gateway: LinkGateway,
    output_port: Callable[[ListIdleEntitiesResponse], None],
) -> None:
    """List all idle entities."""
    output_port(
        ListIdleEntitiesResponse(
            frozenset(entity.identifier for entity in link_gateway.create_link() if entity.state is states.Idle)
        )
    )


class Services(Enum):
    """Names for all available services."""

    PULL = auto()
    DELETE = auto()
    PROCESS = auto()
    LIST_IDLE_ENTITIES = auto()
