""""
Copyright (C) 2022 twyleg
"""
from typing import List

from PySide6.QtCore import QObject, Signal, Property
# from task import Task


class TaskModel(QObject):
    name_changed = Signal(name="name_changed")

    open_log_request = Signal(name="open_log_request")
    open_config_request = Signal(name="open_config_request")

    def __init__(self, name: str) -> None:
        QObject.__init__(self)
        self._name = name

    @Property("QString", notify=name_changed)
    def name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name
        self.name_changed.emit()


class TaskManagerModel(QObject):
    task_list_changed = Signal(name="task_list_changed")

    def __init__(self, parent=None):
        super().__init__(parent)
        self._task_list: List[TaskModel] = []

    @Property("QVariantList", notify=task_list_changed)
    def task_list(self):
        return self._task_list

    def append_tasks(self, tasks: []):
        for task in tasks:
            self._task_list.append(task.task_model)
        self.task_list_changed.emit()
