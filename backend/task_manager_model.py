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
import uuid
import concurrent.futures
from functools import partial
import threading

from PySide6.QtCore import QObject, Signal, Property, QTimer


MAX_THREAD_COUNT = 1


def run_process(process_name: str, path: str, file: str) -> subprocess.Popen:
    """Run the wanted executable and set its delay after startup"""
    # print(f'Starting Process: {process_name}')
    if path == "Directory":
        work_dir = os.getcwd() + r'\bin'
        filepath = fr'{work_dir}\{file}'
        # print(filepath)
        # print(work_dir)

    else:
        filepath = fr'{path}\{file}'
        work_dir = path

    process = subprocess.Popen(filepath,
                               cwd=work_dir,
                               creationflags=subprocess.CREATE_NEW_CONSOLE)

    return process


class TaskModel(QObject):
    """TaskModel Class for Qt, the button functions are nested here """
    state_color_changed = Signal()
    switch_state_changed = Signal()

    autostart_state_request = Signal(bool, name='autostart_state_request')
    name_changed = Signal(name="name_changed")

    open_log_request = Signal(name="open_log_request")
    open_config_request = Signal(name="open_config_request")
    # run_exe_request = Signal(name="run_exe_request")
    run_exe_request = Signal(str)
    close_exe_request = Signal(name='close_exe_request')
    kill_exe_request = Signal(name='kill_exe_request')
    switch_state_request = Signal(name="switch_state_request")

    def __init__(self, task: dict) -> None:
        QObject.__init__(self)
        self._name = task['name']
        self.id = task['id']
        self._state_color = 'red'
        self._switch_state = False

        self.request_start = False

        self.autostart = task['autostart']
        self.path = task['working_directory']
        self.executable = task['executable']
        self.log_level = task['log_level']
        self.delay = task['delay']
        self.config_file = task['config_file']
        self.config_location = task['config_direction']

        # check if the executable is currently running
        self.process = None
        # A QTimer checking to see if the process is still running
        self.process_check_timer = QTimer(self)
        self.process_check_timer.timeout.connect(self.check_process_status)
        self.process_check_timer.start(500)

        # Connect functions to requests
        self.open_log_request.connect(self.handle_open_log_request)
        self.open_config_request.connect(self.handle_open_config_request)
        # self.run_exe_request.connect(self.handle_run_exe_request)
        self.close_exe_request.connect(self.handle_close_exe_request)
        self.kill_exe_request.connect(self.handle_kill_exe_request)
        self.autostart_state_request.connect(self.autostart_setter)
        self.switch_state_request.connect(self.handle_switch_state_request)

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
        # print(f'Task: {self.name} - open log requested with Log Level "{self.log_level}"')
        # under filepath we can change the file that is supposed to open
        # only reason it doesn't open an actual log file is because i don't know how to create one...
        filepath = "settings.json"

        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(filepath)
        else:  # Linux
            subprocess.call(('xdg-open', filepath))

    def check_process_status(self):
        if self.process is not None and self.process.poll() is not None:
            print(f'Process {self.name} has been closed.')
            self.process = None
            self.set_state_color("red")
            self.set_switch_stage(False)
            self.process_check_timer.stop()

    def handle_run_exe_request(self):
        if self.executable == "None":
            print(f"No Executable set for Task: {self.name}")

        elif self.process is None:
            # print(f'Task: {self.name} - open exe requested')
            self.run_process()


    def handle_close_exe_request(self):
        if self.executable != "None":
            print(f'Task: {self.name} - close exe requested')
            self.terminate_process()

    def handle_kill_exe_request(self):
        if self.executable != "None":
            print(f'Task: {self.name} - kill exe requested')
            self.kill_process()

    def handle_switch_state_request(self):
        # print("switch changed")
        self.run_process()

    @Property("QString", notify=name_changed)
    def name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name
        self.name_changed.emit()

    @Property(str, notify=state_color_changed)
    def state_color(self) -> str:
        return self._state_color

    @Property(bool, notify=switch_state_changed)
    def switch_state(self) -> bool:
        return self._switch_state

    @Property(bool)
    def autostart_state(self) -> bool:
        return self.autostart

    def autostart_setter(self, value):
        if self.autostart != value:
            self.autostart = value
            # self.autostart_state_changed.emit()

    def set_state_color(self, value) -> None:
        self._state_color = value
        self.state_color_changed.emit()

    def set_switch_stage(self, value: bool) -> None:
        self._switch_state = value
        self.switch_state_changed.emit()

    def run_process(self) -> None:
        """Run the wanted executable and set its delay after startup"""
        # self.process = run_process(self._name, self.path, self.executable)
        if not self.request_start:
            self.request_start = True
            self.run_exe_request.emit(self.id)

            # self.set_state_color("green")
            # self.set_switch_stage(True)
            # self.process_check_timer.start(500)

    def terminate_process(self) -> None:
        if self.process is not None:
            print(f'Terminating {self.name}')
            self.process.terminate()
            self.process = None
            self.set_state_color("red")
            self.set_switch_stage(False)

        # else:
        #     print(f"{self.name} is not running")

    def kill_process(self) -> None:
        if self.process is not None:
            print(f'Force Terminating {self.name}')
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
            self.process = None

            self.set_state_color("red")
            self.set_switch_stage(False)

        # else:
        #     print(f'Cannot kill {self.name}: not running')


class TaskBackend:
    def __init__(self, task_data: dict):
        print("")


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
    disable_save_dialog = Signal(name="disable_save_dialog")
    create_json_request = Signal(str, list, str)
    save_dialog_changed = Signal()
    filename_changed = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.theme_change_request.connect(self.handle_theme_change_request)
        self.open_folder_request.connect(self.handle_open_folder_request)
        self.create_json_request.connect(self.handle_create_json)
        self.disable_save_dialog.connect(self.handle_disable_save_dialog)

        self.project = None

        self._save_dialog = False
        self._file_name = "new_project.json"
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

    def handle_create_json(self, filepath, content, filename) -> None:
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
        file = json.dumps(finished_dict, indent=4)
        filename = filename.strip().replace(" ", "_").lower()
        extension = ".json"
        # small check so there isn't a project.json.json ;)
        if filename[-5:] == extension:
            filename = filename[:-5]

        new_filename = filename + extension
        # A Check to ensure that other projects aren't being overwritten
        counter = 1
        while os.path.exists(filepath + "/" + new_filename):
            new_filename = f'{filename}_{counter}{extension}'
            counter += 1

        # I couldn't figure out how to select only a folder in QML, so this is a workaround :(
        with open(f"{filepath}/{new_filename}", 'w') as f:
            f.write(file)
            print(f'File save as: {new_filename}')
        # print("hey now, im a rockstar get your game on")
        self._file_name = new_filename
        self._save_dialog = True
        self.filename_changed.emit()
        self.save_dialog_changed.emit()

    def handle_disable_save_dialog(self):
        self._save_dialog = False
        self.save_dialog_changed.emit()

    @Property(bool, notify=save_dialog_changed)
    def save_dialog(self) -> bool:
        return self._save_dialog

    @Property(str, notify=filename_changed)
    def file_name(self):
        return self._file_name


class ProjectModel(QObject):
    taskRunningChanged = Signal()
    task_list_changed = Signal(name="task_list_changed")
    project_title_changed = Signal(name="project_title_changed")

    start_all_tasks_request = Signal(name="start_all_tasks_request")
    # stop_all_tasks_request = Signal(name="stop_all_tasks_request")
    download_request = Signal(name="download_request")

    # project_change_request = Signal(name="project_change_request")
    project_change_request = Signal(str, name="project_change_request")

    def __init__(self, parent=None):
        super().__init__(parent)
        self._project_title = "Micro Manager"
        self._task_list: List[TaskModel] = []
        self._task_dict: dict[str, TaskModel] = {}
        self._child_dict: dict[str, dict] = {}

        # self._worker_thread = threading.Thread(target=self._child_worker)
        # self._worker_thread.start()
        # self._threads = []
        # self._subprocess_started = threading.Event()
        self._lock = threading.Lock()
        self._executor = concurrent.futures.ThreadPoolExecutor(2)

        self.start_all_tasks_request.connect(self.handle_start_all_tasks_request)
        # self.stop_all_tasks_request.connect(self.handle_stop_all_tasks_request)
        self.download_request.connect(self.handle_download_request)
        self.project_change_request.connect(self.handle_project_change_request)

        # flag responsible for the start all button
        self._task_running = False
        # Timer to check if any Task is running to set the Button
        self.task_check_timer = QTimer(self)
        self.task_check_timer.timeout.connect(self.check_task_status)
        self.task_check_timer.start(500)

    def delegate_task(self, child_id, name, path, executable):
        future = self._executor.submit(self._child_worker, child_id, name, path, executable)
        future.add_done_callback(partial(self._task_completed, child_id))

    def _child_worker(self, child_id, name, path, executable):
        sleep_timer = int(self._child_dict[child_id]['delay'])

        process = run_process(name, path, executable)
        time.sleep(sleep_timer)

        with self._lock:
            self._task_dict[child_id].process = process

    def _task_completed(self, child_id, future):
        self._task_dict[child_id].request_start = False
        self._task_dict[child_id].set_state_color("green")
        self._task_dict[child_id].set_switch_stage(True)
        pass

    def check_task_status(self):
        flag = False
        if self._task_list:
            for task in self._task_list:
                if task.process:
                    # self.set_task_running(True)
                    flag = True
                    break
                elif not task.process:
                    # self.set_task_running(False)
                    flag = False

            if self._task_running != flag:
                self.set_task_running(flag)

    def handle_start_all_tasks_request(self):
        if self._task_running:
            self.stop_all_tasks()
        else:
            self.start_all_tasks()

    def start_all_tasks(self) -> None:
        if self._task_list:
            for name, task in self._task_dict.items():
                if task.autostart and not task.process and task.executable != "None":
                    task.run_process()

    def stop_all_tasks(self) -> None:
        if self._task_list:
            for name, task in self._task_dict.items():
                if task.process:
                    task.kill_process()

    def handle_download_request(self) -> None:
        print("download request received")

    def set_task_running(self, state: bool) -> None:
        self._task_running = state
        self.taskRunningChanged.emit()

    def handle_child_execution(self, child_id) -> None:
        if self._task_dict[child_id].process is None:
            name = str(self._task_dict[child_id].name)
            path = self._task_dict[child_id].path
            executable = self._task_dict[child_id].executable
            # self._task_dict[child_id].process = run_process(name, path, executable)
            self.delegate_task(child_id, name, path, executable)

        elif self._task_dict[child_id].process is not None:
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(self._task_dict[child_id].process.pid)])
            self._task_dict[child_id].process = None
            self._task_dict[child_id].set_state_color("red")
            self._task_dict[child_id].set_switch_stage(False)
            self._task_dict[child_id].request_start = False

    @Property("QVariantList", notify=task_list_changed)
    def task_list(self):
        return self._task_list

    @Property("QVariant", notify=project_title_changed)
    def project_title(self):
        return self._project_title

    @Property(bool, notify=taskRunningChanged)
    def task_running(self) -> bool:
        return self._task_running

    def append_tasks(self, tasks: []):
        """Shown tasks are getting appended here"""
        for task in tasks:
            self._task_list.append(task)
        self.task_list_changed.emit()

    def handle_project_change_request(self, file):
        if os.path.exists(file):
            print("Changing Project")

            self.stop_all_tasks()
            self._task_list.clear()

            with open(file) as f:
                project = json.load(f)

                if "title" in project:
                    new_title = project["title"]

                else:
                    new_title = "MicroManager"

                self._project_title = new_title
                self.project_title_changed.emit()

                temp_list = []
                tasks = project["tasks"]

                for entry in tasks:
                    ident = str(uuid.uuid4())
                    entry["id"] = ident
                    child = TaskModel(entry)
                    temp_list.append(child)
                    self._task_dict[ident] = child
                    self._child_dict[ident] = entry
                    child.run_exe_request.connect(self.handle_child_execution)

            self.append_tasks(temp_list)
        else:
            print("No Project Found")
