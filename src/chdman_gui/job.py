from pathlib import Path

from PySide6 import QtCore, QtWidgets

from chdman_gui.consts import CHDMAN_BIN_PATH

class Job:
    def __init__(self, input_path: str):
        self.input_path = Path(input_path)

        self.label = QtWidgets.QLabel(str(self.input_path.stem))

        self.details_browser = QtWidgets.QTextBrowser()
        self.details_browser.append(f"<b>Input full path</b>: {self.input_path}")

        self.details_arrow = QtWidgets.QToolButton()
        self.details_arrow.setArrowType(QtCore.Qt.RightArrow)
        self.details_arrow.clicked.connect(self._handle_details_arrow)


    def show_details(self):
        self.details_browser.show()
        self.details_arrow.setArrowType(QtCore.Qt.DownArrow)

    def hide_details(self):
        self.details_browser.hide()
        self.details_arrow.setArrowType(QtCore.Qt.RightArrow)

    def _handle_details_arrow(self):
        if self.details_browser.isHidden():
            self.show_details()
        else:
            self.hide_details()
