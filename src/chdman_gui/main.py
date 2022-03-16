import glob
import os
import subprocess
import sys
from importlib import import_module
from pathlib import Path
from typing import List, Tuple

from PySide6 import QtGui, QtWidgets

from chdman_gui.consts import CHDMAN_BIN_PATH, MAX_OPTS_PER_COL
from chdman_gui.utils import load_resource


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
        self.job_dropdown.currentIndexChanged.connect(self.update_job_opts_widget)
        self.job_dropdown.currentIndexChanged.connect(self.update_io_filetypes)

        self.media_dropdown_label = QtWidgets.QLabel("Media type:")
        self.media_dropdown = QtWidgets.QComboBox()
        self.media_types = load_resource("media_types")
        self.media_dropdown.addItems([media["text"] for media in self.media_types])
        self.media_dropdown.currentIndexChanged.connect(self.update_job_opts_widget)
        self.media_dropdown.currentIndexChanged.connect(self.update_io_filetypes)

        self.add_files_button = QtWidgets.QPushButton("Add files")
        self.add_files_button.clicked.connect(self.handle_add_files_button)
        self.add_directory_button = QtWidgets.QPushButton("Add a directory")
        self.add_directory_button.clicked.connect(self.handle_add_dir_button)

        self.accepted_inputs_filetypes_label = QtWidgets.QLabel(
            "Accepted inputs filetypes:"
        )
        self.displayed_accepted_inputs_filetypes = QtWidgets.QLabel()

        self.inputs_label = QtWidgets.QLabel("Input files")
        self.inputs_box = QtWidgets.QListWidget()
        self.inputs_box.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.select_all_button = QtWidgets.QPushButton("Select all")
        self.remove_selected_button = QtWidgets.QPushButton("Remove")

        self.output_label = QtWidgets.QLabel("Output Directory:")
        self.output_dirpath = QtWidgets.QLineEdit()
        self.output_dirpath.setText(str(Path(os.path.realpath(__file__)).parent))
        self.output_dirpath.setReadOnly(True)
        self.output_dirpath_button = QtWidgets.QPushButton("Select directory")
        self.output_dirpath_button.clicked.connect(self.select_output_dir)

        self.output_extension_dropdown_label = QtWidgets.QLabel("Output file type:")
        self.output_extension_dropdown = QtWidgets.QComboBox()
        self.update_io_filetypes()

        self.job_opts_label = QtWidgets.QLabel("Job options")

        self.run_jobs_button = QtWidgets.QPushButton("Run job")
        self.run_jobs_button.clicked.connect(self.run_job)

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
            [
                (self.add_files_button, 80),
                (self.add_directory_button, 100),
                (self.accepted_inputs_filetypes_label, 135),
                (self.displayed_accepted_inputs_filetypes, 80),
            ]
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

    def get_current_job(self) -> str:
        current_job = self.jobs_types[self.job_dropdown.currentIndex()]["job_id"]
        return current_job

    def get_current_media(self) -> str:
        current_media = self.media_types[self.media_dropdown.currentIndex()]["media_id"]
        return current_media

    def update_io_filetypes(self):
        current_job = self.get_current_job()
        if current_job == "create":
            self.accepted_inputs_filetypes = self.media_types[
                self.media_dropdown.currentIndex()
            ]["file_types"]
            self.possible_output_filetypes = ["chd"]
        elif current_job == "extract":
            self.accepted_inputs_filetypes = ["chd"]
            self.possible_output_filetypes = self.media_types[
                self.media_dropdown.currentIndex()
            ]["file_types"]
        else:
            self.accepted_inputs_filetypes = ["chd"]
            self.possible_output_filetypes = list()

        self.update_displayed_accepted_inputs_filetypes()
        self.update_possible_out_filetypes_dropdown()

    def update_displayed_accepted_inputs_filetypes(self):
        self.displayed_accepted_inputs_filetypes.setText(
            "<b>" + ", ".join(self.accepted_inputs_filetypes) + "</b>"
        )

    def update_possible_out_filetypes_dropdown(self):
        self.output_extension_dropdown.clear()
        self.output_extension_dropdown.addItems(self.possible_output_filetypes)

    def update_job_opts_widget(self):
        selected_job = self.get_current_job()
        selected_media = self.get_current_media()

        self.job_opts = list()

        try:
            self.job_opts_data = load_resource("jobs_opts/" + selected_job)[
                selected_media
            ]
            for elt in self.job_opts_data:
                left_widget = QtWidgets.QCheckBox(elt["desc"])
                left_widget.setAccessibleName(elt["opt_id"])
                match elt.get("widget", None):
                    case "line_edit":
                        right_widget = QtWidgets.QLineEdit()
                    case "dropdown":
                        right_widget = QtWidgets.QComboBox()
                        dropdown_vals_src = elt["widget_opts"]["values"]
                        if isinstance(dropdown_vals_src, list):
                            dropdown_vals = list(map(str, dropdown_vals_src))
                        elif isinstance(dropdown_vals_src, dict):
                            dropdown_vals = getattr(
                                import_module(dropdown_vals_src["module"]),
                                dropdown_vals_src["func"],
                            )()
                        right_widget.addItems(dropdown_vals)

                    case None:
                        right_widget = QtWidgets.QLabel()
                    case _:
                        raise ValueError(f"Unknown widget type : {elt['widget']}")

                self.job_opts.append([(left_widget, 220), (right_widget, 150)])
        except FileNotFoundError:
            pass

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
            self,
            "Select files",
            "/",
            ";".join([f"*.{ext}" for ext in self.accepted_inputs_filetypes]),
        )[0]
        self.add_files_to_inputs_box(filepaths)

    def handle_add_dir_button(self):
        selected_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select directory"
        )
        filepaths = glob.glob(selected_dir + "/**/*.cue", recursive=True)
        self.add_files_to_inputs_box(filepaths)

    def select_output_dir(self):
        selected_output_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select output directory"
        )
        self.output_dirpath.setText(str(Path(selected_output_dir)))

    def run_job(self):
        # Process job options
        cmd_opts = list()
        for row in self.job_opts_widget.children()[1:]:
            checkbox = row.children()[1]
            if checkbox.isChecked():
                opt_id = checkbox.accessibleName()
                cmd_opts.append("--" + opt_id)
                cmd_opts.append(row.children()[2].text())

        selected_job = self.get_current_job()
        cmd_type = selected_job
        if selected_job in ["create", "extract"]:
            selected_media = self.get_current_media()
            cmd_type += selected_media

        inputs_to_process = [
            Path(self.inputs_box.item(i).text()) for i in range(self.inputs_box.count())
        ]
        for input_path in inputs_to_process:
            output_path = Path(self.output_dirpath.text()) / (input_path.stem + ".chd")
            full_cmd = " ".join(
                [
                    CHDMAN_BIN_PATH,
                    cmd_type,
                    "--input",
                    f'"{input_path}"',
                    "--output",
                    f'"{output_path}"',
                ]
                + cmd_opts
            )
            print(full_cmd)
            subprocess.run(full_cmd)


def main():
    app = QtWidgets.QApplication([])

    main_widget = MainWindow()

    main_widget.setFixedWidth(800)

    font = QtGui.QFont()
    font.setPixelSize(10)
    main_widget.setFont(font)

    main_widget.show()

    sys.exit(app.exec())
