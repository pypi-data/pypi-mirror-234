from PyQt5 import QtCore, QtWidgets


class ProjectGroup:
    def __init__(self, parent_frame):
        self.init_frame(parent_frame)
        self.init_labels()
        self.init_fields()

    def init_frame(self, parent_frame):
        self.frm_project = QtWidgets.QFrame(parent_frame)
        self.frm_project.setGeometry(QtCore.QRect(10, 10, 781, 251))
        self.frm_project.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_project.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_project.setObjectName("frm_project")

    def init_labels(self):
        # Project Name
        self.lbl_project_name = QtWidgets.QLabel(self.frm_project)
        self.lbl_project_name.setGeometry(QtCore.QRect(10, 20, 75, 17))
        self.lbl_project_name.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_project_name.setObjectName("lbl_project_name")
        self.lbl_project_name.setText("Project:")
        # Group
        self.lbl_group = QtWidgets.QLabel(self.frm_project)
        self.lbl_group.setGeometry(QtCore.QRect(10, 60, 75, 17))
        self.lbl_group.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_group.setObjectName("lbl_group")
        self.lbl_group.setText("Group:")
        # Artifact
        self.lbl_artifact = QtWidgets.QLabel(self.frm_project)
        self.lbl_artifact.setGeometry(QtCore.QRect(10, 100, 75, 17))
        self.lbl_artifact.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_artifact.setObjectName("lbl_artifact")
        self.lbl_artifact.setText("Artifact:")
        # Description
        self.lbl_desc = QtWidgets.QLabel(self.frm_project)
        self.lbl_desc.setGeometry(QtCore.QRect(10, 140, 75, 17))
        self.lbl_desc.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_desc.setObjectName("lbl_desc")
        self.lbl_desc.setText("Desc:")
        # Package
        self.lbl_package = QtWidgets.QLabel(self.frm_project)
        self.lbl_package.setGeometry(QtCore.QRect(10, 180, 75, 17))
        self.lbl_package.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_package.setObjectName("lbl_package")
        self.lbl_package.setText("Package:")
        # Banner
        self.lbl_banner = QtWidgets.QLabel(self.frm_project)
        self.lbl_banner.setGeometry(QtCore.QRect(10, 220, 75, 17))
        self.lbl_banner.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_banner.setObjectName("lbl_banner")
        self.lbl_banner.setText("Banner:")

    def init_fields(self):
        # Project Name
        self.txt_project_name = QtWidgets.QLineEdit(self.frm_project)
        self.txt_project_name.setGeometry(QtCore.QRect(90, 10, 681, 25))
        self.txt_project_name.setObjectName("txt_project_name")
        self.txt_project_name.setPlaceholderText("sansys-sample")
        # Group
        self.txt_group = QtWidgets.QLineEdit(self.frm_project)
        self.txt_group.setGeometry(QtCore.QRect(90, 50, 681, 25))
        self.txt_group.setObjectName("txt_group")
        self.txt_group.setPlaceholderText("br.com.sansys.services")
        # Artifact
        self.txt_artifact = QtWidgets.QLineEdit(self.frm_project)
        self.txt_artifact.setGeometry(QtCore.QRect(90, 90, 681, 25))
        self.txt_artifact.setObjectName("txt_artifact")
        self.txt_artifact.setPlaceholderText("sansys-test-sample")
        # Description
        self.txt_desc = QtWidgets.QLineEdit(self.frm_project)
        self.txt_desc.setGeometry(QtCore.QRect(90, 130, 681, 25))
        self.txt_desc.setObjectName("txt_desc")
        self.txt_desc.setPlaceholderText("A Sansys Test Sample")
        # Package
        self.txt_package = QtWidgets.QLineEdit(self.frm_project)
        self.txt_package.setGeometry(QtCore.QRect(90, 170, 681, 25))
        self.txt_package.setObjectName("txt_package")
        self.txt_package.setPlaceholderText("br.com.sansys.services.sample")
        # Banner
        self.txt_banner = QtWidgets.QLineEdit(self.frm_project)
        self.txt_banner.setGeometry(QtCore.QRect(90, 210, 681, 25))
        self.txt_banner.setObjectName("txt_banner")
        self.txt_banner.setPlaceholderText("Sansys Sample")
