# -*- coding: utf-8 -*-
"""Data classes for data uploader."""
import os
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from cognite_robotics.data_classes import JSONRPCRequest


class DataUploaderConfig:
    """Data uploader configuration dataclass."""

    _base_data_path: str
    _raw_data_path: str
    _upload_data_path: str
    _error_data_path: str
    loop_time_step_s: float = 1.0
    retry_upload_interval_s: float = 5.0

    def __init__(self, base_path: str) -> None:
        """Initialize the data uploader configuration."""
        self._base_data_path = os.path.abspath(base_path)
        self._raw_data_path = os.path.join(self._base_data_path, "raw")
        os.makedirs(self._raw_data_path, exist_ok=True)
        self._error_data_path = os.path.join(self._base_data_path, "error")
        os.makedirs(self._error_data_path, exist_ok=True)
        self._upload_data_path = os.path.join(self._base_data_path, "upload")
        os.makedirs(self._upload_data_path, exist_ok=True)

    @property
    def base_data_path(self) -> str:
        """Return the base data path."""
        return self._base_data_path

    @property
    def raw_data_path(self) -> str:
        """Return the raw data path."""
        return self._raw_data_path

    @property
    def upload_data_path(self) -> str:
        """Return the upload data path."""
        return self._upload_data_path

    @property
    def error_data_path(self) -> str:
        """Return the error data path."""
        return self._error_data_path


class UploadError(BaseModel):
    """Upload error dataclass."""

    message: str
    exception: Optional[str] = None


class BaseUploadRequest(BaseModel):
    """Upload request base dataclass."""

    mission_run_id: str
    action_external_id: str
    action_run_id: str
    mission_id: Optional[str] = None
    timestamp_ms: Optional[int] = None
    data_set_id: Optional[int] = None
    data_postprocessing_input: Optional[JSONRPCRequest] = None
    asset_ids: Optional[List[int]] = None
    asset_external_ids: Optional[List[str]] = None
    error: Optional[UploadError] = None


class FileUploadRequest(BaseUploadRequest):
    """File upload request dataclass."""

    file_path: str
    external_id: str
    file_metadata: Optional[Dict[str, Any]] = None


class Datapoint(BaseModel):
    """Data point dataclass, mirrors the Cognite datapoint."""

    timestamp: int
    value: Union[float, str]


class DatapointsUploadRequest(BaseUploadRequest):
    """Data point upload request dataclass."""

    datapoints: List[Datapoint]
    timeseries_external_id: str


class UploadRequestParseError(Exception):
    """Upload request parse error."""

    def __init__(self, json_data: Dict[str, Any]) -> None:
        """Initialize the upload request parse error."""
        super().__init__(f"Error parsing upload request: {json_data}")
