import sys
from typing import Callable, Any, Dict, Iterable, Optional

import airsim

from . import coordinate_system
from .sim_drone import SimDrone

from threading import Event, Thread


class Manager:
    class _PauseDrone(SimDrone):
        """

        """
        _run_event: Event
        _term: bool

        def __init__(self, system: coordinate_system.CoordinateSystem, lidar_names: Dict[str, str] = None,
                     client: airsim.MultirotorClient = None):
            super().__init__(system, lidar_names, client)
            self._run_event: Event = Event()
            self._run_event.set()
            self._term = False

        def _pause_handler(self):
            super()._pause_handler()
            if self._term:
                sys.exit()
            self._run_event.wait()
            if self._term:
                sys.exit()

        def pause(self):
            self._run_event.clear()

        def resume(self):
            self._run_event.set()

        def terminate(self):
            self._term = True
            self._run_event.set()

        def is_paused(self):
            return not self._run_event.is_set()

        def _determinate(self):
            self._term = False

    _drone: _PauseDrone
    algo_thread: Optional[Thread]
    algo_started: bool

    def __init__(self, system: coordinate_system.CoordinateSystem, lidar_names: Optional[Dict[str, str]] = None,
                 client: Optional[airsim.MultirotorClient] = None,
                 method: Optional[Callable[..., Any]] = None, default_args: Optional[Iterable] = None):
        """

        :param system:
        :param lidar_names:
        :param client:
        :param method:
        :param default_args:
        """
        self.default_args = default_args
        self.method = method
        self._drone = self._PauseDrone(system, lidar_names, client)
        self.algo_started = False
        self.algo_thread = None

    def start_algo(self, new_args: Optional[Iterable] = None):
        """

        :return:
        """
        args = [self._drone]
        if new_args is None:
            if self.default_args is not None:
                args += self.default_args
        else:
            args += new_args

        if self.algo_thread is None or not self.algo_thread.is_alive():
            # noinspection PyProtectedMember
            self._drone._determinate()
            self.algo_thread = Thread(target=self.method, args=args)
            self.algo_thread.start()
            self.algo_started = True

        if self._drone.is_paused():
            self._drone.resume()

    def pause_algo(self):
        """

        :return:
        """
        self._drone.pause()

    def resume_algo(self):
        """

        :return:
        """
        self._drone.resume()

    def terminate_algo(self):
        """

        :return:
        """
        if self.algo_thread is not None and self.algo_thread.is_alive():
            self._drone.terminate()
            self.algo_started = False
            self.algo_thread.join()

    # Getters

    def get_algo_state(self):
        """

        :return: 'running', 'paused' or 'terminated'
        """
        if self.algo_started:
            if self._drone.is_paused():
                return 'paused'
            else:
                return 'running'
        else:
            return 'stopped'

    def get_airsim_client(self) -> airsim.MultirotorClient:
        """

        :return:
        """
        return self._drone.client

    # noinspection PyProtectedMember
    def get_position(self):
        return self._drone._get_position()

    # noinspection PyProtectedMember
    def get_orientation(self):
        return self._drone._get_orientation()

    # noinspection PyProtectedMember
    def get_velocity(self):
        return self._drone._get_velocity()

    # noinspection PyProtectedMember
    def get_lidars(self):
        return self._drone._get_lidars()

    def __enter__(self):
        """

        :return:
        """
        return self

    def __exit__(self, *args):
        """

        :param args:
        :return:
        """
        self.get_airsim_client().enableApiControl(False)
        self.terminate_algo()
