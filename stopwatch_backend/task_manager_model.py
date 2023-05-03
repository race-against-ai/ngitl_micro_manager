""""
Copyright (C) 2023 twyleg, PhilippTrashman
"""
import os
import platform
import subprocess
# from task import Task
import time
from typing import List

from PySide6.QtCore import QObject, Signal, Property


def run_process(process_name: str, path: str, file: str, delay: float) -> subprocess.Popen:
    """Run the wanted executable and set its delay after startup"""
    print(f'Starting Process {process_name}')

    process = subprocess.Popen(file,
                               cwd=path,
                               creationflags=subprocess.CREATE_NEW_CONSOLE)

    if delay > 0:
        print(f'Pausing for {delay} seconds')
        time.sleep(delay)

    return process


class TaskModel(QObject):
    """TaskModel Class for Qt, currently the button functions are nested here :( """
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
        filepath = "settings.json"

        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(filepath)
        else:  # Linux
            subprocess.call(('xdg-open', filepath))

    def handle_open_log_request(self):
        print(f'Task: {self.name} - open log requested with Log Level "{self.log_level}"')
        filepath = "example.jpg"

        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(filepath)
        else:  # Linux
            subprocess.call(('xdg-open', filepath))

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

        self.process = run_process(self._name,
                                   r"C:\Users\VW2SMDW\Repos\ngitl_micro_manager\stopwatch_backend",
                                   "python while_true.py",
                                   0)

        # following code snippet is used when wanting to read out the executable from the settings.json...
        # currently commented out because we haven't implemented the bin folder format

        # self.process = run_process(self.name, self.path, self.executable, self.delay)

    def terminate_process(self) -> None:
        if self.process is not None:
            print(f'Terminating {self.name}')
            self.process.terminate()
            self.process = None
        else:
            print(f"{self.name} is not running")

    def kill_process(self) -> None:
        if self.process is not None:
            print(f'Force Terminating {self.name}')
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
        else:
            print(f'Cannot kill {self.name}: not running')


class TaskManagerModel(QObject):
    project_changed = Signal(name="task_list_changed")
    settings_changed = Signal(name="settings_changed")

    def __init__(self, parent=None):
        super().__init__(parent)
        self._project = ProjectModel(self)
        self._settings = SettingsModel(self)

    @Property("QObject", notify=settings_changed)
    def settings(self):
        return self._settings

    @Property("QObject", notify=project_changed)
    def project(self):
        return self._project


class SettingsModel(QObject):

    theme_request = Signal(name="theme_change_requested")
    open_folder_request = Signal(name="open_folder_request")

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.theme_request.connect(self.handle_theme_change)
        self.open_folder_request.connect(self.handle_open_folder_request)

    def handle_theme_change(self) -> None:
        print("changing theme")

    def handle_open_folder_request(self) -> None:
        print("Opening Folder")


class ProjectModel(QObject):
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
