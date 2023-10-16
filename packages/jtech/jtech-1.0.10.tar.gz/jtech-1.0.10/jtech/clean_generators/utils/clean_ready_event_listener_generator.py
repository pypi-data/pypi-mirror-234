from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CleanReadyEventListenerGenerator(CodeGenerator):
    """
    Class for Create ReadyEventListener Java Class
    """

    def get_target(self):
        return "ReadyEventListener.java"

    def get_template(self):
        return tpl.CLEAN_READY_LISTENER

    def get_source(self):
        return src.CLEAN_CONFIG_INFRA_UTILS
