from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CleanRepositoryMongoGenerator(CodeGenerator):
    """
    Class for Create MongoRepository Java Class
    """

    def get_target(self):
        return "{}Repository.java".format(self.capitalize)

    def get_template(self):
        return tpl.CLEAN_REPOSITORY_MONGO

    def get_source(self):
        return src.CLEAN_ADAPTERS_OUTPUT_REPOSITORIES
