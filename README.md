# Simple AirSim
This is a project for simplifying the use of the AirSim drone simulator.

### Airsim
[Airsim](https://github.com/microsoft/AirSim) is a simulator for drones, cars and more, built on [Unreal Engine](https://www.unrealengine.com/).
It is open-source, cross platform, and supports hardware-in-loop with popular flight controllers such as PX4 for physically and visually realistic simulations.
It is developed as an Unreal plugin that can simply be dropped into any Unreal environment.
Airsim's goal is to develop AirSim as a platform for AI research to experiment with deep learning, computer vision and reinforcement learning algorithms for autonomous vehicles.
For this purpose, AirSim also exposes APIs to retrieve data and control vehicles in a platform independent way.

But, AirSim is hard to work with. That's why we made this package.


## Getting Started
### Installation
This project works on windows. Linux and MacOS weren't tested.

Download one of the environments in the Environments section, one built by [Airsim](https://github.com/microsoft/AirSim/releases), or [build one yourself](https://microsoft.github.io/AirSim/unreal_custenv/).

Clone or download this repository into your project.

Install the python prerequisites using pip:
```
pip install -r requirements.txt
```
Copy `settings.json` to `C:\Users\<username>\Documents\AirSim\`.

For keyboard control (optional) install [vJoy](http://vjoystick.sourceforge.net/site/index.php/download-a-install/download).

### Template Script
Create a new python file and paste the following in it:
```python
from simple_airsim.api import coordinate_system
from simple_airsim.api.drone import Drone
from simple_airsim.api.gui_manager import GUIManager
from simple_airsim.api.manager import Manager

def my_algorithm(drone: Drone):
    # Add your code here
    pass

if __name__ == '__main__':
    with Manager(coordinate_system.AIRSIM, method=my_algorithm) as man:
        with GUIManager(man, 10, 10, 10, 3) as gui:
            gui.start()
```
Your algorithm will be inside `my_algorithm`.

Look at the following example:
```python
import time

from simple_airsim.api import coordinate_system
from simple_airsim.api.drone import Drone
from simple_airsim.api.gui_manager import GUIManager
from simple_airsim.api.manager import Manager


def square(drone: Drone):
    drone.takeoff(True)
    while True:
        for i in range(4):
            drone.move_by(1, 0, 0, True)
            drone.turn_by(0, 0, 90, True)
        time.sleep(0.1)


if __name__ == '__main__':
    with Manager(coordinate_system.AIRSIM, method=square) as man:
        with GUIManager(man, 10, 10, 10, 3) as gui:
            gui.start()
```
This code will make the drone fly in a square.

### API
The simulative drone is controlled using calls to a Drone object.
The following calls are supported:

#### drone.takeoff()
Starts the drone. The drone will stay in place until the next command is sent.
#### drone.hover()
Cancel the last command and stay in place.
#### drone.land()
Lands the drone.

#### drone.move_by(x, y, z)
Moves by a specified relative distance (in x, y, z).
#### drone.turn_by(x, y, z)
Turns by a specified relative angle (in roll, pitch, yaw).

#### drone.command(roll, pitch, yaw_rate, z)
Sets the desired roll, and pitch, the desired turn speed in the yaw, and the desired height in the z.

#### drone.get_position()
Returns the drone's position in relation to it's starting point, as a dictionary of 'x', 'y', and 'z' in meters.
#### drone.get_orientation()
Returns the drone's orientation in relation to it's starting point, as a dictionary of 'roll', 'pitch' and 'yaw', in degrees.
### drone.get_velocity()
Returns the drone's velocity in all directions an angles as a dictionary of 'x', 'y', 'z', 'roll', 'pitch', and 'yaw'.
The distances are in meters per second, an the angles are in degrees per second.
#### drone.get_lidars()
Returns the distances from the closest object in all siz directions as a dictionary of 'up', 'down', 'right', 'left',
'front', and 'back', in meters.


Most of the calls also have a 'wait' variable that when set to True will cause the call to only return when finished executing.

## UI

 Features:
 -
 - The drone can be controlled manually using the keyboard, which is helpful for moving the drone to specific places to test an algorithm.
 - The UI shows the drone's position and orientation, as well as the velocity and lidars for easy debugging.
 
### Keyboard Control In Manual Mode
When in Manual Mode, the drone can be controlled using the keyboard, where w/s is throttle, a/d is yaw, up/down is pitch and right/left is roll.

## Environments
We built a few environments to use with this project.

### Line
Link: [Google Drive](https://drive.google.com/file/d/13tKpQrCp1C_KVA_MBFir8fTUaLUs2mBy/view?usp=sharing).

### Square Maze
A simple square track for testing. Link: [Google Drive](https://drive.google.com/file/d/1GSrkXP904t9fP9e7vn6H4vraATs5MePH/view?usp=sharing).

### Ellipse
Link: [Google Drive](https://drive.google.com/file/d/1mrxdPTw27qcFmZ4fyL0wedawqf-rmjMb/view?usp=sharing).

### House
A single-floor house based on a image of a house plan. Link: [Google Drive](https://drive.google.com/file/d/10Nqdo9WjlPTiH_wc9YrR3eiLKGZ-pQdP/view?usp=sharing)
(Additional files: [Google Drive](https://drive.google.com/drive/folders/1m6iZjXdWv4bktlqauYL2k9xcMQaI-Goh?usp=sharing)).


