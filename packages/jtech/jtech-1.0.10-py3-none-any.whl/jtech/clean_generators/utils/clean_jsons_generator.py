from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CleanJsonsGenerator(CodeGenerator):
    """
    Class for Create Jsons Java Class
    """

    def get_target(self):
        return "Jsons.java"

    def get_template(self):
        return tpl.CLEAN_JSONS

    def get_source(self):
        return src.CLEAN_CONFIG_INFRA_UTILS
