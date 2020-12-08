import airsim
from msgpackrpc.future import Future

from . import airsim_to_world, tools, world_to_airsim, get_state

def turn_by(client: airsim.MultirotorClient, roll, pitch, yaw) -> Future:
    """

    :param yaw:
    """
    roll = tools.degree_to_radians(roll)
    pitch = tools.degree_to_radians(pitch)
    z = get_state.position(client)['z']
    z = world_to_airsim.distance(z)

    if yaw != 0:
        yaw = yaw + get_state.orientation(client)['yaw']
        yaw = tools.range_degrees(yaw, with_negative=False)
        return client.moveByVelocityZAsync(0, 0, z, 1, yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=yaw))
    else:
        return client.moveByRollPitchYawrateZAsync(roll, pitch, 0, z, 1)


def move_by(client: airsim.MultirotorClient, x, y, z) -> Future:
    """

    :param client:
    :param x:
    :param y:
    :param z:
    :return:
    """
    pos = get_state.position(client)
    ori = get_state.orientation(client)

    x, y, z = tools.relative_to_global(pos, ori['yaw'], x, y, z)

    x = world_to_airsim.distance(x)
    y = world_to_airsim.distance(y)
    z = world_to_airsim.distance(z)

    return client.moveToPositionAsync(x, y, z, world_to_airsim.distance(1))


def move_roll_pitch_yaw_rate_z(client: airsim.MultirotorClient, roll, pitch, yaw_rate, z, time: float = 1) -> Future:
    """
    Move by real-world roll pitch yaw-rate z.

    :param client: The multirotor client.
    :param roll: roll in real-world (degrees).
    :param pitch: pitch in rea-world (degrees).
    :param yaw_rate: yaw-rate in real-world (degrees).
    :param z: z in real-world (meters).
    :param time: Time (in seconds) to execute this call.
    :return: what client.moveByRollPitchYawrateZAsync returns.
    """
    return client.moveByRollPitchYawrateZAsync(world_to_airsim.angle(roll), world_to_airsim.angle(pitch),
                                               world_to_airsim.angle(yaw_rate), world_to_airsim.distance(z), time)
