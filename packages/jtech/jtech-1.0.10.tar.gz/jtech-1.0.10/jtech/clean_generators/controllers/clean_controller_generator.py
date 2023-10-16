import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CleanControllerGenerator(CodeGenerator):
    """
    Class for Create Controller Java Class
    """

    def get_target(self):
        return "Create{}Controller.java".format(self.capitalize)

    def get_template(self):
        return tpl.CLEAN_CONTROLLER

    def get_source(self):
        return src.CLEAN_ADAPTERS_INPUT_CONTROLLERS
