from PyQt5 import QtCore, QtWidgets


class ArchitectureGroup:
    def __init__(self, parent_frame):
        self.init_frame(parent_frame)
        self.init_labels(parent_frame)
        self.init_radio_buttons()

    def init_frame(self, parent_frame):
        self.frm_arch = QtWidgets.QFrame(parent_frame)
        self.frm_arch.setGeometry(QtCore.QRect(530, 290, 261, 80))
        self.frm_arch.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_arch.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_arch.setObjectName("frm_arch")

    def init_radio_buttons(self):
        self.radio_buttons = []
        self.rb_cqrs = QtWidgets.QRadioButton(self.frm_arch)
        self.rb_cqrs.setGeometry(QtCore.QRect(10, 30, 231, 23))
        self.rb_cqrs.setObjectName("rb_cqrs")
        self.rb_cqrs.setText("CQRS")
        self.radio_buttons.append(self.rb_cqrs)
        self.rb_spring = QtWidgets.QRadioButton(self.frm_arch)
        self.rb_spring.setGeometry(QtCore.QRect(10, 50, 231, 23))
        self.rb_spring.setObjectName("rb_spring")
        self.rb_spring.setText("Spring")
        self.radio_buttons.append(self.rb_spring)
        self.rb_ca = QtWidgets.QRadioButton(self.frm_arch)
        self.rb_ca.setGeometry(QtCore.QRect(10, 10, 231, 23))
        self.rb_ca.setChecked(True)
        self.rb_ca.setObjectName("rb_ca")
        self.rb_ca.setText("Clean Architecture")
        self.radio_buttons.append(self.rb_ca)

    def get_selected_architecture(self):
        for rb in self.radio_buttons:
            if rb.isChecked():
                return rb.text()
        return None

    def init_labels(self, parent_frame):
        self.lbl_arch = QtWidgets.QLabel(parent_frame)
        self.lbl_arch.setGeometry(QtCore.QRect(530, 270, 171, 17))
        self.lbl_arch.setObjectName("lbl_arch")
        self.lbl_arch.setText("Architecture:")
