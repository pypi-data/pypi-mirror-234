import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsRequestGenerator(CodeGenerator):
    """
    Generate Request protocol
    """

    def get_target(self):
        return "{}Request.java".format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_REQUEST

    def get_source(self):
        return src.CQRS_PROTOCOLS
