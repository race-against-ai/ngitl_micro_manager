from stopwatch_backend.task_manager_model import TaskModel


class Task:
    def __init__(self, name: str):
        self.name = name
        self.task_model = TaskModel(name)

        self.task_model.open_log_request.connect(self.handle_open_log_request)
        self.task_model.open_config_request.connect(self.handle_open_config_request)

    def handle_open_log_request(self) -> None:
        print(f'Task {self.name} - open log requested')

    def handle_open_config_request(self) -> None:
        print(f'Task {self.name} - open config requested')
