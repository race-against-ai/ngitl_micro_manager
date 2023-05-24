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

from PySide6.QtCore import QObject, Signal, Property, QCoreApplication, Slot
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog


def run_process(process_name: str, path, file: str) -> subprocess.Popen:
    """Run the wanted executable and set its delay after startup"""
    print(f'Starting Process: {process_name}')

    process = subprocess.Popen(f'{path}\\{file}',
                               cwd=path,
                               creationflags=subprocess.CREATE_NEW_CONSOLE)

    return process


class TaskModel(QObject):
    """TaskModel Class for Qt, the button functions are nested here """
    state_color_changed = Signal()
    switch_state_changed = Signal()
    # autostart_state_changed = Signal()

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
        self.config_file = task['config_file']
        self.config_location = task['config_direction']

        # check if the executable is currently running
        self.process = None

        self.open_log_request.connect(self.handle_open_log_request)
        self.open_config_request.connect(self.handle_open_config_request)
        self.run_exe_request.connect(self.handle_run_exe_request)
        self.close_exe_request.connect(self.handle_close_exe_request)
        self.kill_exe_request.connect(self.handle_kill_exe_request)

    def handle_open_config_request(self):
        print(f"Task: {self.name} - open config requested")
        if self.config_file != 'None':
            filepath = self.config_file
            if self.config_location != "Directory":
                filepath = f'{self.config_location}/{self.config_file}'

            if os.path.exists(filepath):
                if platform.system() == 'Darwin':  # macOS
                    subprocess.call(('open', filepath))
                elif platform.system() == 'Windows':  # Windows
                    os.startfile(filepath)
                else:  # Linux
                    subprocess.call(('xdg-open', filepath))

            else:
                print("Config File not Found")

        else:
            print("Task has no Config File Configured")

    def handle_open_log_request(self):
        print(f'Task: {self.name} - open log requested with Log Level "{self.log_level}"')
        # under filepath we can change the file that is supposed to open
        filepath = "example.jpg"

        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(filepath)
        else:  # Linux
            subprocess.call(('xdg-open', filepath))

    def handle_run_exe_request(self):
        if self.executable == "None":
            print(f"No Executable set for Task: {self.name}")

        elif self.process is None:
            print(f'Task: {self.name} - open exe requested')
            self.run_process()

    def handle_close_exe_request(self):
        if self.executable != "None":
            print(f'Task: {self.name} - close exe requested')
            self.terminate_process()

    def handle_kill_exe_request(self):
        if self.executable != "None":
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

    @Property(bool, notify=switch_state_changed)
    def switch_state(self):
        return self._switch_state

    # @Property("QVariantBool", notify=autostart_state_changed)
    # def state_color(self):
    #     return self.autostart

    def set_state_color(self, value):
        self._state_color = value
        self.state_color_changed.emit()

    def set_switch_stage(self, value: bool):
        self._switch_state = value
        # print(self._switch_state)
        self.switch_state_changed.emit()

    def run_process(self) -> None:
        """Run the wanted executable and set its delay after startup"""

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
    create_json_request = Signal(str, list, str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.theme_change_request.connect(self.handle_theme_change_request)
        self.open_folder_request.connect(self.handle_open_folder_request)
        self.create_json_request.connect(self.handle_create_json)

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

    @staticmethod
    def handle_create_json(filepath, content, filename) -> None:
        """Exports give arguments from QML to a new Json file.
        filepath currently is useless as I couldn't figure out how to enable 'select Folder' mode for FileDialog with our
        QtQuick.Dialogs Version :("""
        filepath = "projects"
        print(f"creating json file in: {filepath}")
        # print(f'File is includes:"{content}"')
        export_list = []
        for task in content[1]["tasks"]:
            # Formatting the list to not be alphabetically sorted
            task_dict = {
                "name": task["name"],
                "executable": task["executable"],
                "working_directory": task["working_directory"],
                "delay": task["delay"],
                "config_file": task["config_file"],
                "config_direction": task["config_dir"],
                "log_level": task["log_level"],
                "autostart": task["autostart"]
            }
            export_list.append(task_dict)
        finished_dict = {"title": content[0]["title"], "tasks": export_list}
        # print(f"finished list is:"
        #       f"{finished_list}")
        file = json.dumps(finished_dict, indent=4)
        filename = filename.strip().replace(" ", "_").lower()
        extension = ".json"
        # small check so there isn't a prokect.json.json ;)
        if filename[-5:] == extension:
            filename = filename[:-5]

        new_filename = filename+extension
        # A Check to ensure that other projects aren't being overwritten
        counter = 1
        while os.path.exists(filepath+"/"+new_filename):
            new_filename = f'{filename}_{counter}{extension}'
            counter += 1

        # I couldn't figure out how to select only a folder in QML, so this is a workaround :(
        with open(f"{filepath}/{new_filename}", 'w') as f:
            f.write(file)
            print(f'File save as: {new_filename}')


class ProjectModel(QObject):
    task_list_changed = Signal(name="task_list_changed")
    project_title_changed = Signal(name="project_title_changed")

    start_all_tasks_request = Signal(name="start_all_tasks_request")
    stop_all_tasks_request = Signal(name="stop_all_tasks_request")
    download_request = Signal(name="download_request")

    # project_change_request = Signal(name="project_change_request")
    project_change_request = Signal(str, name="project_change_request")

    def __init__(self, parent=None):
        super().__init__(parent)
        self._project_title = "Micro Manager"
        self._task_list: List[TaskModel] = []
        self.start_all_tasks_request.connect(self.handle_start_all_tasks_request)
        self.stop_all_tasks_request.connect(self.handle_stop_all_tasks_request)
        self.download_request.connect(self.handle_download_request)
        self.project_change_request.connect(self.handle_project_change_request)

    def handle_start_all_tasks_request(self) -> None:
        for task in self.task_list:
            if task.autostart and not task.process and task.executable != "None":
                task.run_process()
                print(f'Task {task.name}: Pausing for {task.delay}s')
                time.sleep(int(task.delay))

    def handle_stop_all_tasks_request(self) -> None:
        for task in self._task_list:
            # print(task.name)
            if task.process:
                task.kill_process()

    def handle_download_request(self) -> None:
        print("download request received")

    @Property("QVariantList", notify=task_list_changed)
    def task_list(self):
        return self._task_list

    @Property("QVariant", notify=project_title_changed)
    def project_title(self):
        return self._project_title

    def append_tasks(self, tasks: []):
        """Shown tasks are getting appended here"""
        for task in tasks:
            self._task_list.append(task)
        self.task_list_changed.emit()

    def handle_project_change_request(self, file):
        print("Changing Project")
        self.handle_stop_all_tasks_request()
        self._task_list.clear()

        with open(file) as f:
            project = json.load(f)

            if "title" in project:
                new_title = project["title"]
                self._project_title = new_title
                self.project_title_changed.emit()

            temp_list = []
            tasks = project["tasks"]
            for entry in tasks:
                temp_list.append(TaskModel(entry))

        self.append_tasks(temp_list)
