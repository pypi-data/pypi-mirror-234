# -*- coding: utf-8 -*-
"""Utils tests."""
import asyncio
import contextvars
import functools
import json
import logging
import typing
from typing import Any, AsyncGenerator, List, Optional, TypeVar

import grpc
from cognite.client import CogniteClient, global_config
from cognite.client.config import ClientConfig
from cognite.client.credentials import OAuthClientCredentials

from cognite_robotics.utils.env_utils import get_env

logger = logging.getLogger(__name__)

T = TypeVar("T")

global_config.disable_gzip = True
global_config.status_forcelist = {429}  # the data uploader will handle retry on connection related issues


async def yield_from_queue(queue: "asyncio.Queue[T]") -> AsyncGenerator[T, None]:
    """Yield items from a queue.

    Args:
        queue (asyncio.Queue[T]): queue to yield items from
    Returns:
        AsyncGenerator[T, None]: generator of items from the queue
    """
    while True:
        item = await queue.get()
        yield item


async def handle_grpc_error(
    e: grpc.RpcError,
    invoker: Optional[str] = None,
    error_codes_to_handle_silently: List[grpc.StatusCode] = [
        grpc.StatusCode.UNAVAILABLE,
        grpc.StatusCode.INTERNAL,
        grpc.StatusCode.UNAUTHENTICATED,
    ],
) -> None:
    """Handle gPRC errors.

    Args:
        e (grpc.RpcError): RpcError to handle
        invoker (Optional[str], optional): Invoker of the gRPC call. Defaults to None.
        error_codes_to_handle_silently (List[grpc.StatusCode], optional): List of error codes to handle silently.

    Raises:
        e: if error is not in error_codes_to_handle_silently
    """
    if e.code() in error_codes_to_handle_silently:
        # grpc channel is not ready, wait a little bit and try to setup a new stream
        logger.warning(
            f"gRPC error (code: `{e.code()}`, details: `{e.details()}`, invoker: `{invoker if invoker is not None else 'unknown'}`)"
        )
        await asyncio.sleep(1.0)
    else:
        logger.exception(f"gRPC error invoked by `{invoker if invoker is not None else 'unknown'}`", exc_info=e)
        raise e


def create_cognite_client(client_name: str) -> CogniteClient:
    """Use env variables to set up CogniteClient.

    Args:
        client_name (str): client name
    Returns:
        CogniteClient: Cognite CDF client
    """
    cluster = get_env("COGNITE_CLUSTER")
    base_url = f"https://{cluster}.cognitedata.com"
    project = get_env("COGNITE_PROJECT")
    client_secret = get_env("COGNITE_CLIENT_SECRET")
    tenant_id = get_env("COGNITE_TENANT_ID")
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    client_id = get_env("COGNITE_CLIENT_ID")
    token_scopes = [f"{base_url}/.default"]

    creds = OAuthClientCredentials(token_url=token_url, client_id=client_id, client_secret=client_secret, scopes=token_scopes)
    cnf = ClientConfig(client_name=client_name, base_url=base_url, project=str(project), credentials=creds)
    return CogniteClient(cnf)


def get_robot_data_set_id(
    cognite_client: CogniteClient,
) -> Optional[int]:
    """Get the robot's data set id.

    The data set id is the data set of the only robot in CDF the service has access to.

    Returns:
        Optional[Any]: robot data set id (if available)
    """
    cognite_client.config.project
    response = cognite_client.get(f"/api/v1/projects/{cognite_client.config.project}/robotics/robots")
    robots = json.loads(response.content)["items"]
    if len(robots) != 1:
        logger.error("Found none or more than one robot for the robot's credentials.")
        return None
    return int(robots[0].get("dataSetId"))


@typing.no_type_check
async def to_thread(func, /, *args, **kwargs) -> Any:
    """Asyncio thread implementation for Python 3.8."""
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)
