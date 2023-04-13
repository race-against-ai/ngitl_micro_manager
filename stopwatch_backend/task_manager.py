""""
Copyright (C) 2023 twyleg
"""
import os
import sys
import time
import json
import subprocess
from pathlib import Path
from typing import List, Optional, Dict

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

        with open('settings.json', 'r') as f:
            tasks: List[Task] = []
            file = json.load(f)
            self.tasks = file["tasks"]
            for entry in self.tasks:
                tasks.append(Task(entry))

        self._process: Dict[str, subprocess.Popen] = {}

        self.task_manager_model.append_tasks(tasks)

    def handle_open_log_request(self) -> None:
        print("foo")

    def run_process(self, name: str, path: str, file: str, delay: float) -> None:
        """Run the wanted executable and set its delay after startup"""
        self._process[name] = subprocess.Popen(rf'{path}\{file}',
                                   cwd=path,
                                   creationflags=subprocess.CREATE_NEW_CONSOLE)
                                   # stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        time.sleep(delay)

    def kill_process(self, name: str) -> None:
        """Forcefully closes the Task"""
        if name in self._process:
            # self._process[name].terminate()
            subprocess.call(['taskkill', '/F', '/T', '/PID]', str(self._process[name].pid)])
            self._process.pop(name)
        else:
            print(f"Process with the ID: {name} isn't Running")

    def run(self) -> None:
        if not self.engine.rootObjects():
            sys.exit(-1)
        sys.exit(self.app.exec())
