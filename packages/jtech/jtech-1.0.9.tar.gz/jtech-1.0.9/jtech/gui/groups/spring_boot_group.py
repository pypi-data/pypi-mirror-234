import json

import requests
from PyQt5 import QtCore, QtWidgets


class SpringBootVersionGroup:
    def __init__(self, parent_frame):
        self.init_frame(parent_frame)
        self.init_labels(parent_frame)
        self.init_radio_buttons()

    def init_frame(self, parent_frame):
        self.frm_sb = QtWidgets.QFrame(parent_frame)
        self.frm_sb.setGeometry(QtCore.QRect(10, 290, 251, 80))
        self.frm_sb.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_sb.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_sb.setObjectName("frm_sb")

    def init_radio_buttons(self):
        boot_versions = self.get_boot_versions()
        self.radio_buttons = []
        y_offset = 10
        for i, version in enumerate(boot_versions):
            rb = QtWidgets.QRadioButton(self.frm_sb)
            rb.setGeometry(QtCore.QRect(10, y_offset, 231, 23))
            rb.setText(version)
            rb.setObjectName(f"rb_{version}")
            self.radio_buttons.append(rb)
            y_offset += 20

            if i == 0:
                rb.setChecked(True)

    def get_selected_version(self):
        for rb in self.radio_buttons:
            if rb.isChecked():
                return rb.text()
        return None

    def get_boot_versions(self):
        url = "https://start.spring.io/"
        response = requests.get(url)
        if response.status_code == 200:
            parsed = json.loads(response.content)
            values = parsed['bootVersion']['values']
            ids = [value['name'] for value in values if 'M' not in value['name'] and 'SNAPSHOT' not in value['name']]
            return ids
        return ['3.0.9', '3.1.1', '2.7.14']

    def init_labels(self, parent_frame):
        self.lbl_sbv = QtWidgets.QLabel(parent_frame)
        self.lbl_sbv.setGeometry(QtCore.QRect(10, 270, 175, 17))
        self.lbl_sbv.setObjectName("lbl_sbv")
        self.lbl_sbv.setText("Spring Boot Versions:")
