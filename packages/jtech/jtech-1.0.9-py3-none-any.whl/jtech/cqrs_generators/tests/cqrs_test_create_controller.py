import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsCreateControllerTestGenerator(CodeGenerator):
    """
    Generate Create Controller Test
    """

    def get_template(self):
        if self.param.jpa:
            return tpl.CQRS_TEST_CREATE_JPA_CONTROLLER
        else:
            return tpl.CQRS_TEST_CREATE_MONGO_CONTROLLER

    def get_source(self):
        return src.CQRS_CONTROLLERS_COMMANDS

    def get_target(self):
        return "Create{}ControllerTest.java".format(self.capitalize)
