import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl

from jtech.generator.code_generator import CodeGenerator


class CqrsCreateServiceGenerator(CodeGenerator):
    def get_target(self):
        return "Create{}Service.java".format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_SERVICE_COMMAND

    def get_source(self):
        return src.CQRS_SERVICES_COMMANDS
