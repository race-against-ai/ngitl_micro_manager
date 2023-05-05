from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog


class FileDialogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Choose Project File")

        self.file_dialog = QFileDialog(self)
        self.file_dialog.setNameFilter("JSON files (*.json)")
        self.file_dialog.setFileMode(QFileDialog.ExistingFile)

    def open_file_dialog(self):
        file_path, _ = self.file_dialog.getOpenFileName()
        print(file_path)
        # if file_path:
        #     # load the selected project file
        #     task_manager_model.loadProjectFromFile(file_path)


if __name__ == '__main__':
    app = QApplication()

    file_dialog_window = FileDialogWindow()
    file_dialog_window.open_file_dialog()

    app.exec()
