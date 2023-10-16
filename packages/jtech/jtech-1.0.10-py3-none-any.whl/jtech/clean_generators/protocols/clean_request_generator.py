from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CleanRequestGenerator(CodeGenerator):
    """
    Class for Create Request Protocol Java Class
    """

    def get_target(self):
        return "{}Request.java".format(self.capitalize)

    def get_template(self):
        return tpl.CLEAN_REQUEST

    def get_source(self):
        return src.CLEAN_ADAPTERS_INPUT_PROTOCOLS
