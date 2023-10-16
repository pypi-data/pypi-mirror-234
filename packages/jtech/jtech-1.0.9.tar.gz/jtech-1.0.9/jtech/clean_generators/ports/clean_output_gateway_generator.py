from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CleanOutputGatewayGenerator(CodeGenerator):
    """
    Class for Create OutputGateway Java Class
    """

    def get_target(self):
        return "Create{}OutputGateway.java".format(self.capitalize)

    def get_template(self):
        return tpl.CLEAN_OUTPUT_GATEWAY

    def get_source(self):
        return src.CLEAN_PORT_OUTPUT
