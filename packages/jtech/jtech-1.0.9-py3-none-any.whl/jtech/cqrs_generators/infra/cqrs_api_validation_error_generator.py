import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsApiValidationErrorGenerator(CodeGenerator):
    """
    Generate API Validation Error
    """

    def get_target(self):
        return "ApiValidationError.java"

    def get_template(self):
        return tpl.CQRS_API_VALIDATION_ERROR

    def get_source(self):
        return src.CQRS_INFRA_EXCEPTIONS
