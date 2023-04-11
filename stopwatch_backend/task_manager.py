""""
Copyright (C) 2022 twyleg
"""
import os
import sys
import time
from pathlib import Path
from typing import List, Optional

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from task_manager_model import TaskManagerModel, TaskModel
from task import Task


class TaskManager:

    def __init__(self) -> None:
        self.task_manager_model = TaskManagerModel()

        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()

        self.engine.rootContext().setContextProperty("task_manager_model", self.task_manager_model)
        self.engine.load(os.fspath(Path(__file__).resolve().parent / "../frontend/qml/main.qml"))

        tasks: List[Task] = []
        tasks.append(Task('Task 1'))
        tasks.append(Task('Task 2'))

        self.task_manager_model.append_tasks(tasks)

    def handle_open_log_request(self) -> None:
        print("foo")

    def run(self) -> None:
        if not self.engine.rootObjects():
            sys.exit(-1)
        sys.exit(self.app.exec())
