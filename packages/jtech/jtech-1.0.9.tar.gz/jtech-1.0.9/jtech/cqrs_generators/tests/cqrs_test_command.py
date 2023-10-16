import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsCommandTestGenerator(CodeGenerator):
    """
    Generate Create{}CommandTest Sample
    """

    def get_source(self):
        return src.CQRS_COMMAND

    def get_target(self):
        return 'Create{}CommandTest.java'.format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_TEST_COMMAND
