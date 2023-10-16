import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CleanApiErrorGenerator(CodeGenerator):
    """
    Class for Create Api Error Exception Java Class
    """

    def get_target(self):
        return "ApiError.java"

    def get_template(self):
        return tpl.CLEAN_API_ERROR

    def get_source(self):
        return src.CLEAN_CONFIG_INFRA_EXCEPTIONS
