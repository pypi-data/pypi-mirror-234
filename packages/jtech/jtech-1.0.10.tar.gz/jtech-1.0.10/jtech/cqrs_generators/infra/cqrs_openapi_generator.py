import jtech.utils.dir_constants as source
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsOpenApiGenerator(CodeGenerator):
    """
    Generate OpenAPI Configuration
    """

    def get_target(self):
        return "OpenAPI30Configuration.java"

    def get_template(self):
        return tpl.CQRS_OPENAPI

    def get_source(self):
        return source.CQRS_INFRA
