import os
import shutil
import subprocess
import sys
import tarfile

import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication

from jtech.gui.groups.architecture_group import ArchitectureGroup
from jtech.gui.groups.dependencies_group import DependencyGroup
from jtech.gui.groups.java_version_group import JavaVersionGroup
from jtech.gui.groups.project_group import ProjectGroup
from jtech.gui.groups.spring_boot_group import SpringBootVersionGroup
from jtech.project.create_project_gui import CreateProjectGui


class JtechCLIMainWindow:
    """
    Jtech CLI GUI for Dummies...
    """

    def __init__(self):
        super().__init__()

    def setup_ui(self, main_window):
        # MainWindow
        main_window.setObjectName("main_window")
        main_window.resize(800, 577)
        self.main_frame = QtWidgets.QWidget(main_window)
        self.main_frame.setObjectName("main_frame")

        # Groups
        self.project_group = ProjectGroup(self.main_frame)
        self.spring_group = SpringBootVersionGroup(self.main_frame)
        self.java_group = JavaVersionGroup(self.main_frame)
        self.arch_group = ArchitectureGroup(self.main_frame)
        self.dependency_group = DependencyGroup(self.main_frame)

        self.init_buttons()

        main_window.setCentralWidget(self.main_frame)
        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def show_popup(self):
        popup = QtWidgets.QMessageBox()
        popup.setWindowTitle("Generate Samples")
        popup.setText("Generate sample files?")
        popup.setIcon(QtWidgets.QMessageBox.Information)
        popup.addButton("Yes", QtWidgets.QMessageBox.AcceptRole)
        popup.addButton("No", QtWidgets.QMessageBox.RejectRole)
        result = popup.exec_()
        self.generate_project(result)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Jtech CLI - GUI"))

        self.btn_generate.setToolTip(_translate("MainWindow", "Generate project..."))
        self.btn_generate.setText(_translate("MainWindow", "Generate"))
        self.btn_generate.setShortcut(_translate("MainWindow", "Ctrl+G"))
        self.btn_clear.setText(_translate("MainWindow", "Clear"))
        self.btn_clear.setShortcut(_translate("MainWindow", "Ctrl+Shift+C"))

    def init_buttons(self):
        self.btn_generate = QtWidgets.QPushButton(self.main_frame)
        self.btn_generate.setGeometry(QtCore.QRect(670, 520, 121, 51))
        icon = QtGui.QIcon.fromTheme("document-save")
        self.btn_generate.setIcon(icon)
        self.btn_generate.setObjectName("btn_generate")
        self.btn_generate.clicked.connect(self.show_popup)
        self.btn_clear = QtWidgets.QPushButton(self.main_frame)
        self.btn_clear.setGeometry(QtCore.QRect(540, 520, 121, 51))
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.btn_clear.setIcon(icon)
        self.btn_clear.setObjectName("btn_clear")
        self.btn_clear.clicked.connect(self.clear_fields)

    def clear_fields(self):
        self.project_group.txt_project_name.setText("")
        self.project_group.txt_group.setText("")
        self.project_group.txt_desc.setText("")
        self.project_group.txt_banner.setText("")
        self.project_group.txt_package.setText("")
        self.project_group.txt_artifact.setText("")
        self.dependency_group.lbl_add_dependencies.setText("")
        self.project_group.txt_project_name.setFocus()

    def generate_project(self, result):
        tmp_dir = "/tmp/sb"
        gui_project = CreateProjectGui(
            self.project_group.txt_project_name.text(),
            self.project_group.txt_group.text(),
            self.project_group.txt_artifact.text(),
            self.project_group.txt_package.text(),
            self.java_group.get_selected_version(),
            self.spring_group.get_selected_version(),
            self.dependency_group.lbl_add_dependencies.text(),
            self.project_group.txt_banner.text(),
            self.arch_group.get_selected_architecture(),
            result
        )
        gui_project.create()
        tar_filename = os.path.join(tmp_dir, "{}.tar.gz".format(gui_project.project_name))
        with tarfile.open(tar_filename, "w:gz") as tar:
            tar.add("/tmp/sb/{}".format(gui_project.project_name), arcname=gui_project.project_name)

        self.open_file_dialog(tar_filename)

    def open_file_dialog(self, tar_filename):
        tmp_dir = "/tmp/sb"
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        initial_directory = "/jtech/projects/code/"
        default_filename = "{}.tar.gz".format(self.project_group.txt_project_name.text())
        initial_file_path = os.path.join(initial_directory, default_filename)
        file_dialog = QtWidgets.QFileDialog(self.main_frame)
        file_dialog.selectFile(initial_file_path)
        selected_file, _ = file_dialog.getSaveFileName(directory=initial_directory + default_filename,
                                                       caption="Save Files",
                                                       filter="Tar Files (*.tar.gz);;All Files (*)",
                                                       options=options,
                                                       initialFilter="Tar Files (*.tar.gz)")

        if selected_file:
            shutil.copy(tar_filename, selected_file)
            extract_dir = os.path.dirname(selected_file)
            with tarfile.open(selected_file, "r:gz") as tar:
                tar.extractall(path=extract_dir)

            os.remove(selected_file)
            shutil.rmtree(tmp_dir)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Project created successfully!")
            msg.setInformativeText("Open project directory?")
            msg.setWindowTitle("Success")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            result = msg.exec_()
            if result == QMessageBox.Yes:
                folder_path = os.path.dirname(selected_file)
                subprocess.Popen(["xdg-open", folder_path])

        self.clear_fields()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = QtWidgets.QMainWindow()
    ui = JtechCLIMainWindow()

    main_frame_width = 800
    main_frame_height = 577
    window.setFixedSize(main_frame_width, main_frame_height)
    ui.setup_ui(window)
    window.show()
    sys.exit(app.exec_())


def open_gui_interface():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = QtWidgets.QMainWindow()
    ui = JtechCLIMainWindow()

    main_frame_width = 800
    main_frame_height = 577
    window.setFixedSize(main_frame_width, main_frame_height)
    ui.setup_ui(window)
    window.show()
    sys.exit(app.exec_())