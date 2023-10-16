import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CleanUseCaseGenerator(CodeGenerator):
    """
    Class for Create UseCase Java Class
    """

    def get_target(self):
        return "Create{}UseCase.java".format(self.capitalize)

    def get_template(self):
        return tpl.CLEAN_USECASE

    def get_source(self):
        return src.CLEAN_USECASE
