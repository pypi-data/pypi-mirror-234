# -*- coding: utf-8 -*-
"""Bearer token auth."""
from typing import Callable

import grpc


class BearerTokenAuth(grpc.AuthMetadataPlugin):
    """Inject an authorization header with a bearer token in GRPC requests."""

    def __init__(self, project_name: str, token_supplier: Callable[[], str]):
        """Initialize BearerTokenAuth."""
        self._project_metadata = ("cdf-project-name", project_name)
        self._token_supplier = token_supplier

    def __call__(
        self,
        _context: grpc.AuthMetadataContext,
        callback: grpc.AuthMetadataPluginCallback,
    ) -> None:
        """Call bearer token auth."""
        callback(
            (
                ("authorization", "Bearer " + self._token_supplier()),
                self._project_metadata,
            ),
            None,
        )
