from jtech.generator.code_generator import CodeGenerator
import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl


class CqrsFindByIdServiceGenerator(CodeGenerator):
    def get_target(self):
        return "Find{}ByIdService.java".format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_SERVICE_QUERY

    def get_source(self):
        return src.CQRS_SERVICES_QUERIES
