""""
Copyright (C) 2023 twyleg, PhilippTrashman
"""
import os
import platform
import subprocess
import json
import time
from pathlib import Path
from typing import List

from PySide6.QtCore import QObject, Signal, Property, QCoreApplication
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog


def run_process(process_name: str, path: Path, file: str, delay: float) -> subprocess.Popen:
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
    state_color_changed = Signal()
    stateChanged = Signal(bool)

    name_changed = Signal(name="name_changed")

    open_log_request = Signal(name="open_log_request")
    open_config_request = Signal(name="open_config_request")
    run_exe_request = Signal(name="run_exe_request")
    close_exe_request = Signal(name='close_exe_request')

    def __init__(self, task: dict) -> None:
        QObject.__init__(self)
        self._name = task['name']

        self._state_color = 'red'
        self._state = False

        self.autostart = task['autostart']

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
        if self.process is None:
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

    @Property(str, notify=state_color_changed)
    def state_color(self):
        return self._state_color

    def set_state_color(self, value):
        self._state_color = value
        self.state_color_changed.emit()

        # Get the QML object of the Task
        qml_task_object = self.findChild(QObject, "qml_task_object")

        # Set the state_color property of the QML object
        if qml_task_object is not None:
            qml_task_object.setProperty("state_color", value)

    def run_process(self) -> None:
        """Run the wanted executable and set its delay after startup"""

        self.process = run_process(self._name,
                                   Path(__file__).parent,
                                   "python while_true.py",
                                   0)

        # following code snippet is used when wanting to read out the executable from the settings.json...
        # currently commented out because we haven't implemented the bin folder format

        # self.process = run_process(self.name, self.path, self.executable, self.delay)

        self.set_state_color("green")

    def terminate_process(self) -> None:
        if self.process is not None:
            print(f'Terminating {self.name}')
            self.process.terminate()
            self.process = None
            self.set_state_color("red")

        else:
            print(f"{self.name} is not running")


    def kill_process(self) -> None:
        if self.process is not None:
            print(f'Force Terminating {self.name}')
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
            self.set_state_color("red")

        else:
            print(f'Cannot kill {self.name}: not running')



class TaskManagerModel(QObject):
    project_changed = Signal(name="task_list_changed")
    settings_changed = Signal(name="settings_changed")

    def __init__(self, parent=None):
        super().__init__(parent)
        self._project = ProjectModel(self)
        self._settings = SettingsModel(self)

    @Property("QVariant", notify=settings_changed)
    def settings(self):
        return self._settings

    @Property("QVariant", notify=project_changed)
    def project(self):
        return self._project


class SettingsModel(QObject):

    theme_change_request = Signal(name="theme_change_request")
    open_folder_request = Signal(name="open_folder_request")
    project_change_request = Signal(name="project_change_request")

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.theme_change_request.connect(self.handle_theme_change_request)
        self.open_folder_request.connect(self.handle_open_folder_request)
        self.project_change_request.connect(self.handle_project_change_request)

        self.project = None

        self.current_path = Path(__file__).parent

    def handle_theme_change_request(self) -> None:
        print("changing theme")
        if not self.project:
            print("--! standard settings")
            with open('settings.json') as f:
                file = json.load(f)
        else:
            print("--! project settings")

        print(file["theme"])

    def handle_open_folder_request(self) -> None:
        print("Opening Folder")
        subprocess.Popen(f'explorer "{self.current_path}"')

    def handle_project_change_request(self) -> None:
        print("Changing Project")
        current_dir = os.getcwd()
        # try:
        #     self.project = QFileDialog.getOpenFileName(None, "Open Project Json file", current_dir, "JSON Files (*.json)")
        #
        #     # if self.project:
        #     #     print(f'Selected file: {self.project}')
        #
        # except Exception as e:
        #     print(f'Error opening file dialog: {e}')


class ProjectModel(QObject):
    task_list_changed = Signal(name="task_list_changed")

    start_all_tasks_request = Signal(name="start_all_tasks_request")
    stop_all_tasks_request = Signal(name="stop_all_tasks_request")
    download_request = Signal(name="download_request")

    def __init__(self, parent=None):
        super().__init__(parent)
        self._task_list: List[TaskModel] = []
        self.start_all_tasks_request.connect(self.handle_start_all_tasks_request)
        self.stop_all_tasks_request.connect(self.handle_stop_all_tasks_request)
        self.download_request.connect(self.handle_download_request)

    def handle_start_all_tasks_request(self) -> None:

        for task in self.task_list:
            # print(task.name)

            if task.autostart and not task.process:

                task.run_process()
                print(f'Task {task.name}: Pausing for {task.delay}s')
                time.sleep(task.delay)
                task.stateChanged.emit(True)

    def handle_stop_all_tasks_request(self) -> None:
        for task in self.task_list:
            # print(task.name)
            if task.process:
                task.terminate_process()
                task.stateChanged.emit(False)
                print(f'{task.stateChanged}, on {task.name}')

    def handle_download_request(self) -> None:
        print("download request received")

    @Property("QVariantList", notify=task_list_changed)
    def task_list(self):
        return self._task_list

    def append_tasks(self, tasks: []):
        for task in tasks:
            self._task_list.append(task.task_model)
        self.task_list_changed.emit()
