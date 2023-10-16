from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CleanRepositoryJpaGenerator(CodeGenerator):
    """
    Class for Create Jpa Repository Java Class
    """

    def get_target(self):
        return "{}Repository.java".format(self.capitalize)

    def get_template(self):
        return tpl.CLEAN_REPOSITORY_JPA

    def get_source(self):
        return src.CLEAN_ADAPTERS_OUTPUT_REPOSITORIES
