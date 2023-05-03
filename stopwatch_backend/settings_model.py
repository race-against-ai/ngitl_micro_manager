""""
Copyright (C) 2023 twyleg, PhilippTrashman
"""

from typing import List

from PySide6.QtCore import QObject, Signal, Property


class SettingsModel(QObject):

    theme_request = Signal(name="theme_change_requested")
    open_folder_request = Signal(name="open_folder_request")

    def __init__(self) -> None:
        QObject.__init__(self)

        self.theme_request.connect(self.handle_theme_change)
        self.open_folder_request.connect(self.handle_open_folder_request)

    def handle_theme_change(self) -> None:
        print("changing theme")

    def handle_open_folder_request(self) -> None:
        print("Opening Folder")


class SettingsManagerModel(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
