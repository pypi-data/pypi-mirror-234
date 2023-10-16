import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsSuiteTestGenerator(CodeGenerator):
    """
    Generate Suite test
    """

    def get_target(self):
        return '{}SuiteTests.java'.format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_TEST_SUITE

    def get_source(self):
        return "./"
