# -*- coding: utf-8 -*-
"""Channel."""
from typing import Callable

import certifi
import grpc

from cognite_robotics.grpc.helpers.bearer_token_auth import BearerTokenAuth


async def get_insecure_channel(ip: str, port: int) -> grpc.aio.Channel:
    """Get insecure channel."""
    return grpc.aio.insecure_channel(f"{ip}:{port}")


async def get_secure_channel(project: str, oidc_token_callable: Callable[[], str], target: str) -> grpc.aio.Channel:
    """Get secure channel."""
    root_certs = certifi.contents().encode()
    auth_plugin = BearerTokenAuth(project, oidc_token_callable)
    credentials = grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(root_certificates=root_certs),
        grpc.metadata_call_credentials(auth_plugin),
    )
    return grpc.aio.secure_channel(target, credentials)
