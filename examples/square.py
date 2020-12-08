import time

from simple_airsim.api import coordinate_system
from simple_airsim.api.drone import Drone
from simple_airsim.api.gui_manager import GUIManager
from simple_airsim.api.manager import Manager


def loop(drone: Drone):
    drone.takeoff(True)
    while True:
        for i in range(4):
            drone.move_by(1, 0, 0, False)
            time.sleep(2)
            drone.turn_by(0, 0, 90, False)
            time.sleep(2)
        time.sleep(0.1)


if __name__ == '__main__':
    with Manager(coordinate_system.AIRSIM, method=loop) as man:
        with GUIManager(man, 10, 10, 10, 3) as gui:
            gui.start()
