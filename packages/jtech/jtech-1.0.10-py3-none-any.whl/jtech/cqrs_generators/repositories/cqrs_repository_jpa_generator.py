import jtech.utils.dir_constants as source
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsRepositoryJpaGenerator(CodeGenerator):
    """
    Generate Jpa Repository
    """

    def get_target(self):
        return "{}Repository.java".format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_REPOSITORY_JPA

    def get_source(self):
        return source.CQRS_REPOSITORIES
