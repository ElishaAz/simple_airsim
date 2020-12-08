import airsim

from .global_vars import *


def angle(world: float) -> float:
    """
    Translate an angle from real-world to airsim.
    real-world angles: -180 - 180
    Airsim angles: -1 - 1

    :param world: An angle in real-world (degrees)
    :return: The angle in airsim
    """
    world /= 180
    return world


def distance(world: float) -> float:
    """
    Translate distance from real-world to airsim.
    Factor: 1/DRONE_SIZE

    :param world: Distance in real-world (meters)
    :return: The distance in airsim
    """
    world /= DRONE_SCALE
    return world
