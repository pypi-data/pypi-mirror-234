import json

import requests
from PyQt5 import QtCore, QtWidgets


class JavaVersionGroup:
    def __init__(self, parent_frame):
        self.init_frame(parent_frame)
        self.init_labels(parent_frame)
        self.init_radio_buttons()

    def init_frame(self, parent_frame):
        self.frm_java = QtWidgets.QFrame(parent_frame)
        self.frm_java.setGeometry(QtCore.QRect(270, 290, 251, 80))
        self.frm_java.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_java.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_java.setObjectName("frm_java")

    def init_radio_buttons(self):
        java_versions = self.get_available_java_versions()
        self.radio_buttons = []
        y_offset = 10
        for i, version in enumerate(java_versions):
            rb = QtWidgets.QRadioButton(self.frm_java)
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

    def get_available_java_versions(self):
        url = "https://start.spring.io/"
        response = requests.get(url)
        if response.status_code == 200:
            parsed = json.loads(response.content)
            ids_array = []
            java_versions = parsed['javaVersion']
            values_list = java_versions['values']
            for value in values_list:
                version_id = value['id']
                if version_id != '11':
                    ids_array.append(version_id)
            return ids_array
        return ['1.8', '17', '20']

    def init_labels(self, parent_frame):
        self.lbl_java_version = QtWidgets.QLabel(parent_frame)
        self.lbl_java_version.setGeometry(QtCore.QRect(270, 270, 171, 17))
        self.lbl_java_version.setObjectName("lbl_java_version")
        self.lbl_java_version.setText("Java Version:")
