import math

from .global_vars import *


def angle(airsim_angle: float) -> float:
    """
    Translate an angle from airsim to real-world.
    Airsim angles: -1 - 1
    real-world angles: -180 - 180

    :param airsim_angle: An angle in airsim
    :return: The angle in real-world (degrees)
    """
    math.asin(airsim_angle) * 2
    airsim_angle *= 180
    return airsim_angle


def distance(airsim_distance: float) -> float:
    """
    Translate distance from airsim to real-world.
    Factor: DRONE_SIZE

    :param airsim_distance: Distance in airsim
    :return: The distance in real-world (meters)
    """
    airsim_distance *= DRONE_SCALE
    return airsim_distance
