import getpass
from jtech.template_processor.processor import Processor


class CodeGenerator:
    """
    Superclass for generate Code
    """

    def __init__(self, param, project, capitalize, folder):
        self.param = param
        self.project = project
        self.capitalize = capitalize
        self.folder = folder

    def generate(self):
        data = {
            "isJpa": self.param.jpa,
            "isMongo": self.param.mongo,
            "package": self.param.package,
            "className": self.capitalize,
            "project": self.project,
            "username": getpass.getuser()
        }
        generator = Processor(self.folder, data)
        generator.exec(self.get_template(), self.get_source(), self.get_target())

    def get_target(self):
        raise NotImplementedError()

    def get_template(self):
        raise NotImplementedError()

    def get_source(self):
        raise NotImplementedError()
