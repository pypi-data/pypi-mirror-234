import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CleanConfigGenerator(CodeGenerator):
    """
    Class for Create Config Java Class
    """

    def get_target(self):
        return "Create{}UseCaseConfig.java".format(self.capitalize)

    def get_template(self):
        return tpl.CLEAN_CONFIG

    def get_source(self):
        return src.CLEAN_CONFIG_USECASES
