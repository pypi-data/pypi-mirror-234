import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CleanOpenApiGenerator(CodeGenerator):
    """
    Class for Create OpenAPI30Configuration Configuration Java Class
    """

    def get_target(self):
        return "OpenAPI30Configuration.java"

    def get_template(self):
        return tpl.CLEAN_OPENAPI

    def get_source(self):
        return src.CLEAN_CONFIG_INFRA_SWAGGER