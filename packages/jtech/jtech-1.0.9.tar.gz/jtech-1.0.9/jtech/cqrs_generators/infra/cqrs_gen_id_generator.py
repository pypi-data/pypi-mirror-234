import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsGenIdGenerator(CodeGenerator):
    """
    Generate GenId Utils
    """

    def get_target(self):
        return "GenId.java"

    def get_template(self):
        return tpl.CQRS_GEN_ID

    def get_source(self):
        return src.CQRS_UTILS
