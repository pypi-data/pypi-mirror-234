from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CleanGenIdGenerator(CodeGenerator):
    """
    Class for Create GenId Java Class
    """

    def get_target(self):
        return "GenId.java"

    def get_template(self):
        return tpl.CLEAN_GEN_ID

    def get_source(self):
        return src.CLEAN_CONFIG_INFRA_UTILS
