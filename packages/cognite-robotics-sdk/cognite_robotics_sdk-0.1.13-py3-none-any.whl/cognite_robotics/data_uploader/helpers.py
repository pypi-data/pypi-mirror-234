# -*- coding: utf-8 -*-
"""Data uploader helpers."""
import asyncio
import glob
import json
import logging
import os
import re
import shutil
import time
import uuid
from collections import defaultdict
from typing import Any, Dict, List, MutableMapping, Optional, Union

import aiofiles
import aiofiles.os
import pydantic

from cognite_robotics.data_classes import JSONRPCRequest
from cognite_robotics.data_uploader.data_classes import (
    Datapoint,
    DatapointsUploadRequest,
    DataUploaderConfig,
    FileUploadRequest,
    UploadError,
    UploadRequestParseError,
)
from cognite_robotics.protos.messages import common_pb2, data_pb2
from cognite_robotics.utils.utils import to_thread

logger = logging.getLogger(__name__)


async def create_file_upload_request(
    file_path: str,
    mission_run_id: str,
    action_external_id: str,
    action_run_id: str,
    config: DataUploaderConfig,
    mission_id: Optional[str] = None,
    data_set_id: Optional[int] = None,
    file_metadata: Optional[Dict[str, Any]] = None,
    asset_ids: Optional[List[int]] = None,
    asset_external_ids: Optional[List[str]] = None,
    data_capture_time: Optional[int] = None,
    data_postprocessing_input: Optional[JSONRPCRequest] = None,
    extra_metadata: Optional[Dict[str, str]] = None,
) -> None:
    """Create a file upload request.

    This is a helper function to create a file upload request. It copies the file to the upload data path and create a JSON metadata file.

    Args:
        file_path (str): Path to the file you wish to upload. The filename will be used as the external ID for the file in CDF, so make
                sure it is unique (e.g., by adding a timestamp to the filename, data type). Preferably use an absolute path.
        mission_run_id (str): ID for the specific run of the mission with `mission_id`. A typical example is: `mission_id`_`timestamp`.
        action_run_id (str): ID for the specific execution of an action. For example, `infrared_image_capture_1234567910`.
        mission_id (Optional[str]): External ID of the mission that is executed. Defaults to None.
        action_external_id (Optional[str]): External ID of the action that the data is a result of (e.g., data capture) that is executed.
                Defaults to None.
        config (DataUploaderConfig): DataUploaderConfig object, containing the upload data path. Needs to be the same as the one
                used in the DataUploader.
        data_set_id (Optional[int], optional): ID of the CDF data set to which the data belongs to. Defaults to None.
        file_metadata (Optional[Dict[str, Any]], optional): Metadata added to the uploaded file in CDF. Defaults to None.
        asset_ids (Optional[List[int]], optional): List of asset ids. Defaults to None.
        asset_external_ids (Optional[List[str]], optional): List of asset external ids. Defaults to None.
        data_capture_time (Optional[int], optional): Data capture time. Elapsed time in milliseconds since January 1, 1970, 00:00:00 UTC.
                Defaults to None.
        data_postprocessing_input (Optional[JSONRPCRequest], optional): Instructions on how to postprocess the data after upload to CDF.
                Defaults to None.

    Raises:
        FileNotFoundError: The file path does not exist.
        IOError: You can only create upload requests per one file at a time.
        exc_copy: Error copying the file to the upload data path.
        exc_create_json: Error creating the JSON metadata file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File path does not exist: `{file_path}`.")
    if not os.path.isfile(file_path):
        raise IOError(f"File path is not a file: `{file_path}`.")

    if data_capture_time is None:
        data_capture_time = int(time.time() * 1000)

    file_root_name, file_extension = os.path.splitext(os.path.basename(file_path))
    if file_extension.lower() == ".jpeg":
        os.rename(file_path, file_path.replace(".jpeg", ".jpg"))
        file_extension = ".jpg"

    upload_data_path = config.upload_data_path
    if not os.path.exists(upload_data_path):
        os.makedirs(upload_data_path, exist_ok=True)

    upload_file_path = os.path.join(upload_data_path, file_root_name + file_extension)

    # add file metadata, used for data postprocessing and contextualization
    if file_metadata is None:
        file_metadata = {}
    updates = {
        "mission_external_id": mission_id,
        "mission_run_id": mission_run_id,
        "action_run_id": action_run_id,
        "action_external_id": action_external_id,
        "asset_id": asset_ids[0] if asset_ids is not None and len(asset_ids) > 0 else None,
        "asset_external_id": asset_external_ids[0] if asset_external_ids is not None and len(asset_external_ids) > 0 else None,
    }

    for key, value in updates.items():
        if value is not None:
            file_metadata[key] = value

    if extra_metadata is not None:
        for key, value in extra_metadata.items():
            file_metadata[key] = value

    upload_request = FileUploadRequest(
        external_id=file_root_name,
        file_path=os.path.abspath(upload_file_path),
        mission_run_id=mission_run_id,
        mission_id=mission_id,
        action_run_id=action_run_id,
        action_external_id=action_external_id,
        timestamp_ms=data_capture_time,
        data_set_id=data_set_id,
        data_postprocessing_input=data_postprocessing_input,
        asset_ids=asset_ids,
        asset_external_ids=asset_external_ids,
        file_metadata=file_metadata,
    )

    try:
        await asyncio.shield(aiofiles.os.rename(file_path, upload_file_path))
    except Exception as exc_copy:
        message = "Failed to copy file to upload data path."
        logger.error(message)
        try:
            upload_request.error = UploadError(message=message, exception=str(exc_copy))
            await move_files([upload_file_path], config.error_data_path)
        except Exception as exc:
            logger.error(f"Failed to move file to error data path. {exc}")
        else:
            await remove_files([upload_file_path])
        raise exc_copy

    try:
        await _create_upload_request_json(
            upload_request=upload_request, raw_data_path=config.raw_data_path, upload_data_path=upload_data_path
        )
    except Exception as exc_create_json:
        message = "Failed to create upload request JSON."
        logger.error(message)
        try:
            upload_request.error = UploadError(message=message, exception=str(exc_create_json))
            await move_files([upload_file_path], config.error_data_path)
        except Exception as e:
            logger.error(f"{message}: {e}")
        finally:
            # clean up of both json and associated data files (if exists)
            await remove_files(glob.glob(os.path.join(config.upload_data_path, f"{file_root_name}.*")))
        raise exc_create_json


async def create_datapoints_upload_request(
    timestamps: List[int],
    measurements: List[Union[str, float]],
    timeseries_external_id: str,
    mission_id: str,
    mission_run_id: str,
    action_external_id: str,
    action_run_id: str,
    config: DataUploaderConfig,
    data_set_id: Optional[int] = None,
    asset_ids: Optional[List[int]] = None,
    data_postprocessing_input: Optional[JSONRPCRequest] = None,
) -> None:
    """Upload data points to a time series to Cognite Data Fusion.

    Args:
        timestamps (List[int]): List of measurement timestamps in milliseconds.
                Elapsed time in milliseconds since January 1, 1970, 00:00:00 UTC
        measurements (List[Union[str, float]]): List of measurement values. Must be either a float or a string.
        timeseries_external_id (str): External ID of the time series in CDF.
        mission_id (str): External ID of the mission that is executed.
        mission_run_id (str): ID for the specific run of the mission with `mission_id`.
        action_external_id (str): External ID of the action that the data is a result of (e.g., data capture) that is executed.
        action_run_id (str): ID for the action execution.
        config (DataUploaderConfig): DataUploaderConfig object, containing the upload data path. Needs to be the same as the one
                used in the DataUploader.
        data_set_id (Optional[int], optional): ID of the data set. Defaults to None.
        cdf_metadata (Optional[Dict[str, Any]], optional): Metadata added to the timeseries in CDF. Defaults to None.
        asset_ids (Optional[List[int]], optional): List of asset ids. Defaults to None.
        data_postprocessing_input (Optional[JSONRPCRequest], optional): Instructions on how to postprocess the
                data after upload to CDF. Defaults to None.

    Raises:
        ValueError: Number of measurements needs to be equal to number of timestamps.
    """
    if len(measurements) == 0:
        logger.warn("No measurements to upload.")
        return
    if len(timestamps) == 1:
        timestamps = [timestamps[0]] * len(measurements)
    elif len(measurements) != len(timestamps):
        raise ValueError(f"Number of measurements ({len(measurements)}) and timestamps ({len(timestamps)}) must be equal.")

    datapoints = [Datapoint(timestamp=ts, value=value) for ts, value in zip(timestamps, measurements)]

    upload_request = DatapointsUploadRequest(
        mission_id=mission_id,
        mission_run_id=mission_run_id,
        action_run_id=action_run_id,
        timestamp_ms=timestamps[0],
        data_set_id=data_set_id,
        data_postprocessing_input=data_postprocessing_input,
        asset_ids=asset_ids,
        action_external_id=action_external_id,
        datapoints=datapoints,
        timeseries_external_id=timeseries_external_id,
    )

    try:
        await _create_upload_request_json(
            upload_request=upload_request, raw_data_path=config.raw_data_path, upload_data_path=config.upload_data_path
        )
    except Exception as exc_create_json:
        logger.error(f"Failed to create upload request JSON. {exc_create_json}")


async def _create_upload_request_json(
    upload_request: Union[FileUploadRequest, DatapointsUploadRequest], raw_data_path: str, upload_data_path: str
) -> None:
    """Create a JSON file containing the upload request data."""

    async def _create() -> None:
        if isinstance(upload_request, DatapointsUploadRequest):
            filename_json = f"datapoint_upload_{uuid.uuid4()}.json"
        else:
            filename_json = f"{os.path.splitext(os.path.basename(upload_request.file_path))[0]}.json"
        file_path_raw = os.path.join(raw_data_path, filename_json)

        try:
            async with aiofiles.open(file_path_raw, mode="w") as f:
                await f.write(json.dumps(upload_request.dict(), indent=4))
        except Exception as e:
            raise e

        os.rename(file_path_raw, os.path.join(upload_data_path, filename_json))

    await asyncio.shield(_create())


async def get_upload_request_from_json(upload_request_json_filename: str) -> Union[FileUploadRequest, DatapointsUploadRequest]:
    """Create UploadInfo from JSON file."""
    async with aiofiles.open(upload_request_json_filename) as json_file:
        contents = await json_file.read()
    data = json.loads(contents)

    if "file_path" in data:
        return pydantic.TypeAdapter(FileUploadRequest).validate_python(data)
    elif "datapoints" in data:
        return pydantic.TypeAdapter(DatapointsUploadRequest).validate_python(data)
    else:
        raise UploadRequestParseError(data)


def create_data_upload_event_message(upload_request: Union[FileUploadRequest, DatapointsUploadRequest]) -> data_pb2.DataUploadEvent:
    """Create data upload event message."""
    data_upload_message = data_pb2.DataUploadEvent(
        mission_report_id=upload_request.mission_run_id,
        action_report_id=upload_request.action_run_id,
        data_capture_time=upload_request.timestamp_ms if upload_request.timestamp_ms is not None else int(time.time() * 1000),
        data_postprocessing_input=json.dumps(upload_request.data_postprocessing_input.model_dump())
        if upload_request.data_postprocessing_input is not None
        else "",
    )
    if upload_request.action_external_id is not None:
        data_upload_message.action_external_id = upload_request.action_external_id
    if upload_request.asset_ids is not None:
        data_upload_message.asset_ids.extend(upload_request.asset_ids)
    return data_upload_message


def create_data_upload_error_message(
    error: Exception,
    upload_request: Union[FileUploadRequest, DatapointsUploadRequest],
) -> data_pb2.DataUploadEvent:
    """Create data upload error message."""
    data_upload_message = create_data_upload_event_message(upload_request=upload_request)
    error_message = common_pb2.ErrorMessage(message=str(error))
    data_upload_message.error_message.CopyFrom(error_message)
    return data_upload_message


def _create_cdf_filename(
    mission_run_id: str, action_run_id: str, timestamp: int, filename_prefix: Optional[str] = None, data_type: Optional[str] = None
) -> str:
    """Create a name for the file to be uploaded."""
    if filename_prefix is not None:
        name = "__".join([filename_prefix, mission_run_id, action_run_id])
    else:
        name = "__".join([mission_run_id, action_run_id])

    if data_type is not None:
        name = "__".join([name, data_type])

    # to avoid duplicate file names, append the data capture time to the end of the file name (if not already present)
    if re.search(r"\d+$", name) is None:
        name = f"{name}__{timestamp}"

    name = name.replace(".", "__")

    return name


async def remove_files(files: List[str]) -> None:
    """Remove files."""

    def _remove_files() -> None:
        for file in files:
            if not os.path.exists(file):
                logger.debug(f"File `{file}` does not exist. Skipping removal.")
                continue
            try:
                os.remove(file)
                logger.debug(f"Removed {file}.")
            except OSError as e:
                logger.error(f"Failed to remove `{file}`: {e!s}")

    await asyncio.shield(to_thread(_remove_files))


async def move_files(
    files: List[str],
    to_folder: str,
) -> None:
    """Move files."""

    def _move_files() -> None:
        for file in files:
            if not os.path.exists(file):
                logger.debug(f"File `{file}` does not exist. Skipping moving.")
                continue
            try:
                os.rename(file, os.path.join(to_folder, os.path.basename(file)))
                logger.debug(f"Moved {file} to {to_folder}.")
            except Exception as e:
                logger.error(f"Failed to move `{file}`: {e!s}")

    await asyncio.shield(to_thread(_move_files))


async def cleanup_upload_data_folder(upload_data_path: str) -> None:
    """Clean up the upload data folder.

    List all files in the upload data folder, check if there is a JSON file (e.g., the upload request instructions) for each file.
    If no associated JSON file is found, remove all other files.
    """
    files = [f for f in glob.glob(os.path.join(upload_data_path, "*")) if not f.startswith(".")]

    grouped_files = defaultdict(list)
    for file in files:
        filename, _ = os.path.splitext(file)
        grouped_files[filename].append(file)

    for filename, files in grouped_files.items():
        has_json = any(f for f in files if f.endswith(".json"))
        if not has_json:
            logger.info(f"Removing files without JSON: {files}")
            await remove_files(files)


async def cleanup_folder(folder: str) -> None:
    """Clean up a folder.

    List all files in the folder, remove all files and subdirectories
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                await asyncio.shield(to_thread(shutil.rmtree, file_path))
        except Exception as e:
            logger.error(f"Failed to delete {file_path}: {e}")


def flatten_dict(d: Union[Dict[Any, Any], MutableMapping[Any, Any]], parent_key: str = "", sep: str = "_") -> Dict[Any, Any]:
    """Flatten dictionary.

    Args:
        d (Union[Dict[Any, Any], MutableMapping[Any, Any]]): dictionary to be flattened
        parent_key (str, optional): parent key. Defaults to "".
        sep (str, optional): seperator for the keys when flattening. Defaults to "_".

    Returns:
        Dict[Any, Any]: Flattened dictionary
    """
    items: List[Any] = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
