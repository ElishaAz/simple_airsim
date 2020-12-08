import math
from typing import Dict, Tuple

import airsim
from .global_vars import *


def relative_to_global(position: Dict[str, float], yaw: float, x, y, z) -> Tuple[float, float, float]:
    """

    :param position:
    :param yaw:
    :param x:
    :param y:
    :param z:
    :return:
    """
    rad_yaw = degree_to_radians(yaw)

    l = math.sqrt(x * x + y * y)

    # rad_ang = math.atan(y / x)

    ret_x = x * math.cos(rad_yaw) + y * math.cos(rad_yaw + math.pi / 2) + position['x']
    ret_y = x * math.sin(rad_yaw) + y * math.sin(rad_yaw + math.pi / 2) + position['y']

    return ret_x, ret_y, z + position['z']


def global_to_relative_velocity(vx, vy, vz, yaw: float) -> Tuple[float, float, float]:
    """
    :param vx:
    :param vy:
    :param vz:
    :param yaw:
    :return:
    """
    rad_yaw = degree_to_radians(yaw)

    ret_x = vx * math.cos(rad_yaw) + vy * math.sin(rad_yaw)
    ret_y = vx * -math.sin(rad_yaw) + vy * math.cos(rad_yaw)

    return ret_x, ret_y, vz


def degree_to_radians(degree: float) -> float:
    """

    :param degree:
    :return:
    """
    return degree / 180 * math.pi


def radians_to_degrees(radians: float) -> float:
    """

    :param radians:
    :return:
    """
    return radians / math.pi * 180


def range_degrees(degree: float, with_negative: bool = True) -> float:
    """

    :param degree:
    :param with_negative:
    :return:
    """
    while degree < 0:
        degree += 360

    while degree > 360:
        degree -= 360

    if with_negative:
        degree -= 180

    return degree


def quaternion_to_euler(q: airsim.Quaternionr):
    """
    Code from: https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    :param q:
    :return:
    """
    sinr_cosp = 2 * (q.w_val * q.x_val + q.y_val * q.z_val)
    cosr_cosp = 1 - 2 * (q.x_val * q.x_val + q.y_val * q.y_val)
    roll = math.atan2(sinr_cosp, cosr_cosp)
    sinp = 2 * (q.w_val * q.y_val - q.z_val * q.x_val)
    if math.fabs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2, sinp)
    else:
        pitch = math.asin(sinp)

    siny_cosp = 2 * (q.w_val * q.z_val + q.x_val * q.y_val)
    cosy_cosp = 1 - 2 * (q.y_val * q.y_val + q.z_val * q.z_val)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    # roll, pitch, yaw = airsim.to_eularian_angles(q)
    #
    # roll = radians_to_degrees(roll)
    # pitch = radians_to_degrees(pitch)
    # yaw = radians_to_degrees(yaw)

    return roll, pitch, yaw
