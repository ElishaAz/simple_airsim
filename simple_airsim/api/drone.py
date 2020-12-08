from abc import ABC, abstractmethod

from typing import Dict, Optional

import numpy as np

from . import camera_config


class Drone(ABC):
    @abstractmethod
    def _pause_handler(self) -> None:
        """

        :return:
        """
        pass

    @abstractmethod
    def takeoff(self, wait) -> None:
        """
        Takeoff.
        :param wait: Should we wait for the command to finish, or return immediately?
        """
        pass

    @abstractmethod
    def hover(self, wait) -> None:
        """
        Hover.
        :param wait: Should we wait for the command to finish, or return immediately?
        """
        pass

    @abstractmethod
    def land(self, wait) -> None:
        """
        Land.
        :param wait: Should we wait for the command to finish, or return immediately?
        """
        pass

    @abstractmethod
    def move_by(self, x, y, z, wait) -> None:
        """
        Move a specific amount of meters in every axis.
        Note: directions are defined by the coordinate system.
        :param x: The number of meters to move in parallel to the x axis.
        :param y: The number of meters to move in parallel to the y axis.
        :param z: The number of meters to move in parallel to the z axis.
        :param wait: Should we wait for the command to finish, or return immediately?
        """
        pass

    @abstractmethod
    def turn_by(self, roll, pitch, yaw, wait) -> None:
        """
        Turn a specific amount of degrees in every axis.
        Note: directions are defined by the coordinate system.
        :param roll: The number of degrees to rotate the roll (rotate around the x axis).
        :param pitch: The number of degrees to rotate the pitch (rotate around the y axis).
        :param yaw: The number of degrees to rotate the yaw (rotate around the z axis).
        :param wait: Should we wait for the command to finish, or return immediately?
        """
        pass

    @abstractmethod
    def command(self, roll, pitch, yaw_rate, z, wait=False, duration=0.1) -> None:
        """
        Target a specific roll, pitch, and z, with a specific speed in yaw.
        Note: directions are defined by the coordinate system.
        :param roll: The target roll in degrees.
        :param pitch: The target pitch in degrees.
        :param yaw_rate: The yaw speed in degrees per second.
        :param z: The target height.
        :param wait: Should we wait for the command to finish, or return immediately?
        :param duration: Time (in seconds) to execute this call.
         This will be overridden if a different api function is called during this time.
        """
        pass

    @abstractmethod
    def rc(self, right, forward, up, yaw) -> None:
        """
        Not implemented.

        :param right:
        :param forward:
        :param up:
        :param yaw:
        :return:
        """
        pass

    @abstractmethod
    def get_position(self) -> Dict[str, float]:
        """

        :return: A dictionary of 'x', 'y', 'z' and their values in meters.
        """
        pass

    @abstractmethod
    def get_orientation(self) -> Dict[str, float]:
        """

        :return: A dictionary of 'roll', 'pitch', 'yaw' and their values in meters.
        """
        pass

    @abstractmethod
    def get_velocity(self) -> Dict[str, float]:
        """

        :return: A dictionary of 'x', 'y', 'z', 'roll', 'pitch', 'yaw' and the velocity (linear or angular) in each.
        """
        pass

    @abstractmethod
    def get_lidars(self) -> Dict[str, Optional[float]]:
        """

        :return: A dictionary of the lidar names and their values.
        """
        pass

    def get_image(self, camera_id: int, cam_type: camera_config.ImageType,
                  return_type: camera_config.ReturnType) -> np.ndarray:
        """
        Get an image from the drone.
        :param camera_id: The id of the camera.
        :param cam_type: The type of the image (e.g. depth, segmentation etc.).
        :param return_type: The return format i.e. RGB or BGR, and with / without alpha.
        :return: A numpy array of the image (in the shape (x, y, color)).
        """
        pass
