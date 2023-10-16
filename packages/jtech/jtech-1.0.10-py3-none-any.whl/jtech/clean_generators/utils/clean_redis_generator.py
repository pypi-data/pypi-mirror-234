from jtech.generator.code_generator import CodeGenerator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CleanRedisGenerator(CodeGenerator):
    """
    Class for Create RedisConfiguration Java Class
    """

    def get_target(self):
        return "RedisConfiguration.java"

    def get_template(self):
        return tpl.CLEAN_REDIS

    def get_source(self):
        return src.CLEAN_CONFIG_INFRA_REDIS
