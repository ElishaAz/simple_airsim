from abc import ABC, abstractmethod
from enum import Enum

from typing import Tuple


class CoordinateSystem(ABC):
    """
    A class that defines a coordinate system.
    The default coordinate system is Airsim (see: "Coordinate System.md").
    This class then translates it into other coordinate systems.
    """

    @abstractmethod
    def fa_pos(self, x, y, z) -> Tuple[float, float, float]:
        """
        Translate position from airsim coordinate system to this one.
        :param x: x in airsim coordinates, in meters.
        :param y: y in airsim coordinates, in meters.
        :param z: z in airsim coordinates, in meters.
        :return: x, y, z tuple in current coordinates.
        """
        pass

    @abstractmethod
    def fa_ori(self, r, p, y) -> Tuple[float, float, float]:
        """
        Translate orientation from airsim coordinate system to this one.
        :param r: roll in airsim coordinates, in degrees.
        :param p: pitch in airsim coordinates, in degrees.
        :param y: yaw in airsim coordinates, in degrees.
        :return: roll, pitch, yaw tuple in current coordinates.
        """
        pass

    @abstractmethod
    def ta_pos(self, x, y, z) -> Tuple[float, float, float]:
        """
        Translate position from current coordinate system to airsim.
        :param x: x in current coordinates, in meters.
        :param y: y in current coordinates, in meters.
        :param z: z in current coordinates, in meters.
        :return: x, y, z tuple in airsim coordinates.
        """
        pass

    @abstractmethod
    def ta_ori(self, r, p, y) -> Tuple[float, float, float]:
        """
        Translate orientation from current coordinate system to airsim.
        :param r: roll in current coordinates, in degrees.
        :param p: pitch in current coordinates, in degrees.
        :param y: yaw in current coordinates, in degrees.
        :return: roll, pitch, yaw tuple in airsim coordinates.
        """
        pass


# airsim coordinate system (see: "Coordinate System.md").
AIRSIM = type("AIRSIM_COORDINATE_SYSTEM_TYPE", (CoordinateSystem, object),
              {"fa_pos": lambda s, x, y, z: (x, y, z),
               "fa_ori": lambda s, r, p, y: (r, p, y),
               "ta_pos": lambda s, x, y, z: (x, y, z),
               "ta_ori": lambda s, r, p, y: (r, p, y),
               '__doc__': "Airsim coordinate system (see: 'Coordinate System.md')."})()

# dji coordinate system (see: "Coordinate System.md").
DJI = type("DJI_COORDINATE_SYSTEM_TYPE", (CoordinateSystem, object),
           {"fa_pos": lambda s, x, y, z: (x, y, z),
            "fa_ori": lambda s, r, p, y: (r, -p, -y),
            "ta_pos": lambda s, x, y, z: (x, y, z),
            "ta_ori": lambda s, r, p, y: (r, -p, -y),
            '__doc__': "DJI coordinate system (see: 'Coordinate System.md')."})()
