import os

import jtech.utils.dir_constants as const
from jtech.creators.gradle_properties_creator import PropertiesCreator
from jtech.docker_compose.generate_docker_compose import GenerateDockerCompose
from jtech.generator.application_yml_generator import ApplicationYmlGenerator
from jtech.generator.banner_generator import SpringBootBannerGenerator
from jtech.generator.base_dir_generator import BaseDirGenerator
from jtech.generator.clean_code_generator import CleanCodeGenerator
from jtech.manipulate.java_class_manipulator import JavaFileManipulator
from jtech.mockserver.mockserver import GenerateMockServer
from jtech.utils.file_remove import RemoveFile


class CleanArchitectureStructureCreator:
    """
    Generate clean architecture structure and sample files.

    :param param: DTO with all parameters.
    """

    def __init__(self, param):
        self.param = param

    def create_structure(self):
        composer_dir, mockserver_dir, project_dir, resources_dir, tests_dir, resources_tests_dir, project_tests_dir = self.generate_base_dirs()
        self.create_sub_dirs(project_dir, project_tests_dir)
        self.generate_docker_mockserver(composer_dir, mockserver_dir)
        real_name = self.create_samples(project_dir, project_tests_dir)
        self.remove_application_properties(resources_dir)
        os.mkdir(resources_tests_dir)
        self.add_application_properties_test(os.path.join(resources_tests_dir, "application-test.properties"))
        self.create_yaml(os.path.join(resources_dir, "application.yml"), real_name, self.param.package)
        self.create_docker_composer(composer_dir)
        self.create_mockserver(mockserver_dir)
        self.create_banner(resources_dir)

    def create_yaml(self, file, project, package):
        application_yml = ApplicationYmlGenerator(self.param, file, project, package)
        application_yml.generate()

    def generate_samples(self, project_name, capitalize, project_dir, project_tests_dir):
        """Generate Clean Architecture sample files."""
        generator = CleanCodeGenerator(self.param, project_name, capitalize, project_dir, project_tests_dir)
        generator.all()
        manipulator = JavaFileManipulator(os.path.join(project_dir, "Start{}.java".format(capitalize)))
        manipulator.manipulate_clean_arch(self.param)

    def generate_base_dirs(self):
        dirs = BaseDirGenerator(self.param)
        return dirs.generate()

    def create_sub_dirs(self, project_dir, project_tests_dir):
        """ Create sub dirs in the project"""
        sub_dirs = [
            const.CLEAN_DOMAINS,
            const.CLEAN_USECASE,
            const.CLEAN_PORT_INPUT,
            const.CLEAN_PORT_OUTPUT,
            const.CLEAN_ADAPTERS_INPUT_CONTROLLERS,
            const.CLEAN_ADAPTERS_INPUT_HANDLERS,
            const.CLEAN_ADAPTERS_INPUT_PROTOCOLS,
            const.CLEAN_ADAPTERS_OUTPUT_ENTITIES,
            const.CLEAN_CONFIG_INFRA_SWAGGER,
            const.CLEAN_CONFIG_INFRA_UTILS,
            const.CLEAN_CONFIG_INFRA_EXCEPTIONS,
            const.CLEAN_CONFIG_INFRA_HANDLERS,
            const.CLEAN_CONFIG_INFRA_LISTENERS,
            const.CLEAN_CONFIG_USECASES
        ]

        for sub_dir in sub_dirs:
            os.makedirs(os.path.join(project_dir, sub_dir), exist_ok=True)
            os.makedirs(os.path.join(project_tests_dir, sub_dir), exist_ok=True)

        if self.param.kafka:
            os.makedirs(os.path.join(project_dir, const.CLEAN_CONFIG_INFRA_KAFKA), exist_ok=True)

        if self.param.redis:
            os.makedirs(os.path.join(project_dir, const.CLEAN_CONFIG_INFRA_REDIS), exist_ok=True)

    def generate_docker_mockserver(self, composer_dir, mockserver_dir):
        os.makedirs(composer_dir, exist_ok=True)
        os.makedirs(mockserver_dir, exist_ok=True)

    def create_samples(self, project_dir, project_tests_dir):
        names = self.param.project.split("-")
        project = names[-1]
        capitalize = project[0].upper() + project[1:]
        if self.param.samples:
            self.generate_samples(project, capitalize, project_dir, project_tests_dir)
            self.remove_default_test(os.path.join(project_tests_dir, "Start{}Tests.java".format(capitalize)))
        return project

    def remove_default_test(self, param):
        remover = RemoveFile(param)
        remover.remove()

    def remove_application_properties(self, resources_dir):
        application_properties = RemoveFile(os.path.join(resources_dir, "application.properties"))
        application_properties.remove()

    def add_application_properties_test(self, file):
        creator = PropertiesCreator(file)
        creator.create_test_properties()

    def create_docker_composer(self, composer_dir):
        docker_compose = GenerateDockerCompose(path=os.path.join(composer_dir, 'docker-compose.yml'), param=self.param)
        docker_compose.generate()

    def create_mockserver(self, mockserver_dir):
        mockserver = GenerateMockServer(path=mockserver_dir, param=self.param)
        mockserver.generate()

    def create_banner(self, resources_dir):
        banner = SpringBootBannerGenerator(self.param.banner_text, resources_dir)
        banner.generate_banner()
