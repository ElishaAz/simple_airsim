import time
from threading import Thread
from typing import Callable, Dict

from .manager import Manager

DEFAULT_VALUES = {
    "time": lambda man: time.time(),
    "x": lambda man: man.get_position()['x'],
    "y": lambda man: man.get_position()['y'],
    "z": lambda man: man.get_position()['z'],

    "pitch": lambda man: man.get_orientation()['pitch'],
    "roll": lambda man: man.get_orientation()['roll'],
    "yaw": lambda man: man.get_orientation()['yaw'],

    "vx": lambda man: man.get_velocity()['x'],
    "vy": lambda man: man.get_velocity()['y'],
    "vz": lambda man: man.get_velocity()['z'],

    "up": lambda man: man.get_lidars()['up'],
    "front": lambda man: man.get_lidars()['front'],
    "back": lambda man: man.get_lidars()['back'],
    "right": lambda man: man.get_lidars()['right'],
    "left": lambda man: man.get_lidars()['left'],
}


class LogWriter:
    man: Manager

    def __init__(self, man: Manager, values: Dict[str, Callable[[Manager], str]] = None, filename: str = None,
                 use_thread=True, t_delta_time=0.1):
        """

        :param man: The Manager object to read the values from.
        :param values:
        :param filename:
        :param use_thread:
        :param t_delta_time:
        """
        self.filename = filename

        if filename is None:
            filename = 'logs/Logs ' + time.strftime("%d%m%Y-%H%M%S") + '.csv'

        self.t_delta_time = t_delta_time
        self.run = True
        self.use_thread = use_thread
        self.man = man
        self.values = values

        if values is None:
            self.values = DEFAULT_VALUES

        if use_thread:
            self.write_thread = Thread()

        self.file = None

    def _print_first_line(self):
        """

        :return:
        """
        with open(self.filename, "a") as file:
            file.write(', '.join(self.values.keys()))
            file.flush()
            file.close()

    def write(self):
        """

        :return:
        """
        with open(self.filename, "a") as file:
            val = []

            for x in self.values.values():
                val.append(x(self.man))

            file.write(', '.join(val))

            # file.write(', '.join((x(self.man) for x in self.values.values())))

            file.flush()
            file.close()

    def _write_loop(self):
        """

        :return:
        """
        while self.run:
            self.write()
            time.sleep(self.t_delta_time)

    def stop_thread(self):
        self.run = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.run = False
