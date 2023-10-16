# -*- coding: utf-8 -*-
"""CogniteRobotics robot interface gRPC client."""
import asyncio
import logging
from typing import AsyncGenerator, Union

import grpc

from cognite_robotics.config.config import CogniteRoboticsClientConfig, LocalClientConfig
from cognite_robotics.grpc.helpers.channel import get_insecure_channel, get_secure_channel
from cognite_robotics.protos.messages import connectivity_pb2, data_pb2
from cognite_robotics.protos.messages.common_pb2 import Connect, SuccessMessage
from cognite_robotics.protos.messages.mission_log_pb2 import MissionLogMessage
from cognite_robotics.protos.messages.robot_control_pb2 import ControlEvent, ControlResponse, UserControlCommand
from cognite_robotics.protos.messages.robot_registration_pb2 import RobotRegistrationRequest
from cognite_robotics.protos.messages.robot_state_pb2 import RobotStateMessage
from cognite_robotics.protos.services.robot_interface_pb2_grpc import RobotInterfaceStub
from cognite_robotics.utils.utils import handle_grpc_error

logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class CogniteRobotInterfaceClient:
    """gRPC Client for robot <-> cloud communication."""

    def __init__(self, client_config: Union[CogniteRoboticsClientConfig, LocalClientConfig]) -> None:
        """Initialize gRPC client for robot <-> cloud comunication."""
        self.client_config = client_config
        self._metadata = None if isinstance(self.client_config, CogniteRoboticsClientConfig) else [("auth-ticket", "TESTTICKET")]
        self.initialized_channel = False
        self.stop_tasks_trigger = asyncio.Event()  # Event to stop client loops

    async def connect(self) -> None:
        """Connect to remote/cloud host."""
        await self._refresh_channel()
        self.initialized_channel = True

    async def shutdown_client(self) -> None:
        """Shut down gRPC client."""
        self.stop_tasks_trigger.set()

    async def _refresh_channel(self) -> None:
        if isinstance(self.client_config, CogniteRoboticsClientConfig):
            logger.info("Setting up a secure channel.")
            channel = await get_secure_channel(
                self.client_config.project, self.client_config.oidc_token_callable, self.client_config.target
            )
        else:
            logger.info(f"Setting up an insecure channel at {self.client_config.ip}:{self.client_config.port}.")
            channel = await get_insecure_channel(self.client_config.ip, self.client_config.port)

        self.robot_interface_client = RobotInterfaceStub(channel)

    async def register_robot(self, request: RobotRegistrationRequest) -> None:
        """Register the robot with Cognite Robotics.

        Args:
            request (RobotRegistrationRequest): Robot registration request
        """
        if not self.initialized_channel:
            await self._refresh_channel()
            self.initialized_channel = True

        await self.robot_interface_client.RobotRegistration(request, metadata=self._metadata)

    async def robot_connectivity(self) -> None:
        """Set up a stream to send connectivity status to cloud and send connected messages."""
        if not self.initialized_channel:
            await self._refresh_channel()
            self.initialized_channel = True
        queue: "asyncio.Queue[connectivity_pb2.Pong]" = asyncio.Queue()

        async def _generate_pong() -> AsyncGenerator[object, None]:
            connect_message = Connect()
            pong = connectivity_pb2.Pong()
            pong.connect.CopyFrom(connect_message)
            yield pong
            while not self.stop_tasks_trigger.is_set():
                pong = await queue.get()
                yield pong

        while not self.stop_tasks_trigger.is_set():
            stream = self.robot_interface_client.RobotConnectivity(_generate_pong(), metadata=self._metadata)
            try:
                async for ping in stream:
                    pong = connectivity_pb2.Pong()
                    pong.connectivity_status.request_id = ping.request_id
                    pong.connectivity_status.ping_sent_at = ping.timestamp
                    await queue.put(pong)
            except grpc.RpcError as e:
                await handle_grpc_error(e, invoker="robot_connectivity")
            except Exception as e:
                logger.exception("An error occurred when trying to establish a ping-pong connection to the cloud", exc_info=e)
                raise e

    async def send_robot_states(self, states_generator: AsyncGenerator[RobotStateMessage, None]) -> None:
        """Send RobotStateMessages to the cloud.

        Args:
            states_generator (AsyncGenerator[RobotStateMessage, None]): generator of RobotStateMessages
        """
        if not self.initialized_channel:
            await self._refresh_channel()
            self.initialized_channel = True
        while not self.stop_tasks_trigger.is_set():
            stream = self.robot_interface_client.RobotStatus(states_generator, metadata=self._metadata)
            try:
                async for _ in stream:
                    pass
            except grpc.RpcError as e:
                await handle_grpc_error(e, invoker="send_robot_states")
            except Exception as e:
                logger.exception("An error occurred when in the robot states stream", exc_info=e)
                raise e

    async def receive_robot_control_messages(self) -> AsyncGenerator[UserControlCommand, None]:
        """Receive control messages from the cloud service.

        This function sets up a bi-directional stream to the robot control endpoint in Robotics Services.
        On each received control command issued by the user, we send a success control event message
        back on the stream, and yield the received UserControlCommand for further processing (e.g., send
        to the robot-specific API.

        Yields
            AsyncGenerator[UserControlCommand, None]: UserControlCommand

        """
        if not self.initialized_channel:
            await self._refresh_channel()
            self.initialized_channel = True

        queue: "asyncio.Queue[ControlEvent]" = asyncio.Queue()

        async def _generate_control_events() -> AsyncGenerator[ControlEvent, None]:
            connect_message = Connect()
            control_event = ControlEvent()
            control_event.connect.CopyFrom(connect_message)
            yield control_event
            while not self.stop_tasks_trigger.is_set():
                control_event = await queue.get()
                yield control_event

        while not self.stop_tasks_trigger.is_set():
            stream = self.robot_interface_client.RobotControl(_generate_control_events(), metadata=self._metadata)
            try:
                async for control_command in stream:
                    request_id = control_command.request_id
                    success_message = SuccessMessage(message="Received control command.")
                    control_response = ControlResponse(request_id=request_id, success=success_message)
                    control_response.command.CopyFrom(control_command.command)
                    control_event = ControlEvent()
                    control_event.robot_control_log.CopyFrom(control_response)
                    await queue.put(control_event)
                    yield control_command.command
            except grpc.RpcError as e:
                await handle_grpc_error(e, invoker="receive_robot_control_messages")
            except Exception as e:
                logger.exception("An error occurred when in the robot control stream", exc_info=e)
                raise e

    async def send_mission_log_messages(self, mission_log_generator: AsyncGenerator[MissionLogMessage, None]) -> None:
        """Send MissionLogMessages to the cloud.

        Args:
            mission_log_generator (AsyncGenerator[MissionLogMessage, None]): generator of MissionLogMessage
        """
        if not self.initialized_channel:
            await self._refresh_channel()
            self.initialized_channel = True

        while not self.stop_tasks_trigger.is_set():
            stream = self.robot_interface_client.MissionLog(mission_log_generator, metadata=self._metadata)
            try:
                async for _ in stream:
                    pass
            except grpc.RpcError as e:
                await handle_grpc_error(e, invoker="send_mission_log_messages")
            except Exception as e:
                logger.exception("An error occurred when in the mission log stream", exc_info=e)
                raise e

    async def send_data_upload_event(self, event: data_pb2.DataUploadEvent) -> None:
        """Send data upload event to Robotics Services."""
        if not self.initialized_channel:
            await self._refresh_channel()
            self.initialized_channel = True
        await self.robot_interface_client.DataUpload(event, metadata=self._metadata)
