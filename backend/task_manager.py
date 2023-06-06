""""
Copyright (C) 2023 twyleg, PhilippTrashman
"""
import os
import sys
import json
from pathlib import Path
from typing import List, Optional, Dict

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from task_manager_model import TaskManagerModel, TaskModel


def find_qml_main_file(relative_path: str) -> Path:
    search_directory_list = [
        Path(os.getcwd()),
        Path(os.getcwd()).parent,
        Path(__file__).parent
    ]
    for directory in search_directory_list:
        filepath = directory / relative_path
        if filepath.is_file():
            print(f'chose: {filepath}')
            return filepath
    raise FileNotFoundError(f'Unable to find QML File: {relative_path}')


class TaskManager:

    def __init__(self) -> None:

        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()

        self.task_manager_model = TaskManagerModel(self.app)

        self.engine.rootContext().setContextProperty("task_manager_model", self.task_manager_model)
        self.engine.load(find_qml_main_file("frontend/qml/main.qml"))

        self.root_object = self.engine.rootObjects()[0]

        self.settings = {
            "resolution": [800, 600],
            "theme": {
                    "primary_color": "#262b33",
                    "secondary_color": "#2f343f",
                    "tertiary_color": "#4c5e7c"
            },
            "log_level": "INFO",
            "dev_mode": False,
            "standard_project": ""
        }
        self.project = self.settings["standard_project"]
        self.read_settings()

        self.tasks: List[TaskModel] = []
        self.task_manager_model.project.handle_project_change_request(self.project)

    def read_settings(self):
        if os.path.isfile("settings.json"):
            completion_check = True

            with open('settings.json', 'r') as f:
                if completion_check:
                    file = json.load(f)
                    for key in self.settings:
                        if key in file:
                            self.settings[key] = file[key]
                        else:
                            print(f'Value "{key}" missing in setting: Using Standard Settings for Value')
                            completion_check = False

            if not completion_check:
                file = json.dumps(self.settings, indent=4)
                with open("settings.json", 'w') as f:
                    f.write(file)

        else:
            print("Settings File not Found: Creating new at root location")
            file = json.dumps(self.settings, indent=4)
            with open("settings.json", 'w') as f:
                f.write(file)

        log_level = self.settings["log_level"]
        theme = self.settings["theme"]
        resolution = self.settings["resolution"]
        dev_mode = self.settings["dev_mode"]
        self.project = self.settings["standard_project"]

        self.root_object.setProperty("width", resolution[0])
        self.root_object.setProperty("height", resolution[1])
        self.root_object.setProperty("devMode", dev_mode)

        for entry, key in theme.items():
            self.root_object.setProperty(entry, key)

    def run(self) -> None:
        if not self.engine.rootObjects():
            sys.exit(-1)
        sys.exit(self.app.exec())
