""""
Copyright (C) 2023 twyleg, PhilippTrashman
"""
import os
import sys
import time
import json
import subprocess
from pathlib import Path
from typing import List, Optional, Dict

from PySide6.QtCore import Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from task_manager_model import TaskManagerModel, TaskModel


class TaskManager:

    def __init__(self) -> None:

        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()

        self.task_manager_model = TaskManagerModel(self.app)

        self.engine.rootContext().setContextProperty("task_manager_model", self.task_manager_model)
        self.engine.load(os.fspath(Path(__file__).resolve().parent / "../frontend/qml/main.qml"))

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
        self.read_settings()

        self.tasks: List[TaskModel] = []
        self.task_manager_model.project.handle_project_change_request('projects/RAAI.json')

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

        # print(completion_check)

        log_level = self.settings["log_level"]
        theme = self.settings["theme"]
        resolution = self.settings["resolution"]
        dev_mode = self.settings["dev_mode"]

        self.root_object.setProperty("width", resolution[0])
        self.root_object.setProperty("height", resolution[1])
        self.root_object.setProperty("devMode", dev_mode)

        for entry, key in theme.items():
            self.root_object.setProperty(entry, key)

    def read_project(self, file: str):
        if file[-5:] == ".json":
            print(f"reading Project: {file}")
            with open(file, 'r') as f:
                project = json.load(f)

                if "title" in project:
                    title = project["title"]
                    # self.change_title(title)

                tasks = project["tasks"]
                for entry in tasks:
                    self.tasks.append(TaskModel(entry))

    def run(self) -> None:
        if not self.engine.rootObjects():
            sys.exit(-1)
        sys.exit(self.app.exec())
