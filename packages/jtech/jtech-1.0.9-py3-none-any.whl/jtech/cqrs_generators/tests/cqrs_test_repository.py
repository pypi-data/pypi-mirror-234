import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsRepositoryTestGenerator(CodeGenerator):
    """
    Generate Jpa Repository test
    """

    def get_target(self):
        return '{}RepositoryTest.java'.format(self.capitalize)

    def get_template(self):
        if self.param.jpa:
            return tpl.CQRS_TEST_JPA_REPOSITORY
        else:
            return tpl.CQRS_TEST_MONGO_REPOSITORY

    def get_source(self):
        return src.CQRS_REPOSITORIES
