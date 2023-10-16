from PyQt5 import QtWidgets, QtCore, QtGui

from jtech.gui.handlers.dependencies_handler import DependencyActionEvent


class DependencyGroup:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.init_frame(parent_frame)
        self.init_labels(parent_frame)
        self.init_buttons()
        self.init_handler()

    def init_buttons(self):
        self.btn_add_dependencies = QtWidgets.QPushButton(self.frame)
        self.btn_add_dependencies.setGeometry(QtCore.QRect(430, 10, 341, 41))
        icon = QtGui.QIcon.fromTheme("list-add")
        self.btn_add_dependencies.setIcon(icon)
        self.btn_add_dependencies.setObjectName("btn_add_dependencies")
        self.btn_clear_dependencies = QtWidgets.QPushButton(self.frame)
        self.btn_clear_dependencies.setGeometry(QtCore.QRect(430, 60, 341, 41))
        self.btn_add_dependencies.setText(" Add Dependencies")
        icon = QtGui.QIcon.fromTheme("image-missing")
        self.btn_clear_dependencies.setIcon(icon)
        self.btn_clear_dependencies.setObjectName("btn_clear_dependencies")
        self.btn_clear_dependencies.setText(" Clear Dependencies")

    def init_labels(self, parent_frame):
        self.lbl_add_dependencies = QtWidgets.QLabel(self.frame)
        self.lbl_add_dependencies.setGeometry(QtCore.QRect(10, 10, 371, 91))
        self.lbl_add_dependencies.setScaledContents(True)
        self.lbl_add_dependencies.setWordWrap(True)
        self.lbl_add_dependencies.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lbl_add_dependencies.setObjectName("lbl_add_dependencies")
        self.lbl_dependencies = QtWidgets.QLabel(parent_frame)
        self.lbl_dependencies.setGeometry(QtCore.QRect(10, 380, 171, 17))
        self.lbl_dependencies.setObjectName("lbl_dependencies")
        self.lbl_dependencies.setText("Dependencies:")

    def init_frame(self, parent_frame):
        self.frame = QtWidgets.QFrame(parent_frame)
        self.frame.setGeometry(QtCore.QRect(10, 400, 781, 111))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

    def set_dependencies_text(self, text):
        self.lbl_add_dependencies.setText(text)

    def open_dependency_selection_dialog(self):
        handler = DependencyActionEvent()
        selected_dependencies = handler.selected_dependencies(self.parent)
        selected_dependencies.append("web")
        selected_dependencies.append("lombok")
        self.lbl_add_dependencies.setText(", ".join(selected_dependencies))

    def clear_dependencies(self):
        self.lbl_add_dependencies.setText("")

    def init_handler(self):
        self.btn_add_dependencies.clicked.connect(self.open_dependency_selection_dialog)
        self.btn_clear_dependencies.clicked.connect(self.clear_dependencies)
