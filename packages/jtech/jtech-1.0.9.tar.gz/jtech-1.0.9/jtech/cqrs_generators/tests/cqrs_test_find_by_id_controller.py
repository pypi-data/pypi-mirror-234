import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsFindByIdControllerTestGenerator(CodeGenerator):
    """
    Generate FindByIdController test.
    """
    def get_target(self):
        return 'Find{}ByIdControllerTest.java'.format(self.capitalize)

    def get_source(self):
        return src.CQRS_CONTROLLERS_QUERIES

    def get_template(self):
        if self.param.jpa:
            return tpl.CQRS_TEST_FIND_BY_ID_JPA_CONTROLLER
        else:
            return tpl.CQRS_TEST_FIND_BY_ID_MONGO_CONTROLLER
