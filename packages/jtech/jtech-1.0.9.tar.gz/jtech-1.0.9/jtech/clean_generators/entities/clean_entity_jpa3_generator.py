from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CleanEntityJpa3Generator(CodeGenerator):

    def get_target(self):
        return "{}Entity.java".format(self.capitalize)

    def get_template(self):
        return tpl.CLEAN_JPA_ENTITY3

    def get_source(self):
        return src.CLEAN_ADAPTERS_OUTPUT_ENTITIES
