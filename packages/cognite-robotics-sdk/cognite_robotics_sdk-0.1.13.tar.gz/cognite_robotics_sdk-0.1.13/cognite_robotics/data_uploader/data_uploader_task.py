# -*- coding: utf-8 -*-
"""Main for data uploader."""
import asyncio

from cognite_robotics.data_uploader.data_classes import DataUploaderConfig
from cognite_robotics.data_uploader.data_uploader import data_upload_event_message_publisher, data_uploader
from cognite_robotics.grpc.clients.robot_interface_client import CogniteRobotInterfaceClient
from cognite_robotics.protos.messages import data_pb2
from cognite_robotics.utils.utils import create_cognite_client


async def data_uploader_tasks(
    stop_task_trigger: asyncio.Event,
    robot_interface_client: CogniteRobotInterfaceClient,
    data_set_id: int,
    config: DataUploaderConfig,
) -> None:
    """Set up tasks for data uploader."""
    data_upload_event_queue: "asyncio.Queue[data_pb2.DataUploadEvent]" = asyncio.Queue()
    cognite_client = create_cognite_client(client_name="data_uploader")

    data_uploader_task = asyncio.create_task(
        data_uploader(
            stop_task_trigger=stop_task_trigger,
            data_upload_event_queue=data_upload_event_queue,
            cognite_client=cognite_client,
            data_set_id=data_set_id,
            config=config,
        ),
        name="data_uploader",
    )

    data_upload_event_message_publisher_task = asyncio.create_task(
        data_upload_event_message_publisher(
            stop_task_trigger=stop_task_trigger,
            robot_interface_client=robot_interface_client,
            data_upload_event_queue=data_upload_event_queue,
        ),
        name="data_upload_event_publisher",
    )

    await asyncio.wait([data_uploader_task, data_upload_event_message_publisher_task], return_when=asyncio.FIRST_EXCEPTION)
