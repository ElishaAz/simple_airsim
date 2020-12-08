import threading

import airsim
import cv2
import numpy as np
from typing import Dict

from .._utils import get_state, do_action
from . import coordinate_system, camera_config
from .drone import Drone

# _DEFAULT_LIDAR_NAMES = {"lidar_front": "front",
#                         "lidar_front_left": "front_left",
#                         "lidar_front_right": "front_right",
#                         "lidar_right": "right",
#                         "lidar_left": "left",
#                         "lidar_back": "back",
#                         "lidar_back_left": "back_left",
#                         "lidar_back_right": "back_right",
#                         "lidar_down": "down",
#                         "lidar_up": "up"}

_DEFAULT_LIDAR_NAMES = {"lidar_front": "front",
                        "lidar_right": "right",
                        "lidar_left": "left",
                        "lidar_back": "back",
                        "lidar_down": "down",
                        "lidar_up": "up"}


_RC_MAX_ROLL = 45  # degrees
_RC_MAX_PITCH = 45  # degrees
_RC_YAW_SPEED = 45  # degrees per second


def synchronized_with_attr(lock_name):
    def decorator(method):
        def synced_method(self, *args, **kws):
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

        return synced_method

    return decorator


class SimDrone(Drone):
    client: airsim.MultirotorClient

    def __init__(self, system: coordinate_system.CoordinateSystem,
                 lidar_names: Dict[str, str] = None,
                 client: airsim.MultirotorClient = None):
        """
        Initialize a drone.
        :param system: The coordinate system to use.
        :param lidar_names: The names of the lidar sensors in airsim and in code. Leave 'None' for default.
        :param client: The airsim client. Leave 'None' for default.
        """
        self.lock = threading.RLock()

        self.system = system
        if lidar_names is None:
            self.lidar_names = _DEFAULT_LIDAR_NAMES

        self.client = client
        if self.client is None:
            self.client = airsim.MultirotorClient()
            self.client.confirmConnection()
            self.client.enableApiControl(True)

    def _pause_handler(self):
        """

        :return:
        """
        pass

    # One-line functions

    @synchronized_with_attr("lock")
    def takeoff(self, wait: bool) -> None:
        """
        Takeoff.
        :param wait: Should we wait for the command to finish, or return immediately?
        """
        self._pause_handler()

        if wait:
            self.client.takeoffAsync().join()
        else:
            self.client.takeoffAsync()

    @synchronized_with_attr("lock")
    def hover(self, wait: bool) -> None:
        """
        Hover.
        :param wait: Should we wait for the command to finish, or return immediately?
        """
        self._pause_handler()

        if wait:
            self.client.hoverAsync().join()
        else:
            self.client.hoverAsync()

    @synchronized_with_attr("lock")
    def land(self, wait: bool) -> None:
        """
        Land.
        :param wait: Should we wait for the command to finish, or return immediately?
        """
        self._pause_handler()

        if wait:
            self.client.landAsync().join()
        else:
            self.client.landAsync()

    # Complex functions

    @synchronized_with_attr("lock")
    def move_by(self, x: float, y: float, z: float, wait: bool) -> None:
        """
        Move a specific amount of meters in every axis.
        Note: directions are defined by the coordinate system.
        :param x: The number of meters to move in parallel to the x axis.
        :param y: The number of meters to move in parallel to the y axis.
        :param z: The number of meters to move in parallel to the z axis.
        :param wait: Should we wait for the command to finish, or return immediately?
        """
        self._pause_handler()

        x, y, z = self.system.ta_pos(x, y, z)

        if wait:
            do_action.move_by(self.client, x, y, z).join()
        else:
            do_action.move_by(self.client, x, y, z)

    @synchronized_with_attr("lock")
    def turn_by(self, roll: float, pitch: float, yaw: float, wait: bool) -> None:
        """
        Turn a specific amount of degrees in every axis.
        Note: directions are defined by the coordinate system.
        :param roll: The number of degrees to rotate the roll (rotate around the x axis).
        :param pitch: The number of degrees to rotate the pitch (rotate around the y axis).
        :param yaw: The number of degrees to rotate the yaw (rotate around the z axis).
        :param wait: Should we wait for the command to finish, or return immediately?
        """
        self._pause_handler()

        roll, pitch, yaw = self.system.ta_ori(roll, pitch, yaw)

        if wait:
            do_action.turn_by(self.client, roll, pitch, yaw).join()
        else:
            do_action.turn_by(self.client, roll, pitch, yaw)

    @synchronized_with_attr("lock")
    def command(self, roll: float, pitch: float, yaw_rate: float, z: float,
                wait: bool = False, duration: float = 0.1) -> None:
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
        self._pause_handler()

        roll, pitch, yaw_rate = self.system.ta_ori(roll, pitch, yaw_rate)
        x, y, z = self.system.ta_pos(0, 0, z)

        if wait:
            do_action.move_roll_pitch_yaw_rate_z(self.client, roll, pitch, yaw_rate, z, duration).join()
        else:
            do_action.move_roll_pitch_yaw_rate_z(self.client, roll, pitch, yaw_rate, z, duration)

    @synchronized_with_attr("lock")
    def rc(self, right: float, forward: float, up: float, yaw: float):
        """

        :param right:
        :param forward:
        :param up:
        :param yaw:
        :return:
        """
        self._pause_handler()

        raise NotImplementedError()

    # Getters

    def get_position(self):
        """

        :return: A dictionary of 'x', 'y', 'z' and their values in meters.
        """
        self._pause_handler()

        return self._get_position()

    @synchronized_with_attr("lock")
    def _get_position(self):
        pos = get_state.position(self.client)
        x, y, z = self.system.fa_pos(pos['x'], pos['y'], pos['z'])
        return {'x': x, 'y': y, 'z': z}

    def get_orientation(self):
        """

        :return: A dictionary of 'roll', 'pitch', 'yaw' and their values in meters.
        """
        self._pause_handler()

        return self._get_orientation()

    @synchronized_with_attr("lock")
    def _get_orientation(self):
        ori = get_state.orientation(self.client)
        roll, pitch, yaw = self.system.fa_ori(ori['roll'], ori['pitch'], ori['yaw'])
        return {'roll': roll, 'pitch': pitch, 'yaw': yaw}

    def get_velocity(self):
        """

        :return: A dictionary of 'x', 'y', 'z', 'roll', 'pitch', 'yaw' and the velocity (linear or angular) in each.
        """
        self._pause_handler()

        return self._get_velocity()

    @synchronized_with_attr("lock")
    def _get_velocity(self):
        vel = get_state.velocity(self.client)
        x, y, z = self.system.fa_pos(vel['x'], vel['y'], vel['z'])
        roll, pitch, yaw = self.system.fa_ori(vel['roll'], vel['pitch'], vel['yaw'])
        return {'x': x, 'y': y, 'z': z, 'roll': roll, 'pitch': pitch, 'yaw': yaw}

    def get_lidars(self):
        """

        :return: A dictionary of the lidars as defined in 'self.lidar_names' and their values.
        """
        self._pause_handler()

        return self._get_lidars()

    @synchronized_with_attr("lock")
    def _get_lidars(self):
        return get_state.lidars(self.client, self.lidar_names)

    @synchronized_with_attr("lock")
    def get_image(self, camera_id: int, cam_type: camera_config.ImageType,
                  return_type: camera_config.ReturnType, default_alpha: int = 128) -> np.ndarray:
        """

        :return:
        """
        raw_image = self.client.simGetImage(str(camera_id), cam_type.airsim_val)
        im: np.ndarray = cv2.imdecode(airsim.string_to_uint8_array(raw_image),
                                      cv2.IMREAD_UNCHANGED if return_type.with_alpha else cv2.IMREAD_COLOR)

        if return_type.with_alpha:
            if im.shape[3] == 3:  # If image does not contain alpha, add alpha.
                np.dstack(im, np.full((im.shape[0], im.shape[1]), default_alpha, dtype=im.dtype))

            if return_type.format == "RGB":
                return cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA)
            elif return_type.format == "BGR":
                return im
        else:
            if return_type.format == "RGB":
                return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            elif return_type.format == "BGR":
                return im

    # Sim only

    @synchronized_with_attr("lock")
    def pause_sim(self):
        self.client.simPause(True)

    @synchronized_with_attr("lock")
    def resume_sim(self):
        """

        :return:
        """
        self.client.simPause(False)

    @synchronized_with_attr("lock")
    def pause_sim_state(self):
        """

        :return:
        """
        return self.client.simIsPause()

    @synchronized_with_attr("lock")
    def continue_for_time(self, seconds):
        self.client.simContinueForTime(seconds)
