from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CleanResponseGenerator(CodeGenerator):
    """
    Class for Create Response Protocol Java Class
    """

    def get_target(self):
        return "{}Response.java".format(self.capitalize)

    def get_template(self):
        return tpl.CLEAN_RESPONSE

    def get_source(self):
        return src.CLEAN_ADAPTERS_INPUT_PROTOCOLS
