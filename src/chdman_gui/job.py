from pathlib import Path

from PySide6 import QtCore, QtWidgets


class Job:
    def __init__(self, full_path: str):
        self.full_path = Path(full_path)

        self.label = QtWidgets.QLabel(str(self.full_path.stem))

        self.details_browser = QtWidgets.QTextBrowser()
        self.details_browser.append(f"<b>Input full path</b>: {self.full_path}")

        self.details_arrow = QtWidgets.QToolButton()
        self.details_arrow.setArrowType(QtCore.Qt.RightArrow)
        self.details_arrow.clicked.connect(self.handle_details_arrow)

    def handle_details_arrow(self):
        if self.details_browser.isHidden():
            self.show_details()
        else:
            self.hide_details()

    def show_details(self):
        self.details_browser.show()
        self.details_arrow.setArrowType(QtCore.Qt.DownArrow)

    def hide_details(self):
        self.details_browser.hide()
        self.details_arrow.setArrowType(QtCore.Qt.RightArrow)
