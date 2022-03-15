import sys
from typing import List, Tuple

from PySide6 import QtWidgets

jobs_types = [
    {"job_id": "info", "text": "Display information about a CHD"},
    {"job_id": "verify", "text": "Verify a CHD's integrity"},
    {"job_id": "create", "text": "Create CHD from media"},
    {"job_id": "extract", "text": "Extract media from CHD"},
    {
        "job_id": "copy",
        "text": "Copy data from a CHD to another",
    },
    {"job_id": "addmeta", "text": "Add metadata to CHD"},
    {"job_id": "delmeta", "text": "remove metadata from CHD"},
    {"job_id": "dumpmeta", "text": "Dump metadata from CHD"},
]

media_types = [
    {"media_id": "cd", "text": "CD image"},
    {"media_id": "hd", "text": "Hard Disk image"},
    {"media_id": "ld", "text": "LaserDisc image"},
    {"media_id": "raw", "text": "Raw image"},
]


def custom_horizontal_box(
    widgets: List[Tuple[QtWidgets.QWidget, int]]
) -> Tuple[QtWidgets.QWidget, QtWidgets.QLayout]:
    layout = QtWidgets.QHBoxLayout()
    for widget, width in widgets:
        widget.setFixedWidth(width)
        layout.addWidget(widget)

    parent_widget = QtWidgets.QWidget()
    # We add len(widgets) * 10 to leave some space for margins between the widgets
    parent_widget.setFixedWidth(sum([elt[1] for elt in widgets]) + len(widgets) * 10)
    parent_widget.setLayout(layout)

    return parent_widget, layout


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.job_dropdown_label = QtWidgets.QLabel("Job type:")
        self.job_dropdown = QtWidgets.QComboBox()
        self.job_dropdown.addItems([job["text"] for job in jobs_types])

        self.media_dropdown_label = QtWidgets.QLabel("Media type:")
        self.media_dropdown = QtWidgets.QComboBox()
        self.media_dropdown.addItems([media["text"] for media in media_types])

        self.add_files_button = QtWidgets.QPushButton("Add files")
        self.add_directory_button = QtWidgets.QPushButton("Add a directory")

        self.inputs_label = QtWidgets.QLabel("Input files")
        self.inputs_box = QtWidgets.QListWidget()
        self.inputs_box.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.inputs_box.addItem("D:\\Some\\File\\path\\1.cue")
        self.inputs_box.addItem("D:\\Some\\File\\path\\2.cue")
        self.inputs_box.addItem("D:\\Some\\File\\path\\3.cue")
        self.inputs_box.addItem("D:\\Some\\File\\path\\4.cue")

        self.select_all_button = QtWidgets.QPushButton("Select all")
        self.remove_selected_button = QtWidgets.QPushButton("Remove")

        self.output_label = QtWidgets.QLabel("Output Directory:")
        self.output_dirpath = QtWidgets.QLineEdit()
        self.output_dirpath.setReadOnly(True)
        self.output_dirpath_button = QtWidgets.QPushButton("Select directory")

        self.output_extension_dropdown_label = QtWidgets.QLabel("Output file type:")
        self.output_extension_dropdown = QtWidgets.QComboBox()
        self.output_extension_dropdown.addItems(["ext1", "ext2", "ext3"])

        self.layout = QtWidgets.QVBoxLayout(self)

        # First row
        self.first_row_widget, self.first_row_layout = custom_horizontal_box(
            [
                (self.job_dropdown_label, 50),
                (self.job_dropdown, 220),
                (self.media_dropdown_label, 70),
                (self.media_dropdown, 120),
            ]
        )
        self.first_row_layout.setContentsMargins(0, 10, 0, 10)
        self.layout.addWidget(self.first_row_widget)

        # Second row
        self.inputs_label.setContentsMargins(5, 0, 0, 0)
        self.layout.addWidget(self.inputs_label)

        # Third row
        self.third_row_widget, self.third_row_layout = custom_horizontal_box(
            [(self.add_files_button, 80), (self.add_directory_button, 100)]
        )
        self.third_row_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.third_row_widget)

        # Fourth row
        self.inputs_box.setFixedHeight(150)
        self.layout.addWidget(self.inputs_box)

        # Fifth row
        self.fifth_row_widget, self.fifth_row_layout = custom_horizontal_box(
            [(self.select_all_button, 100), (self.remove_selected_button, 100)]
        )
        self.layout.addWidget(self.fifth_row_widget)

        # Sixth row
        self.sixth_row_widget, self.sixth_row_layout = custom_horizontal_box(
            [
                (self.output_label, 90),
                (self.output_dirpath, 400),
                (self.output_dirpath_button, 100),
            ]
        )
        self.layout.addWidget(self.sixth_row_widget)

        # Seventh row
        self.seventh_row_widget, self.seventh_row_layout = custom_horizontal_box(
            [
                (self.output_extension_dropdown_label, 90),
                (self.output_extension_dropdown, 50),
            ]
        )
        self.layout.addWidget(self.seventh_row_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.setFixedWidth(800)
    widget.show()

    sys.exit(app.exec())
