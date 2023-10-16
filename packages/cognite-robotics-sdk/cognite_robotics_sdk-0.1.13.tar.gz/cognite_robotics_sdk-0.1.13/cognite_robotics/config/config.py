# -*- coding: utf-8 -*-
"""Cognite Robotics client configuration."""
from dataclasses import dataclass
from typing import Callable

from cognite_robotics.utils.env_utils import get_env
from cognite_robotics.utils.token import get_token_generator


@dataclass
class CogniteRoboticsClientConfig:
    """Cognite Robotics client configuration."""

    project: str
    target: str
    cluster: str
    oidc_token_callable: Callable[[], str]


@dataclass
class LocalClientConfig:
    """Client configuration for local development."""

    ip: str
    port: int


def load_config_from_env() -> CogniteRoboticsClientConfig:
    """Load client configuration from environment variables."""
    cluster = get_env("COGNITE_CLUSTER")
    scopes = [f"https://{cluster}.cognitedata.com/.default"]
    client_id = get_env("COGNITE_CLIENT_ID")
    client_secret = get_env("COGNITE_CLIENT_SECRET")
    tenant_id = get_env("COGNITE_TENANT_ID")
    project = get_env("COGNITE_PROJECT")
    target = f"{cluster}.cognitedata.com:443"
    oidc_token_callable = get_token_generator(tenant_id, client_id, client_secret, scopes)
    return CogniteRoboticsClientConfig(project, target, cluster, oidc_token_callable)
