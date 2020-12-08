import math
from typing import Optional, Dict

import airsim
import numpy as np

from . import world_to_airsim


def _parse_lidarData(data):
    # reshape array of floats to array of [X,Y,Z]
    points = np.array(data.point_cloud, dtype=np.dtype('f4'))
    points = np.reshape(points, (int(points.shape[0] / 3), 3))

    return points


def _get_dist(point: np.ndarray, pos: np.ndarray) -> float:
    x = point[0] - pos[0]
    y = point[1] - pos[1]
    z = point[2] - pos[2]

    return math.sqrt(x * x + y * y + z * z)


def _lidar_dist(lidar: airsim.LidarData) -> Optional[float]:
    if len(lidar.point_cloud) < 3:
        return world_to_airsim.distance(-1)

    point = _parse_lidarData(lidar)[-1]
    val = _get_dist(point, np.array([0, 0, 0]))
    return val if val is not None else world_to_airsim.distance(-1)


def get(client: airsim.MultirotorClient, lidar_names: Dict[str, str]):
    """

    :param client: 
    :param lidar_names: 
    :return:
    """
    return_value = {}
    for name, value in lidar_names.items():
        return_value[value] = _lidar_dist(client.getLidarData(lidar_name=name))
    return return_value
