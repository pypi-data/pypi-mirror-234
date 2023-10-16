from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CqrsEntityDefaultGenerator(CodeGenerator):

    def get_target(self):
        return "{}Entity.java".format(self.capitalize)

    def get_template(self):
        return tpl.CQRS_DEFAULT_ENTITY

    def get_source(self):
        return src.CQRS_ENTITIES
