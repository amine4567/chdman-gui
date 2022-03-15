import glob
import sys
from pathlib import Path
from typing import List, Tuple

from PySide6 import QtWidgets

from .utils import load_resource

MAX_OPTS_PER_COL = 9


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
        self.jobs_types = load_resource("jobs_types")
        self.job_dropdown.addItems([job["text"] for job in self.jobs_types])

        self.media_dropdown_label = QtWidgets.QLabel("Media type:")
        self.media_dropdown = QtWidgets.QComboBox()
        self.media_types = load_resource("media_types")
        self.media_dropdown.addItems([media["text"] for media in self.media_types])
        self.media_dropdown.currentIndexChanged.connect(self.update_job_opts_widget)

        self.add_files_button = QtWidgets.QPushButton("Add files")
        self.add_files_button.clicked.connect(self.handle_add_files_button)
        self.add_directory_button = QtWidgets.QPushButton("Add a directory")
        self.add_directory_button.clicked.connect(self.handle_add_dir_button)

        self.inputs_label = QtWidgets.QLabel("Input files")
        self.inputs_box = QtWidgets.QListWidget()
        self.inputs_box.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.select_all_button = QtWidgets.QPushButton("Select all")
        self.remove_selected_button = QtWidgets.QPushButton("Remove")

        self.output_label = QtWidgets.QLabel("Output Directory:")
        self.output_dirpath = QtWidgets.QLineEdit()
        self.output_dirpath.setReadOnly(True)
        self.output_dirpath_button = QtWidgets.QPushButton("Select directory")

        self.output_extension_dropdown_label = QtWidgets.QLabel("Output file type:")
        self.output_extension_dropdown = QtWidgets.QComboBox()
        self.output_extension_dropdown.addItems(["ext1", "ext2", "ext3"])

        self.job_opts_label = QtWidgets.QLabel("Job options")

        self.run_jobs_button = QtWidgets.QPushButton("Run jobs")

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

        # 8th row
        self.layout.addWidget(self.run_jobs_button)

        # 9th row
        self.layout.addWidget(self.job_opts_label)

        # 10th row and beyond: job options
        self.update_job_opts_widget()

    def update_job_opts_widget(self):
        selected_job = self.jobs_types[self.job_dropdown.currentIndex()]["job_id"]
        selected_media = self.media_types[self.media_dropdown.currentIndex()][
            "media_id"
        ]

        job_opts_dict = load_resource("jobs_opts/" + selected_job)[selected_media]
        self.job_opts = list()
        for elt in job_opts_dict:
            left_widget = QtWidgets.QCheckBox(elt["desc"])
            match elt.get("widget", None):
                case "line_edit":
                    right_widget = QtWidgets.QLineEdit()
                case "dropdown":
                    right_widget = QtWidgets.QComboBox()
                case None:
                    right_widget = QtWidgets.QLabel()
                case _:
                    raise ValueError(f"Unknown widget type : {elt['widget']}")

            self.job_opts.append([(left_widget, 250), (right_widget, 120)])

        # Update layout
        if hasattr(self, "job_opts_widget"):
            self.layout.removeWidget(self.job_opts_widget)
            self.job_opts_widget.hide()

        rows = self.job_opts[:MAX_OPTS_PER_COL]
        if len(self.job_opts) > MAX_OPTS_PER_COL:
            for i, widgets in enumerate(self.job_opts[MAX_OPTS_PER_COL:]):
                rows[i].extend(widgets)

        self.job_opts_layout = QtWidgets.QVBoxLayout()
        self.job_opts_widget = QtWidgets.QWidget()

        for row in rows:
            row_widget, row_layout = custom_horizontal_box(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            self.job_opts_layout.addWidget(row_widget)

        self.job_opts_widget.setLayout(self.job_opts_layout)

        self.layout.addWidget(self.job_opts_widget)

    def add_files_to_inputs_box(self, filepaths: List[str]):
        existing_paths = set(
            [
                Path(self.inputs_box.item(i).text())
                for i in range(self.inputs_box.count())
            ]
        )
        self.inputs_box.addItems(map(str, set(map(Path, filepaths)) - existing_paths))

    def handle_add_files_button(self):
        filepaths = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select files", "/", "*.cue;*.toc;*.gdi"
        )[0]
        self.add_files_to_inputs_box(filepaths)

    def handle_add_dir_button(self):
        selected_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select directory"
        )
        filepaths = glob.glob(selected_dir + "/**/*.cue", recursive=True)
        self.add_files_to_inputs_box(filepaths)


def main():
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.setFixedWidth(800)
    widget.show()

    sys.exit(app.exec())
