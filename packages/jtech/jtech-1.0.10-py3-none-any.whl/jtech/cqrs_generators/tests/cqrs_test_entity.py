import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsEntityTestGenerator(CodeGenerator):
    """
    Generate Entity Test for versions
    """

    def get_template(self):
        if self.param.jpa:
            return tpl.CQRS_TEST_JPA_ENTITY
        elif self.param.mongo:
            return tpl.CQRS_TEST_MONGO_ENTITY
        else:
            return tpl.CQRS_TEST_DEFAULT_ENTITY

    def get_source(self):
        return src.CQRS_ENTITIES

    def get_target(self):
        return '{}EntityTest.java'.format(self.capitalize)
