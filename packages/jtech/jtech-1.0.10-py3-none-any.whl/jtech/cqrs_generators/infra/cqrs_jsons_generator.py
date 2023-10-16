import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsJsonsGenerator(CodeGenerator):
    """
    Generate Jsons Utils
    """

    def get_target(self):
        return "Jsons.java"

    def get_template(self):
        return tpl.CQRS_JSONS

    def get_source(self):
        return src.CQRS_UTILS
