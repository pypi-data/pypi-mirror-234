import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CleanEntityDefaultGenerator(CodeGenerator):
    """
    Class for Create Entity Java Class
    """

    def get_target(self):
        return "{}Entity.java".format(self.capitalize)

    def get_template(self):
        return tpl.CLEAN_ENTITY

    def get_source(self):
        return src.CLEAN_ADAPTERS_OUTPUT_ENTITIES
