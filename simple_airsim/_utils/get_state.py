import airsim
from typing import Dict, Optional

from . import airsim_to_world, world_to_airsim, tools, airsim_lidars
from . import global_vars


def orientation(client: airsim.MultirotorClient) -> Dict[str, float]:
    """

    :param client: The multirotor client.
    :return: A dictionary of the orientation {"roll", "pitch", "yaw"} in real-world
    """

    ori = client.simGetVehiclePose().orientation
    roll, pitch, yaw = tools.quaternion_to_euler(ori)
    return {"roll": tools.radians_to_degrees(roll),
            "pitch": tools.radians_to_degrees(pitch),
            "yaw": tools.radians_to_degrees(yaw)}


def position(client: airsim.MultirotorClient) -> Dict[str, float]:
    """

    :param client: The multirotor client.
    :return: A dictionary of the position {"front", "right", "up"} in real-world
    """
    pos = client.simGetVehiclePose().position
    return {"x": airsim_to_world.distance(pos.x_val),
            "y": airsim_to_world.distance(pos.y_val),
            "z": airsim_to_world.distance(pos.z_val)}


def lidars(client: airsim.MultirotorClient, lidar_names: Dict[str, str]) -> Dict[str, Optional[float]]:
    """
    :param client: The multirotor client.
    :param lidar_names: The name dictionary of the lidars.
    :return: A dictionary of the lidars in real-world (meters).
    """
    lid = airsim_lidars.get(client, lidar_names)
    ret = {}
    for k in lid:
        if lid[k] is None:
            ret[k] = None
        else:
            ret[k] = airsim_to_world.distance(lid[k])

    return ret


def velocity(client: airsim.MultirotorClient) -> Dict[str, float]:
    """

    :param client: The multirotor client.
    :return: A dictionary of the velocities of the drone in x, y, z, roll, pitch, yaw.
    """
    kinematics_estimated = client.getMultirotorState().kinematics_estimated
    linear_velocity = kinematics_estimated.linear_velocity
    angular_velocity = kinematics_estimated.angular_velocity

    x, y, z = tools.global_to_relative_velocity(airsim_to_world.distance(linear_velocity.x_val),
                                                airsim_to_world.distance(linear_velocity.y_val),
                                                airsim_to_world.distance(linear_velocity.z_val),
                                                orientation(client)['yaw'])
    # x = distance(linear_velocity.x_val)
    # y = distance(linear_velocity.y_val)
    # z = distance(linear_velocity.z_val)
    roll = tools.radians_to_degrees(angular_velocity.x_val)
    pitch = tools.radians_to_degrees(angular_velocity.y_val)
    yaw = tools.radians_to_degrees(angular_velocity.z_val)

    return {'x': x, 'y': y, 'z': z, 'roll': roll, 'pitch': pitch, 'yaw': yaw}
