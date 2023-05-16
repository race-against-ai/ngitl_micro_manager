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

import tkinter as tk
from tkinter import filedialog

from PySide6.QtCore import QObject, Signal, Property, QCoreApplication
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog


def run_process(process_name: str, path, file: str) -> subprocess.Popen:
    """Run the wanted executable and set its delay after startup"""
    print(f'Starting Process: {process_name}')

    process = subprocess.Popen(f'{path}\\{file}',
                               cwd=path,
                               creationflags=subprocess.CREATE_NEW_CONSOLE)

    return process


class TaskModel(QObject):
    """TaskModel Class for Qt, currently the button functions are nested here :( """
    state_color_changed = Signal()
    switch_state_changed = Signal()

    name_changed = Signal(name="name_changed")

    open_log_request = Signal(name="open_log_request")
    open_config_request = Signal(name="open_config_request")
    run_exe_request = Signal(name="run_exe_request")
    close_exe_request = Signal(name='close_exe_request')
    kill_exe_request = Signal(name='kill_exe_request')

    def __init__(self, task: dict) -> None:
        QObject.__init__(self)
        self._name = task['name']

        self._state_color = 'red'
        self._switch_state = False

        self.autostart = task['autostart']

        self.path = task['working_directory']
        self.executable = task['executable']
        self.log_level = task['log_level']
        self.delay = task['delay']

        # check if the executable is currently running
        self.process = None

        self.open_log_request.connect(self.handle_open_log_request)
        self.open_config_request.connect(self.handle_open_config_request)
        self.run_exe_request.connect(self.handle_run_exe_request)
        self.close_exe_request.connect(self.handle_close_exe_request)
        self.kill_exe_request.connect(self.handle_kill_exe_request)

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

    def handle_kill_exe_request(self):
        print(f'Task: {self.name} - kill exe requested')
        self.kill_process()

    @Property("QString", notify=name_changed)
    def name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name
        self.name_changed.emit()

    @Property(str, notify=state_color_changed)
    def state_color(self):
        return self._state_color

    @Property(str, notify=switch_state_changed)
    def switch_state(self):
        return self._switch_state

    def set_state_color(self, value):
        self._state_color = value
        self.state_color_changed.emit()

        qml_task_object = self.findChild(QObject, "qml_task_object")

        if qml_task_object is not None:
            qml_task_object.setProperty("state_color", value)

    def set_switch_stage(self, value: bool):
        self._switch_state = value
        self.switch_state_changed.emit()

        qml_task_object = self.findChild(QObject, "qml_task_object")

        if qml_task_object is not None:
            qml_task_object.setProperty("switch_state", value)

    def run_process(self) -> None:
        """Run the wanted executable and set its delay after startup"""

        # self.process = subprocess.Popen("python while_true.py",
        #                                 cwd=Path(__file__).parent,
        #                                 creationflags=subprocess.CREATE_NEW_CONSOLE)

        # following code snippet is used when wanting to read out the executable from the settings.json...
        # currently commented out because we haven't implemented the bin folder format
        self.process = run_process(self.name, self.path, self.executable)

        self.set_state_color("green")
        self.set_switch_stage(True)

    def terminate_process(self) -> None:
        if self.process is not None:
            print(f'Terminating {self.name}')
            self.process.terminate()
            self.process = None
            self.set_state_color("red")
            self.set_switch_stage(False)

        else:
            print(f"{self.name} is not running")

    def kill_process(self) -> None:
        if self.process is not None:
            print(f'Force Terminating {self.name}')
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
            self.process = None

            self.set_state_color("red")
            self.set_switch_stage(False)

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
    file_path_request = Signal(object, name="file_path_request")

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.theme_change_request.connect(self.handle_theme_change_request)
        self.open_folder_request.connect(self.handle_open_folder_request)
        self.project_change_request.connect(self.handle_project_change_request)
        self.file_path_request.connect(self.handle_file_path_request)

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

    def handle_file_path_request(self, index) -> None:
        """Opens a file locator through Tkinter... I couldn't figure out how to do it through QML :("""
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()
        result = [index, file_path]
        # print(file_path)
        self.file_path_request.emit(result)

        root.destroy()

    # def handle_project_creator_request(self, title, name_list, task_list, delay_list) -> None:
    #     print("New Project Creator Requested")
    #     creator = ConfigFileCreator(title)


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

    def handle_stop_all_tasks_request(self) -> None:
        for task in self.task_list:
            # print(task.name)
            if task.process:
                task.kill_process()

    def handle_download_request(self) -> None:
        print("download request received")

    @Property("QVariantList", notify=task_list_changed)
    def task_list(self):
        return self._task_list

    def append_tasks(self, tasks: []):
        for task in tasks:
            self._task_list.append(task.task_model)
        self.task_list_changed.emit()


class ConfigFileCreator:
    """
    A Json File Creator for a new Project, for creating enter a Project name,
    then call the append_task for appending a task to the project.

    Finally, you need to export the file with a filename and directory.
    The Config file is meant to then be readable by the MicroManager later on
    """

    def __init__(self, title):
        self._config_file = {}
        self._task_list = []

    def append_task(self, name, autostart, file_path, delay, working_dir, config_file, log_level):
        print(f'adding task: {name}'
              f'to the Task Dictionary ')
        task_dict = {
            "name": name,
            "autostart": autostart,
            "executable": file_path,
            "delay": delay,
            "working_directory": working_dir,
            "config_file": config_file,
            "log_level": log_level
        }
        self._task_list.append(task_dict)

    def export_config(self, filename, file_path):
        print(f"exporting config {filename} to {file_path}")
        self._config_file["title"] = self.title
        self._config_file["tasks"] = self._task_list
