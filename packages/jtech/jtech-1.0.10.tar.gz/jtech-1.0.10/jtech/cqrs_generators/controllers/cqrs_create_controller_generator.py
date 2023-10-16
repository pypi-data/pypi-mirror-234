from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CqrsCreateControllerGenerator(CodeGenerator):
    """
    Generate Create Controller
    """

    def get_target(self):
        return "Create{}Controller.java".format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_CONTROLLER_COMMAND

    def get_source(self):
        return src.CQRS_CONTROLLERS_COMMANDS
