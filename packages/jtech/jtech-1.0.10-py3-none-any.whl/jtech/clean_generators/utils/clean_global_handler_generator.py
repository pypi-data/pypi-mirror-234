from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CleanGlobalExceptionHandlerGenerator(CodeGenerator):
    """
    Class for Create Global Exception Handler Java Class
    """

    def get_target(self):
        return "GlobalExceptionHandler.java"

    def get_template(self):
        return tpl.CLEAN_GLOBAL_HANDLER

    def get_source(self):
        return src.CLEAN_CONFIG_INFRA_UTILS
