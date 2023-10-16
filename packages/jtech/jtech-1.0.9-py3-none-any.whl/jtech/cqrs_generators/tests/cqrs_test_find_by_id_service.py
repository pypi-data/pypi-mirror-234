import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsFindByIdServiceTestGenerator(CodeGenerator):
    """
    Generate FindByIdService test
    """

    def get_target(self):
        return 'Find{}ByIdServiceTest.java'.format(self.capitalize)

    def get_source(self):
        return src.CQRS_SERVICES_QUERIES_IMPL

    def get_template(self):
        if self.param.jpa:
            return tpl.CQRS_TEST_FIND_BY_ID_JPA_SERVICE
        else:
            return tpl.CQRS_TEST_FIND_BY_ID_MONGO_SERVICE
