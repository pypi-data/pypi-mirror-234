import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsCommandGenerator(CodeGenerator):
    """
    Generate Create Command
    """

    def get_target(self):
        return "Create{}Command.java".format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_CREATE_COMMAND

    def get_source(self):
        return src.CQRS_COMMAND
