import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsAggregatorGenerator(CodeGenerator):
    """
    Generate Aggregate Interface
    """

    def get_target(self):
        return "{}Aggregate.java".format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_AGGREGATE

    def get_source(self):
        return src.CQRS_AGGREGATE
