import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsResponseGenerator(CodeGenerator):
    """
    Generate Response protocol
    """

    def get_target(self):
        return "{}Response.java".format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_RESPONSE

    def get_source(self):
        return src.CQRS_PROTOCOLS
