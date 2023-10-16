import sys
import json
from PyQt5 import QtWidgets, QtCore, QtGui
import pkg_resources

from jtech.gui.theme.button import btn_default, btn_success
from jtech.gui.theme.textfield import textfield


class DependencySelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent_frame):
        super().__init__(parent_frame)
        self.setModal(True)
        self.checkbox_dict = None
        self.dependencies_path = pkg_resources.resource_filename('jtech', 'resources/dependencies/dependencies.json')
        with open(self.dependencies_path, 'r') as file:
            self.dependencies_data = json.load(file)

        self.init_ui()

    def get_selected_dependencies(self):
        return self.confirm_selection()

    def init_ui(self):
        self.setFixedWidth(800)

        main_layout = QtWidgets.QVBoxLayout()
        self.checkbox_dict = {}
        self.label_dict = {}

        # Filter
        filter_layout = QtWidgets.QHBoxLayout()
        self.filter_edit = QtWidgets.QLineEdit()
        self.filter_edit.setPlaceholderText("Filter by name..")
        self.filter_edit.setStyleSheet(textfield())
        self.filter_edit.textChanged.connect(self.filter_dependencies)
        filter_layout.addWidget(self.filter_edit)
        main_layout.addLayout(filter_layout)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout()

        for group, dependencies in self.dependencies_data.items():
            group_label = QtWidgets.QLabel(group)
            scroll_layout.addWidget(group_label)
            self.label_dict[group] = group_label

            for dependency in dependencies:
                checkbox = QtWidgets.QCheckBox(dependency['name'])
                checkbox.setStyleSheet("QCheckBox { margin-left: 20px; }")
                scroll_layout.addWidget(checkbox)
                self.checkbox_dict[dependency['name']] = checkbox

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        self.init_buttons(main_layout)
        self.setLayout(main_layout)
        self.setWindowTitle("Select Dependencies")
        self.show()

    def init_buttons(self, main_layout):

        button_layout = QtWidgets.QHBoxLayout()

        clear_all_button = QtWidgets.QPushButton("Clear All")
        clear_all_button.clicked.connect(self.clear_all)
        clear_all_button.setStyleSheet(btn_default())
        button_layout.addWidget(clear_all_button, alignment=QtCore.Qt.AlignCenter)

        select_all_button = QtWidgets.QPushButton("Select All")
        select_all_button.clicked.connect(self.select_all)
        select_all_button.setStyleSheet(btn_default())
        button_layout.addWidget(select_all_button, alignment=QtCore.Qt.AlignCenter)

        confirm_button = QtWidgets.QPushButton("Add")
        icon = QtGui.QIcon.fromTheme("list-add")
        confirm_button.setIcon(icon)
        confirm_button.clicked.connect(self.confirm_selection)
        confirm_button.setStyleSheet(btn_success())
        button_layout.addWidget(confirm_button, alignment=QtCore.Qt.AlignCenter)

        main_layout.addLayout(button_layout)

    def select_all(self):
        for checkbox in self.checkbox_dict.values():
            checkbox.setChecked(True)

    def clear_all(self):
        for checkbox in self.checkbox_dict.values():
            checkbox.setChecked(False)

    def filter_dependencies(self):
        filter_text = self.filter_edit.text().strip().lower()

        for name, checkbox in self.checkbox_dict.items():
            checkbox_text = name.lower()
            checkbox.setVisible(filter_text in checkbox_text)

        for group, label in self.label_dict.items():
            group_visible = any(
                self.checkbox_dict[dependency['name']].isVisible()
                for dependency in self.dependencies_data[group]
            )
            label.setVisible(group_visible)

    def confirm_selection(self):
        selected_dependencies = []
        for group, dependencies in self.dependencies_data.items():
            for dependency in dependencies:
                checkbox = self.checkbox_dict.get(dependency['name'])
                if checkbox and checkbox.isChecked():
                    selected_dependencies.append(dependency['value'])
        self.close()
        return selected_dependencies
