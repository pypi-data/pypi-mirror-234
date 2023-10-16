# -*- coding: utf-8 -*-
"""Helper functions to create gRPC messages."""


from typing import List, Optional

from cognite_robotics.protos.messages.geometry_pb2 import BODY, MAP, Point, Quaternion, Transform
from cognite_robotics.protos.messages.joint_state_pb2 import JointState, JointStates
from cognite_robotics.protos.messages.mission_pb2 import RobotCapability
from cognite_robotics.protos.messages.payloads_pb2 import AbsolutePTZ
from cognite_robotics.protos.messages.robot_registration_pb2 import Metadata, RobotRegistrationRequest
from cognite_robotics.protos.messages.robot_state_pb2 import (
    ConnectionState,
    DockingState,
    EstopRegistrationState,
    EstopState,
    LogMessage,
    LogSeverity,
    MissionState,
    PowerState,
    RobotState,
    RobotStateMessage,
)
from cognite_robotics.protos.messages.video_pb2 import CameraControls, VideoComposition, VideoConfiguration

#####################
# RobotRegistration #
#####################


def robot_registration_request(
    robot_name: str,
    robot_description: str,
    robot_type: str,
    robot_capability_external_ids: List[str],
    video_configuration: Optional[VideoConfiguration],
    has_estop: bool,
    has_power_on: bool,
) -> RobotRegistrationRequest:
    """Create a RobotRegistrationRequest.

    Args:
        robot_name (str): Name of the robot
        robot_description (str): Description of the robot
        robot_type (str): Type of the robot (e.g. SPOT, TAUROB, ANYMAL etc.)
        robot_capabilities (List[RobotCapability]): List of robot capabilities
        video_configuration (VideoConfiguration): VideoConfiguration object
        has_estop (bool): The robot has an available emergency stop
        has_power_on (bool): The robot has an available power on/off capability
    Returns:
        RobotRegistrationRequest: RobotRegistrationRequest object
    """
    request = RobotRegistrationRequest(robot_name=robot_name, robot_description=robot_description, robot_type=robot_type)
    request.capabilities.extend(
        [RobotCapability(capability_external_id=capability_external_id) for capability_external_id in robot_capability_external_ids]
    )
    metadata = Metadata(
        three_d_model="",  # TODO: Deprecate this: https://cognitedata.atlassian.net/browse/RS-1133
        get_estop=has_estop,
        power_on=has_power_on,
    )
    request.metadata.CopyFrom(metadata)
    if video_configuration:
        request.video_config.CopyFrom(video_configuration)
    return request


def video_configuration(
    description: str, stream_id: int, room_id: int, available_video_compositions: List[str], ptz_go_to: bool, navigate_to: bool
) -> VideoConfiguration:
    """Create a VideoConfiguration.

    Args:
        description (str): Description of the video feed
        stream_id (int): ID of the stream
        room_id (int): ID of the room
        available_video_compositions (List[str]): List of available video compositions
        ptz_go_to (bool): The robot supports controlling PTZ camera by clicking in video stream
        navigate_to (bool): he robot supports navigation by clicking in video stream
    Returns:
        VideoConfiguration: VideoConfiguration object
    """
    return VideoConfiguration(
        description=description,
        stream_id=stream_id,
        room_id=room_id,
        available_video_compositions=[VideoComposition(screen=screen) for screen in available_video_compositions],
        available_camera_controls=CameraControls(
            ptz_go_to=ptz_go_to,
            navigate_to=navigate_to,
        ),
    )


######################
# RobotStateMessages #
######################


def robot_state_message(timestamp: int, robot_state: RobotState) -> RobotStateMessage:
    """Create a RobotStateMessage.

    Args:
        timestamp (int): Timestamp of the state
        robot_state (RobotState): RobotState object
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    message = RobotStateMessage(ping_sent=timestamp)
    message.robot_state.CopyFrom(robot_state)
    return message


def robot_pose_state_message(
    timestamp: int, pos_x: float, pos_y: float, pos_z: float, quat_x: int, quat_y: int, quat_z: int, quat_w: int
) -> RobotStateMessage:
    """Create a RobotStateMessage with the robot pose.

    Args:
        timestamp (int): Timestamp of the state
        pos_x (float): X position of the robot
        pos_y (float): Y position of the robot
        pos_z (float): Z position of the robot
        quat_x (int): X quaternion of the robot
        quat_y (int): Y quaternion of the robot
        quat_z (int): Z quaternion of the robot
        quat_w (int): W quaternion of the robot
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    position = Point(x=pos_x, y=pos_y, z=pos_z)
    orientation = Quaternion(x=quat_x, y=quat_y, z=quat_z, w=quat_w)
    transform = Transform(to=MAP, frm=BODY, translation=position, orientation=orientation)
    robot_state = RobotState(map_transform=transform)
    return robot_state_message(timestamp, robot_state)


def robot_joint_states_state_message(timestamp: int, joint_states: List[JointState]) -> RobotStateMessage:
    """Create a RobotStateMessage with the joint states.

    Args:
        timestamp (int): Timestamp of the state
        joint_states (List[JointState]): List of joint states
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    joint_states_message = JointStates(joint_states=joint_states)
    robot_state = RobotState(joint_states=joint_states_message)
    return robot_state_message(timestamp, robot_state)


def robot_mission_state_message(timestamp: int, mission_state: MissionState.ValueType) -> RobotStateMessage:
    """Create a RobotStateMessage with the mission state.

    Args:
        timestamp (int): Timestamp of the state
        mission_state (MissionState.ValueType): Mission state of the robot
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    robot_state = RobotState(mission_state=mission_state)
    return robot_state_message(timestamp, robot_state)


def robot_connection_state_message(timestamp: int, connection_state: ConnectionState.ValueType) -> RobotStateMessage:
    """Create a RobotStateMessage with the connection state.

    Args:
        timestamp (int): Timestamp of the state
        connection_state (ConnectionState.ValueType): Connection state of the robot
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    robot_state = RobotState(connection_state=connection_state)
    return robot_state_message(timestamp, robot_state)


def robot_docking_state_message(timestamp: int, docking_state: DockingState.ValueType) -> RobotStateMessage:
    """Create a RobotStateMessage with the docking state.

    Args:
        timestamp (int): Timestamp of the state
        docking_state (DockingState): Docking state of the robot
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    robot_state = RobotState(docking_state=docking_state)
    return robot_state_message(timestamp, robot_state)


def robot_power_state_message(timestamp: int, power_state: PowerState.ValueType) -> RobotStateMessage:
    """Create a RobotStateMessage with the power state.

    Args:
        timestamp (int): Timestamp of the state
        power_state (PowerState): Power state of the robot
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    robot_state = RobotState(power_state=power_state)
    return robot_state_message(timestamp, robot_state)


def robot_absolute_ptz_state_message(timestamp: int, pan: float, tilt: float, zoom: float) -> RobotStateMessage:
    """Create a RobotStateMessage with the absolute PTZ state.

    Args:
        timestamp (int): Timestamp of the state
        pan (float): Pan of the PTZ camera
        tilt (float): Tilt of the PTZ camera
        zoom (float): Zoom of the PTZ camera
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    absolute_ptz = AbsolutePTZ(pan=pan, tilt=tilt, zoom=zoom)
    robot_state = RobotState(ptz_state=absolute_ptz)
    return robot_state_message(timestamp, robot_state)


def robot_battery_percentage_state_message(timestamp: int, battery_percentage: float) -> RobotStateMessage:
    """Create a RobotStateMessage with the battery percentage.

    Args:
        timestamp (int): Timestamp of the state
        battery_percentage (float): Battery percentage of the robot
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    robot_state = RobotState(battery_percentage=battery_percentage)
    return robot_state_message(timestamp, robot_state)


def robot_log_message_state_message(timestamp: int, message: str, severity: LogSeverity.ValueType) -> RobotStateMessage:
    """Create a RobotStateMessage with the log message.

    Args:
        timestamp (int): Timestamp of the state
        message (str): Log message
        severity (LogSeverity.ValueType): Severity of the log message
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    log_message = LogMessage(severity=severity, message=message)
    robot_state = RobotState(log_message=log_message)
    return robot_state_message(timestamp, robot_state)


def robot_estop_state_message(timestamp: int, estop_state: EstopState.ValueType) -> RobotStateMessage:
    """Create a RobotStateMessage with the estop state.

    Args:
        timestamp (int): Timestamp of the state
        estop_state (EStopState.ValueType): EStop state of the robot
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    robot_state = RobotState(estop_state=estop_state)
    return robot_state_message(timestamp, robot_state)


def robot_estop_registration_state_message(timestamp: int, estop_registration_state: EstopRegistrationState.ValueType) -> RobotStateMessage:
    """Create a RobotStateMessage with the estop registration state.

    Args:
        timestamp (int): Timestamp of the state
        estop_registration_state (EStopRegistrationState.ValueType): EStop registration state of the robot
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    robot_state = RobotState(estop_registration_state=estop_registration_state)
    return robot_state_message(timestamp, robot_state)
