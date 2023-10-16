import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsAggregatorImplGenerator(CodeGenerator):
    """
    Generate Aggregate Implementation
    """

    def get_target(self):
        return "{}AggregateImpl.java".format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_AGGREGATE_IMPL

    def get_source(self):
        return src.CQRS_AGGREGATE_IMPL
