import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsResponseTestGenerator(CodeGenerator):
    """
    Generate response protocol test
    """

    def get_target(self):
        return '{}ResponseTest.java'.format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_TEST_RESPONSE

    def get_source(self):
        return src.CQRS_PROTOCOLS
