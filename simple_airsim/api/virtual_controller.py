import warnings

PYVJOY_IMPORT_SUCCESSFUL = False
PYNPUT_IMPORT_SUCCESSFUL = False

try:
    import pyvjoy

    PYVJOY_IMPORT_SUCCESSFUL = True
    from pynput.keyboard import Key, Listener

    PYNPUT_IMPORT_SUCCESSFUL = True
except ModuleNotFoundError:
    warnings.warn(F"Not all virtual_controller modules were imported correctly."
                  F" pyvjoy: {PYVJOY_IMPORT_SUCCESSFUL}. pynput: {PYNPUT_IMPORT_SUCCESSFUL}"
                  F"\nPlease install the modules to use virtual_controller.")

VJOY_INSTALLED = True


def vjoy_accessible():
    global VJOY_INSTALLED, PYVJOY_IMPORT_SUCCESSFUL
    return VJOY_INSTALLED and PYVJOY_IMPORT_SUCCESSFUL


def pynput_vjoy_accessible():
    global PYNPUT_IMPORT_SUCCESSFUL
    return PYNPUT_IMPORT_SUCCESSFUL and vjoy_accessible()


VJOY_VALUE = 1


class VirtualController:
    run_listeners: bool
    listener_closed: bool

    def __init__(self, fix_airsim: bool = True, keyboard_listeners: bool = True):
        """

        """
        self.listener_thread = None
        global VJOY_INSTALLED
        self.keyboard_listeners = keyboard_listeners
        if not vjoy_accessible():
            return
        self.fix_airsim = fix_airsim
        try:
            self.j = pyvjoy.VJoyDevice(1)
            VJOY_INSTALLED = True
        except pyvjoy.vJoyException:
            VJOY_INSTALLED = False
        self.run_listeners = keyboard_listeners
        self.listener_closed = False

        self.listener_active = False
        self.listener: Listener = Listener(
            on_press=self.on_press,
            on_release=self.on_release)

    def on_press(self, key):
        if not self.listener_active:
            return

        if str(key) == 'Key.right':
            self.move_right(VJOY_VALUE)
        if str(key) == 'Key.left':
            self.move_right(-VJOY_VALUE)
        if str(key) == 'Key.up':
            self.move_forward(VJOY_VALUE)
        if str(key) == 'Key.down':
            self.move_forward(-VJOY_VALUE)

        if str(key) == "'d'":
            self.clockwise(VJOY_VALUE)
        if str(key) == "'a'":
            self.clockwise(-VJOY_VALUE)
        if str(key) == "'w'":
            self.throttle(VJOY_VALUE)
        if str(key) == "'s'":
            self.throttle(-VJOY_VALUE)

        if not self.run_listeners:
            self.reset()
            return False

    def on_release(self, key):
        if not self.listener_active:
            return

        if str(key) == 'Key.right' or str(key) == 'Key.left':
            self.move_right(0)
        if str(key) == 'Key.up' or str(key) == 'Key.down':
            self.move_forward(0)

        if str(key) == "'d'" or str(key) == "'a'":
            self.clockwise(0)
        if str(key) == "'w'" or str(key) == "'s'":
            self.throttle(0)

        if key == Key.esc:
            self.reset()
            # Stop listener
            return False

        if not self.run_listeners:
            self.reset()
            return False

    def enable(self):
        """

        :return:
        """
        if not pynput_vjoy_accessible():
            return

        self.listener_active = True

    def disable(self):
        """

        :return:
        """
        if not pynput_vjoy_accessible():
            return

        self.listener_active = False

        self.reset()

    def throttle(self, val: float):
        """

        :param val: between -1 and 1
        :return:
        """
        if not vjoy_accessible():
            return
        try:
            if self.fix_airsim:
                self.j.set_axis(pyvjoy.HID_USAGE_Y, self._get_val(-val))
            else:
                self.j.set_axis(pyvjoy.HID_USAGE_X, self._get_val(val))
        except pyvjoy.vJoyException:
            ""

    def clockwise(self, val: float):
        """

        :param val: between -1 and 1
        :return:
        """
        if not vjoy_accessible():
            return
        try:
            if self.fix_airsim:
                self.j.set_axis(pyvjoy.HID_USAGE_X, self._get_val(val))
            else:
                self.j.set_axis(pyvjoy.HID_USAGE_Y, self._get_val(val))
        except pyvjoy.vJoyException:
            ""

    def move_right(self, val: float):
        """

        :param val: between -1 and 1
        :return: wAxisVBRX
        """
        if not vjoy_accessible():
            return
        try:
            if self.fix_airsim:
                self.j.set_axis(pyvjoy.HID_USAGE_RX, self._get_val(val))
            else:
                self.j.set_axis(pyvjoy.HID_USAGE_RX, self._get_val(val))
        except pyvjoy.vJoyException:
            ""

    def move_forward(self, val: float):
        """

        :param val: between -1 and 1
        :return:
        """
        if not vjoy_accessible():
            return
        try:
            if self.fix_airsim:
                self.j.set_axis(pyvjoy.HID_USAGE_RY, self._get_val(-val))
            else:
                self.j.set_axis(pyvjoy.HID_USAGE_RY, self._get_val(val))
        except pyvjoy.vJoyException:
            ""

    def update(self):
        """

        :return:
        """
        if not vjoy_accessible():
            return
        # self.j.update()

    def reset(self):
        """

        :return:
        """
        if not vjoy_accessible():
            return

        self.move_forward(0)
        self.move_right(0)
        self.throttle(0)
        self.clockwise(0)

    @staticmethod
    def _get_val(val):
        return int(val * 0x4000) + 0x4000

    def __enter__(self) -> "VirtualController":
        """

        :return:
        """
        self.listener.start()
        return self

    def __exit__(self, *args):
        """

        :param args:
        :return:
        """
        self.listener.stop()


if __name__ == "__main__":
    cont = VirtualController()
    cont.enable()
    input()
    cont.disable()
    cont.throttle(1)
    cont.clockwise(1)
    cont.move_right(1)
    cont.move_forward(1)
    input()
    cont.throttle(-1)
    cont.clockwise(-1)
    cont.move_right(-1)
    cont.move_forward(-1)
    input()
