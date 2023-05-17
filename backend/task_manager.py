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

from PySide6 import QtCore
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

        with open('settings.json', 'r') as f:

            file = json.load(f)
            self.log_level = file["log_level"]
            self.resolution = file["resolution"]
            self.theme = file["theme"]

            for entry, key in self.theme.items():
                self.root_object.setProperty(entry, key)

        with open('project.json', 'r') as f:
            self.tasks: List[TaskModel] = []
            file = json.load(f)

            if "title" in file:
                title = file["title"]
                self.root_object.setProperty("titleText", title)

            tasks = file["tasks"]
            for entry in tasks:
                self.tasks.append(TaskModel(entry))

        self.root_object.setProperty("width", self.resolution[0])
        self.root_object.setProperty("height", self.resolution[1])

        self._process: Dict[str, subprocess.Popen] = {}

        self.task_manager_model.project.append_tasks(self.tasks)

    def run(self) -> None:
        if not self.engine.rootObjects():
            sys.exit(-1)
        sys.exit(self.app.exec())
