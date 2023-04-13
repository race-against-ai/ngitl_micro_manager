""""
Copyright (C) 2022 twyleg
"""
from typing import List

from PySide6.QtCore import QObject, Signal, Property
# from task import Task
import time
import subprocess
import os


class TaskModel(QObject):
    name_changed = Signal(name="name_changed")

    open_log_request = Signal(name="open_log_request")
    open_config_request = Signal(name="open_config_request")
    run_exe_request = Signal(name="run_exe_request")
    close_exe_request = Signal(name='close_exe_request')

    def __init__(self, task: dict) -> None:
        QObject.__init__(self)
        self._name = task['name']

        self.path = r'/bin'
        self.executable = task['executable']
        self.log_level = task['log_level']
        self.delay = task['delay']

        # check if the executable is currently running
        self.process = None

        self.open_log_request.connect(self.handle_open_log_request)
        self.open_config_request.connect(self.handle_open_config_request)
        self.run_exe_request.connect(self.handle_run_exe_request)
        self.close_exe_request.connect(self.handle_close_exe_request)

    def handle_open_config_request(self):
        print(f"Task: {self.name} - open config requested")

    def handle_open_log_request(self):
        print(f'Task: {self.name} - open log requested with Log Level "{self.log_level}"')

    def handle_run_exe_request(self):
        print(f'Task: {self.name} - open exe requested')
        self.run_process()

    def handle_close_exe_request(self):
        print(f'Task: {self.name} - close exe requested')
        self.terminate_process()

    @Property("QString", notify=name_changed)
    def name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name
        self.name_changed.emit()

    def run_process(self) -> None:
        """Run the wanted executable and set its delay after startup"""
        print(f'Starting Process {self.name}')
        image_path = "example.jpg"

        self.process = subprocess.Popen(f"python while_true.py",
                         cwd=r"C:\Users\VW2SMDW\Repos\ngitl_micro_manager\stopwatch_backend",
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
        # self.process = subprocess.Popen(rf'{self.path}\{self.executable}',
        #                                 cwd=self.path,
        #                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
        #                                 # stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #
        print(f'Pausing for {self.delay} seconds')
        time.sleep(self.delay)

    def terminate_process(self) -> None:
        if self.process is not None:
            print(f'Terminating {self.name}')
            self.process.terminate()
            self.process = None
        else:
            print(f"Executable isn't running")


class TaskManagerModel(QObject):
    task_list_changed = Signal(name="task_list_changed")

    def __init__(self, parent=None):
        super().__init__(parent)
        self._task_list: List[TaskModel] = []

    @Property("QVariantList", notify=task_list_changed)
    def task_list(self):
        return self._task_list

    def append_tasks(self, tasks: []):
        for task in tasks:
            self._task_list.append(task.task_model)
        self.task_list_changed.emit()
