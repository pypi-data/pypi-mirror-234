import jtech.utils.dir_constants as source
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsRedisGenerator(CodeGenerator):
    """
    Generate Redis configuration
    """

    def get_target(self):
        return "RedisConfiguration.java"

    def get_template(self):
        return tpl.CQRS_REDIS

    def get_source(self):
        return source.CQRS_INFRA
