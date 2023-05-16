""""
Copyright (C) 2023 twyleg, PhilippTrashman
"""

from backend.task_manager_model import TaskModel
from PySide6.QtCore import QObject, Signal, Property, Slot
import subprocess
import time


class Task(QObject):
    def __init__(self, task: dict):
        QObject.__init__(self)
        self.name = task['name']
        self.task_model = TaskModel(task)
        self.path = r'/bin'
        self.executable = task['executable']
        self.log_level = task['log_level']
        self.delay = task['delay']

        self.process = None

        # Flag to check if the Executable is running or not
        self.status = False
