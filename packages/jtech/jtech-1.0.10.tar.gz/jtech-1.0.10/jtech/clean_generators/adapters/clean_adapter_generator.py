import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CleanAdapterGenerator(CodeGenerator):
    """
    Class for Create Adapter Java Class
    """

    def get_target(self):
        return "Create{}Adapter.java".format(self.capitalize)

    def get_template(self):
        return tpl.CLEAN_ADAPTER

    def get_source(self):
        return src.CLEAN_ADAPTERS_OUTPUT
