# this is the main class - Algorithm
"""
Article : Vision-Less Sensing for Autonomous Micro-Drones -2018
By: Simon Pikalov,Elisha Azaria ,Shaya Sonnenberg,Boaz Ben-Moshe andAmos Azaria
 Drone Algorithm.
 Programmer : Lama Shawahny
"""
import enum
import time
from typing import Dict, Optional
import pid
from simple_airsim.api import coordinate_system
from simple_airsim.api.drone import Drone
from simple_airsim.api.gui_manager import GUIManager
from simple_airsim.api.manager import Manager

dist_right = 0.5  # m
dist_left = 1  # c
dist_front = 0.6  # m
dist_right_emergency = 0.4  # m
dist_left_emergency = 0.2  # c
dist_front_emergency = 0.2  # m
tunnel_emergency = 2.1
dist_back = 0.5

pitch_speed = 10
roll_speed = 5
yaw_speed = 60
pitch_speed_emergency = -5
roll_speed_emergency = 5
turn_by_yaw = 60
lidar_infinity = 4
right_error = 0.5
yaw_permanent = -5
Pr = 10
Ir = 0
Dr = 15

Pl = 1
Il = 0.000001
Dl = 6

Pf = 0.7
If = 0
Df = 1

height = -1
cullusion = 0

class State(enum.Enum):
    hover = 1
    right_wall = 2
    two_wall_flight = 3
    up = 4
    down = 5
    scan = 6
    emergency = 0


(roll_history, pitch_history, yaw_rate_history, z_history) = (0, 10, 0, -1)

right_pid = pid.PidController(Pr, Ir, Dr, dist_right)  # right pid
right_pid.set_bounds(-30, 10)

front_pid = pid.PidController(Pf, If, Df, dist_front)  # front pid
front_pid.set_bounds(-30, 8)

left_pid = pid.PidController(Pl, Il, Dl, dist_left)  # left pid
left_pid.set_bounds(-30, 10)

def normal_lidars(lidars):
    if lidars["front"] < 0:
        print("front normalized")
        lidars["front"] = dist_front
    if lidars["right"] < 0:
        print("front normalized")
        lidars["right"] = dist_right

def creat_dict(lidars):
    """
    Additional function for assumps lidars in dictionary in order to get drone state later .
    """
    dic = {}
    dic["front"] = lidars["front"]
    dic["right"] = lidars["right"]
    dic["left"] = lidars["left"]
    dic["back"] = lidars["back"]
    dic["down"] = lidars["down"]
    dic["up"] = lidars["up"]
    return dic


# The 5 states that we use in the algorithm
def Rotate_CCW(lidars):
    """
    Rotate C.C.W :slightly rotates counterclockwise(to align with the right wall).
    """
    dic=creat_dict(lidars)
    dic["state"] = "Rotate_CCW"
    print(dic)

def Emergency(lidars):
    """
    Emergency state : Drone brakes to avoid crashing
    """
    dic=creat_dict(lidars)
    dic["state"] = "Emergency"
    print(dic)

def Tunnel(lidars):
    """
    Tunnel :Drone centers in between the left and right walls while maintaining the
    desired speed.
    """
    dic=creat_dict(lidars)
    dic["state"] = "Tunnel"
    print(dic)


def Turn_CW(lidars):
    """
    Turn_CW: Drone turns 90 degrees clockwise (to find the right wall)
    """
    dic=creat_dict(lidars)
    dic["state"] = "Turn_CW"
    print(dic)


def FlyForward(lidars):
    """FlyForward: Drone flies forward while making minor adjustments to maintain
        predefined bounds, i.e., its distance from the right and the desired speed.
    """
    dic=creat_dict(lidars)
    dic["state"] = "FlyForward"
    print(dic)

def loop(drone: Drone):
    """The main algorithm for drone ,
       Controlling algorithm in which drone states are represented here .
    """
    global roll_history
    global pitch_history
    global yaw_rate_history
    global z_history
    global cullusion
    global turn_by_yaw
    global gui
    drone.move_by(6,3,0,0)
    while True:
        lidars: Dict[str, Optional[float]] = drone.get_lidars()
       # position: Dict[str, float] = drone.get_position()
       # orientation: Dict[str, float] = drone.get_orientation()
        velocity: Dict[str, float] = drone.get_velocity()
        normal_lidars(lidars)  # incase of infinity for the drone not to go crazy
        flag1=0
        fla2=0
        flag3 = 0


        (roll, pitch, yaw_rate, z) = (0, 0, 0, 0)
        now_time = time.time()
        pitch_ans = front_pid.pid(lidars["front"],now_time )
        roll_ans = right_pid.pid(lidars["right"],now_time)
        # print("right", right_pid, "\n")
        # print("front", front_pid)
        info_str = ''
        (roll, pitch, yaw_rate, z) = (roll_ans, pitch_ans, yaw_permanent, -1)
        (roll_history, pitch_history, yaw_rate_history, z_history) = (roll, pitch, yaw_rate, -1)
        info_str += '\n'

        if lidars["front"] > 0 and lidars["front"] < dist_front * 3:  # case close to wall
            (roll, pitch, yaw_rate, z) = (
                roll_ans, pitch_ans, yaw_speed * 3, -1)  # if front is a bit far rotate  counter clockwise
            print("else front :", pitch)
            info_str += F"Front rotate : {pitch}\n"
            Rotate_CCW(lidars)
            flag1=1
        flag = 0
        if lidars["right"] > lidar_infinity or lidars["right"] == right_error:  # and (lidars["front"] < lidar_infinity or lidars["back"] < lidar_infinity or lidars["left"] < lidar_infinity):
            info_str += f"right rotate : {pitch}\n"
            drone.turn_by(0, 0, turn_by_yaw, True)
            fla2=1
            Turn_CW(lidars)
            lidars = drone.get_lidars()
            if lidars["front"] >= dist_front:
                drone.move_by(1, 0, 0, True)  # TODO fix infinity loop taking the new front and right after rotation
                flag=1
            if flag==0:
                Turn_CW(lidars)
                flag=1

        if lidars["left"] < tunnel_emergency and lidars["right"] < tunnel_emergency:
            Tunnel(lidars)
            flag3=1

        if velocity['x'] > 0.3:
            pitch = -3
        pitch = pitch*4
        drone.command(roll, pitch, yaw_rate, -1)

        info_str += F"Roll: {roll}\tPitch: {pitch}\tYaw:{yaw_rate}\n"

        gui.set_algo_info(info_str)
        if flag==0 and flag1==0 and fla2==0 and flag3==0:
            FlyForward(lidars)
        time.sleep(0.05)


if __name__ == '__main__':
    with Manager(coordinate_system.AIRSIM, method=loop) as man:
        with GUIManager(man, 10, 10, 10, 3) as gui:
            gui.start()
