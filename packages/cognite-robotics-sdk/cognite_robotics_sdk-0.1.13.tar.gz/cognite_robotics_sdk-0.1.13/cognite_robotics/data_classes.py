# -*- coding: utf-8 -*-
"""Data classes."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class JSONRPCRequest(BaseModel):
    """JSON RPC request."""

    method: str
    parameters: Dict[str, Any]
    id: Optional[int] = None


class CogniteRobotActionMetadata(BaseModel):
    """Cognite robot action metadata dataclass."""

    mission_run_id: str
    action_run_id: str
    action_external_id: str
    asset_ids: Optional[List[int]] = None
    asset_external_ids: Optional[List[str]] = None
    upload_instructions: Optional[Dict[str, JSONRPCRequest]] = None
    data_postprocessing_input: Optional[Dict[str, JSONRPCRequest]] = None
