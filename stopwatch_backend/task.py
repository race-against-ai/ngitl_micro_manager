from stopwatch_backend.task_manager_model import TaskModel
from PySide6.QtCore import QObject, Signal, Property, Slot


class Task(QObject):
    def __init__(self, task: dict):
        QObject.__init__(self)
        self.name = task['name']
        self.task_model = TaskModel(task['name'])

        self.task_model.open_log_request.connect(self.handle_open_log_request)
        self.task_model.open_config_request.connect(self.handle_open_config_request)
        self.task_model.open_exe_request.connect(self.handle_exe_request)

        # from the config file, checks if autostart is enabled for this task
        self.autostart = task['enabled']

        # Flag to check if the Executable is running or not
        self.status = False

    def handle_open_log_request(self) -> None:
        print(f'Task {self.name} - open log requested')

    @Slot()
    def handle_open_config_request(self) -> None:
        print(f'Task {self.name} - open config requested')

    def handle_exe_request(self) -> None:
        print(f'Task {self.name} - open exe requested')
