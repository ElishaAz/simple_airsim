from threading import Thread

import PySimpleGUI as sg

from typing import Iterable

from . import coordinate_system
from .manager import Manager

try:
    from .virtual_controller import VirtualController
except ImportError:
    print("To use VirtualController install vJoy.")


class GUIManager:
    run: bool
    _event_thread: Thread
    _update_thread: Thread

    algo_info: str

    # noinspection PyTypeChecker
    def __init__(self, manager: Manager, label_x: int, value_x, y: int, decimal_point: int,
                 algo_info_rows: int = 3, use_virtual_controller: bool = False,
                 main_font=('Helvitica', 15), title_font=('Helvitica', 25, 'bold'), algo_info_font=('Helvitica', 15)):
        """

        """
        sg.SetOptions(font=main_font)
        sg.theme('Dark Green 3')

        self.run = True
        self.manager = manager

        # self.data_precision = data_precision
        self.format_str = F"%{value_x - decimal_point - 1}.{decimal_point}f"

        self.main_layout = [
            [sg.Text('Algorithm Controls:', font=title_font)],
            [
                # sg.Text("\t"),
                sg.Button("Start", key='-ALGO_START-'),
                sg.Button("Pause", key='-ALGO_PAUSE-'), sg.Button("Resume", key='-ALGO_RESUME-'),
                sg.Button("Stop", key='-ALGO_TERM-'), sg.Text(size=(15, 1), key='-ALGO_STATE-'),
                sg.Radio("Algorithm Mode", "-MODE-", key='-ALGO_MODE-', enable_events=True, default=True),
                sg.Radio("Manual Mode", "-MODE-", key='-MANUAL_MODE-', enable_events=True, default=False)
            ],

            [sg.Text('Information:', font=title_font)],
            [sg.Text(size=(label_x, y), key='-TEL-'), sg.Text(size=(value_x, y), key='-TEL_VAL-'),
             sg.Text(size=(label_x, y), key='-VEL-'), sg.Text(size=(value_x, y), key='-VEL_VAL-'),
             sg.Text(size=(label_x, y), key='-LID-'), sg.Text(size=(value_x, y), key='-LID_VAL-')],
            [sg.Text('Algorithm Information:', font=title_font)],
            [sg.Text(size=(int(((label_x + value_x) * 3 + 5) / main_font[1] * algo_info_font[1]), algo_info_rows),
                     key='-ALGO_INFO-', font=algo_info_font)]
        ]

        self._init_windows()

        self.use_virtual_controller = use_virtual_controller
        self._enter_called = False

        if self.use_virtual_controller:
            self.controller = VirtualController()

        self.manual_algo_running = False
        self.algo_info = ""

    # noinspection PyTypeChecker
    def _init_windows(self):
        self.main_window: sg.Window = sg.Window("Main Controls", self.main_layout, icon='../images/logo.ico',
                                                finalize=True, use_default_focus=False)

        self.main_window['-TEL-'].update(
            'Telemetry:\n' +
            ':\n'.join(self.manager.get_position().keys()) +
            ':\n\n' + ':\n'.join(self.manager.get_orientation().keys()))

        self.main_window['-VEL-'].update(
            'Velocity:\n' +
            ':\n'.join(self.manager.get_velocity().keys()))

        self.main_window['-LID-'].update(
            'Lidars:\n' +
            ':\n'.join(self.manager.get_lidars().keys()))

    def start(self):
        if not self._enter_called:
            raise Exception(
                """
                GUIManager should be initialized using context (i.e. using the 'with' keyword).
                E.g.:
                    with Manager(...) as man:
                        with GUIManager(man,...) as gui:
                            gui.start()
                """)

        self._event_thread = Thread(target=self._event_loop)
        # self._update_thread = Thread(target=self._update_loop)

        # self._update_thread.start()

        self._event_thread.run()

    def set_algo_info(self, info: str):
        """
        Sets the string that will be displayed as the algorithm information.
        Info can be multiline, but you have to set a big enough 'algo_info_y' for that.
        :param info: The string to display.
        :return:
        """
        self.algo_info = info

    # # noinspection PyTypeChecker
    # def _update_loop(self):
    #     while self.run:
    #         self.main_window['-TEL_VAL-'].update(
    #             '\n' + '\n'.join(self._format_str(self.manager.get_position().values())) +
    #             '\n\n' + '\n'.join(self._format_str(self.manager.get_orientation().values())))
    #
    #         self.main_window['-VEL_VAL-'].update(
    #             '\n' + '\n'.join(self._format_str(self.manager.get_velocity().values())))
    #
    #         self.main_window['-LID_VAL-'].update(
    #             '\n' + '\n'.join(self._format_str(self.manager.get_lidars().values())))
    #
    #         self.main_window['-ALGO_STATE-'].update("State: " + self.manager.get_algo_state())
    #
    #         time.sleep(0.05)

    def _format_str(self, a: Iterable):
        """

        :param set:
        :return:
        """
        return (((self.format_str % x) if x is not None else 'None') for x in a)
        # return (F"{None if x is None else round(x, self.data_precision)}" for x in a)

    # noinspection PyTypeChecker
    def _event_loop(self):
        while self.run:
            event, values = self.main_window.Read(timeout=100)

            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Quit' or str(event) == 'None':
                self.run = False
                self.manager.terminate_algo()
                break

            if event == '-ALGO_START-':
                self.manager.start_algo()
            if event == '-ALGO_PAUSE-':
                self.manager.pause_algo()
            if event == '-ALGO_RESUME-':
                self.manager.resume_algo()
            if event == '-ALGO_TERM-':
                self.manager.terminate_algo()

            if event == '-ALGO_MODE-':
                self.manager.get_airsim_client().enableApiControl(True)
                if self.manual_algo_running:
                    self.manager.resume_algo()

            if event == '-MANUAL_MODE-':
                self.manager.get_airsim_client().enableApiControl(False)
                self.manual_algo_running = self.manager.get_algo_state() == 'running'
                if self.manual_algo_running:
                    self.manager.pause_algo()

            # Update text
            self.main_window['-TEL_VAL-'].update(
                '\n' + '\n'.join(self._format_str(self.manager.get_position().values())) +
                '\n\n' + '\n'.join(self._format_str(self.manager.get_orientation().values())))

            self.main_window['-VEL_VAL-'].update(
                '\n' + '\n'.join(self._format_str(self.manager.get_velocity().values())))

            self.main_window['-LID_VAL-'].update(
                '\n' + '\n'.join(self._format_str(self.manager.get_lidars().values())))

            self.main_window['-ALGO_STATE-'].update("State: " + self.manager.get_algo_state())

            self.main_window['-ALGO_INFO-'].update(self.algo_info)

        # self._update_thread.join()

        # Finish up by removing from the screen
        self.main_window.close()

    def __enter__(self) -> "GUIManager":
        """

        :return:
        """
        self._enter_called = True

        if self.use_virtual_controller:
            self.controller.__enter__()
            self.controller.enable()
        return self

    def __exit__(self, *args):
        """

        :param args:
        :return:
        """
        if self.use_virtual_controller:
            self.controller.disable()
            self.controller.__exit__(*args)

        # self.manager.terminate_algo()


if __name__ == '__main__':
    with Manager(coordinate_system.AIRSIM) as man:
        with GUIManager(man, 10, 10, 10, 3) as gui:
            gui.start()
