from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CleanKafkaGenerator(CodeGenerator):
    """
    Class for Create Kafka Configuration Java Class
    """

    def get_target(self):
        return "KafkaConfiguration.java"

    def get_template(self):
        return tpl.CLEAN_KAFKA

    def get_source(self):
        return src.CLEAN_CONFIG_INFRA_KAFKA
