""""
Copyright (C) 2023 twyleg, PhilippTrashman
"""

from stopwatch_backend.task_manager_model import TaskModel
from PySide6.QtCore import QObject, Signal, Property, Slot
import subprocess
import time


class Task(QObject):
    def __init__(self, task: dict):
        QObject.__init__(self)
        self.name = task['name']
        self.task_model = TaskModel(task)
        self.path = r'/bin'
        self.executable = task['executable']
        self.log_level = task['log_level']
        self.delay = task['delay']

        self.task_model.open_log_request.connect(self.handle_open_log_request)
        self.task_model.open_config_request.connect(self.handle_open_config_request)
        self.task_model.run_exe_request.connect(self.handle_exe_request)
        self.task_model.close_exe_request.connect(self.handle_exe_close_request)

        self.process = None

        # from the config file, checks if autostart is enabled for this task
        self.autostart = task['enabled']

        # Flag to check if the Executable is running or not
        self.status = False

    def handle_open_log_request(self) -> None:
        print(f'Task: {self.name} - open log requested')

    @Slot()
    def handle_open_config_request(self) -> None:
        print(f'Task: {self.name} - open config requested')

    def handle_exe_request(self) -> None:
        print(f'Task: {self.name} - open exe requested')
        self.run_process()

    def handle_exe_close_request(self) -> None:
        print(f'Task: {self.name} - close exe requested')
        self.terminate_process()

    def run_process(self) -> None:
        """Run the wanted executable and set its delay after startup"""
        print(f'Starting Process {self.name}')
        # self.process = subprocess.Popen(rf'{self.path}\{self.executable}',
        #                                 cwd=self.path,
        #                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
        #                                 # stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #
        print(f'Pausing for {self.delay} seconds')
        time.sleep(self.delay)

    def terminate_process(self) -> None:
        print(f'Terminating {self.name}')
