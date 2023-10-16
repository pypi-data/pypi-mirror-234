# -*- coding: utf-8 -*-
"""Data uploader."""
import asyncio
import glob
import json
import logging
import mimetypes
import os
import socket
import time
import unittest
import unittest.mock
from typing import List, Optional, Union

import aiofiles
import aiofiles.os
import grpc
from cognite.client import CogniteClient
from cognite.client.exceptions import CogniteConnectionError

from cognite_robotics.data_uploader.data_classes import DatapointsUploadRequest, DataUploaderConfig, FileUploadRequest, UploadError
from cognite_robotics.data_uploader.helpers import (
    cleanup_upload_data_folder,
    create_data_upload_error_message,
    create_data_upload_event_message,
    flatten_dict,
    get_upload_request_from_json,
    move_files,
    remove_files,
)
from cognite_robotics.grpc.clients.robot_interface_client import CogniteRobotInterfaceClient
from cognite_robotics.protos.messages import data_pb2
from cognite_robotics.utils.utils import handle_grpc_error, to_thread

logger = logging.getLogger(__name__)
mimetypes.add_type("application/octet-stream", ".raw")


async def data_uploader(
    stop_task_trigger: asyncio.Event,
    data_upload_event_queue: "asyncio.Queue[data_pb2.DataUploadEvent]",
    cognite_client: CogniteClient,
    data_set_id: int,
    config: DataUploaderConfig,
    loop_time_step_s: float = 1.0,
) -> None:
    """Upload data to CDF and notify Robotics Services."""
    data_error_path = config.error_data_path
    if not os.path.exists(data_error_path):
        os.makedirs(data_error_path, exist_ok=True)
    data_upload_path = config.upload_data_path
    if not os.path.exists(data_upload_path):
        logger.warning(f"Data upload path does not exist, creating: `{data_upload_path}`.")
        os.makedirs(data_upload_path, exist_ok=True)

    while not stop_task_trigger.is_set():
        logger.info("Starting data uploader.")
        try:
            logger.debug("Cleaning up upload data folder.")
            await cleanup_upload_data_folder(config.upload_data_path)

            while not stop_task_trigger.is_set():
                loop_start_time = time.perf_counter_ns()
                for json_file in glob.glob(os.path.join(config.upload_data_path, "*.json")):
                    if stop_task_trigger.is_set():
                        break

                    file_root_name, _ = os.path.splitext(os.path.basename(json_file))
                    all_files_same_name = glob.glob(os.path.join(config.upload_data_path, f"{file_root_name}.*"))

                    logger.info(f"Upload request, file root name: `{file_root_name}`.")
                    try:
                        upload_request = await get_upload_request_from_json(json_file)
                    except Exception as e:
                        logger.error(f"Error reading upload request file, skipping upload, files: `{file_root_name}`.", exc_info=e)
                        await move_files(all_files_same_name, data_error_path)
                        continue

                    logger.info(
                        f"Uploading data to CDF, mission run: `{upload_request.mission_run_id}`, action: `{upload_request.action_run_id}`."
                    )
                    try:
                        data_upload_message = None
                        if isinstance(upload_request, FileUploadRequest):
                            data_upload_message = await handle_file_upload_request(
                                cognite_client=cognite_client,
                                upload_request=upload_request,
                                data_set_id=data_set_id,
                            )
                        elif isinstance(upload_request, DatapointsUploadRequest):
                            data_upload_message = await handle_datapoint_upload_request(
                                cognite_client=cognite_client,
                                upload_request=upload_request,
                            )
                    except (ConnectionError, CogniteConnectionError, socket.gaierror):
                        logger.warning(
                            f"Failed to upload to CDF. Retrying upload in {config.retry_upload_interval_s} seconds.",
                        )
                        await asyncio.sleep(config.retry_upload_interval_s)
                    except Exception as error:
                        data_upload_message = await handle_failed_upload(
                            json_file_path=json_file,
                            all_files=all_files_same_name,
                            upload_request=upload_request,
                            error=error,
                            data_error_path=data_error_path,
                        )
                    else:
                        await remove_files(files=all_files_same_name)
                    finally:
                        if data_upload_message is not None:
                            await data_upload_event_queue.put(data_upload_message)

                loop_execution_time_s = float(time.perf_counter_ns() - loop_start_time) / 1000000000.0
                await asyncio.sleep(max(0.0, loop_time_step_s - loop_execution_time_s))
        except Exception as e:
            logger.error("Data uploader failed.", exc_info=e)
            # raise  # still raising to allow for a restart of the data uploader
        finally:
            logger.info("Data uploader stopped.")


async def data_upload_event_message_publisher(
    stop_task_trigger: asyncio.Event,
    robot_interface_client: CogniteRobotInterfaceClient,
    data_upload_event_queue: "asyncio.Queue[data_pb2.DataUploadEvent]",
) -> None:
    """Handle data upload event and response."""
    logger.info("Starting data upload event message handler.")
    while not stop_task_trigger.is_set():
        data_upload_event = await data_upload_event_queue.get()
        logger.info(
            f"Sending data upload event, mission_run_id: `{data_upload_event.mission_report_id}`,"
            f" action_run_id: `{data_upload_event.action_report_id}`."
        )
        try:
            await robot_interface_client.send_data_upload_event(data_upload_event)
        except grpc.RpcError as e:
            await handle_grpc_error(e, invoker="send_data_upload_event")
        except Exception as e:
            raise Exception("An unknown error occurred when sending data_upload_event, shutting down handler") from e


async def handle_file_upload_request(
    cognite_client: CogniteClient,
    data_set_id: int,
    upload_request: FileUploadRequest,
) -> Optional[data_pb2.DataUploadEvent]:
    """Upload file to CDF."""
    file_path = upload_request.file_path
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File `{file_path}` not found.")

    external_id = upload_request.external_id
    retrieved_files = await to_thread(cognite_client.files.retrieve, external_id=external_id)
    if retrieved_files is not None:
        if isinstance(retrieved_files, unittest.mock.MagicMock):
            logger.debug(f"Mocked response, external_id: `{external_id}`.")
        else:
            message = f"File already exists in CDF, retaining the existing file, external_id: `{external_id}`."
            logger.debug(message)
            # TODO: implement robot log client
            # await create_robot_log(
            #     message=message,
            #     severity=INFO,
            #     robot_status_queue=robot_status_queue,
            # )
            return None

    file_metadata = upload_request.file_metadata
    if file_metadata is not None:
        file_metadata = flatten_dict(file_metadata)
        file_metadata = {key: str(value) for key, value in file_metadata.items() if value not in (None, "", "None")}
    else:
        file_metadata = {}

    (mime_type, _) = mimetypes.guess_type(file_path)

    result = await asyncio.shield(
        to_thread(
            cognite_client.files.upload,
            file_path,
            name=os.path.basename(file_path),
            external_id=upload_request.external_id,
            metadata=file_metadata,
            data_set_id=data_set_id,
            mime_type=mime_type,  # type: ignore
        )
    )

    file_id = int(result.id)
    file_upload_message = data_pb2.FileUpload(file_id=file_id)
    data_upload_message: data_pb2.DataUploadEvent = create_data_upload_event_message(upload_request=upload_request)
    data_upload_message.file_upload.CopyFrom(file_upload_message)

    logger.debug(f"File upload successful, external_id: `{external_id}`.")
    # TODO: implement robot log client
    # await create_robot_log(
    #     message=f"File upload successful, file external_id: `{external_id}`.",
    #     severity=INFO,
    #     robot_status_queue=robot_status_queue,
    # )
    return data_upload_message


async def handle_datapoint_upload_request(
    cognite_client: CogniteClient,
    upload_request: DatapointsUploadRequest,
) -> data_pb2.DataUploadEvent:
    """Upload data to a timeseries."""
    timeseries_external_id = upload_request.timeseries_external_id

    def check_timeseries_exists() -> bool:
        return cognite_client.time_series.retrieve(external_id=timeseries_external_id) is None

    if not await to_thread(check_timeseries_exists):
        raise Exception(f"Timeseries does not exist, external_id: `{timeseries_external_id}`.")

    data_points = [datapoint.model_dump() for datapoint in upload_request.datapoints]
    await asyncio.shield(to_thread(cognite_client.time_series.data.insert, datapoints=data_points, external_id=timeseries_external_id))
    message = f"Datapoints upload successful, timeseries_external_id: `{timeseries_external_id}`."
    logger.info(message)
    # TODO: implement robot log client
    # await create_robot_log(
    #     message=message,
    #     severity=INFO,
    #     robot_status_queue=robot_status_queue,
    # )
    data_upload_message: data_pb2.DataUploadEvent = create_data_upload_event_message(upload_request)
    datapoint_upload_message = data_pb2.DataPointUpload(
        timeseries_external_id=timeseries_external_id,
        timestamp=upload_request.timestamp_ms if upload_request.timestamp_ms is not None else int(time.time() * 1000),
    )
    data_upload_message.data_point_upload.CopyFrom(datapoint_upload_message)
    return data_upload_message


async def handle_failed_upload(
    json_file_path: str,
    all_files: List[str],
    upload_request: Union[FileUploadRequest, DatapointsUploadRequest],
    error: Exception,
    data_error_path: str,
) -> data_pb2.DataUploadEvent:
    """Handle failed upload."""
    try:
        try:
            upload_request.mission_run_id
            upload_request.error = UploadError(message="Failed data upload", exception=str(error))
            async with aiofiles.open(json_file_path, mode="w") as f:
                await f.write(json.dumps(upload_request.model_dump()))

            if json_file_path not in all_files:
                all_files.append(json_file_path)
        finally:
            try:
                await move_files(files=all_files, to_folder=data_error_path)
            except Exception:
                await remove_files(files=all_files)

        message = f"Error uploading data to CDF, mission run: `{upload_request.mission_run_id}`."
        logger.error(
            message,
            exc_info=error,
        )
        # TODO: implement robot log client
        # if isinstance(error, FileExistsError):
        #     severity = WARNING
        # else:
        #     severity = ERROR
        # await create_robot_log(
        #     message=f"{message} error: {str(error)}.",
        #     severity=severity,
        #     robot_status_queue=robot_status_queue,
        # )
    finally:
        data_upload_error_message: data_pb2.DataUploadEvent = create_data_upload_error_message(error, upload_request=upload_request)
        return data_upload_error_message
