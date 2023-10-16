import jtech.utils.dir_constants as source
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsKafkaGenerator(CodeGenerator):
    """
    Generate Kafka Configuration
    """

    def get_target(self):
        return "KafkaConfiguration.java"

    def get_template(self):
        return tpl.CQRS_KAFKA

    def get_source(self):
        return source.CQRS_INFRA
