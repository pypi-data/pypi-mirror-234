import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CleanDomainGenerator(CodeGenerator):
    """
    Class for Create Domain Java Class
    """

    def get_target(self):
        return "{}.java".format(self.capitalize)

    def get_template(self):
        return tpl.CLEAN_DOMAIN

    def get_source(self):
        return src.CLEAN_DOMAINS
