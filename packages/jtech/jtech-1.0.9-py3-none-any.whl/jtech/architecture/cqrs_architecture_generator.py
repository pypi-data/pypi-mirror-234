import os

from jtech.creators.gradle_properties_creator import PropertiesCreator
from jtech.generator.application_yml_generator import ApplicationYmlGenerator
from jtech.generator.banner_generator import SpringBootBannerGenerator
from jtech.generator.base_dir_generator import BaseDirGenerator
from jtech.generator.cqrs_code_generator import CqrsCodeGenerator
from jtech.docker_compose.generate_docker_compose import GenerateDockerCompose
from jtech.manipulate.application_yml_manipulator import ApplicationYmlManipulator
from jtech.manipulate.java_class_manipulator import JavaFileManipulator
from jtech.mockserver.mockserver import GenerateMockServer
from jtech.utils.file_remove import RemoveFile
import jtech.utils.dir_constants as const


class CqrsArchitectureStructureCreator:
    """
    Generate cqrs architecture structure and sample files.

    param: param DTO with all parameters.
    """

    def __init__(self, param):
        self.param = param

    def create_structure(self):
        """Create folder structure."""
        composer_dir, mockserver_dir, project_dir, resources_dir, test_dir, resources_test_dir, project_test_dir = self.generate_base_folder()
        self.create_subfolders(project_dir, project_test_dir)
        self.generate_docker_mockserver(composer_dir, mockserver_dir)
        real_name = self.create_samples(project_dir, project_test_dir)
        self.remove_application_properties(resources_dir)
        os.mkdir(resources_test_dir)
        self.add_application_properties_test(os.path.join(resources_test_dir, "application-test.properties"))
        self.create_yaml(os.path.join(resources_dir, "application.yml"), real_name, self.param.package)
        self.create_docker_compose(composer_dir)
        self.create_mockserver(mockserver_dir)
        self.create_banner(resources_dir)

    def generate_docker_mockserver(self, composer_dir, mockserver_dir):
        os.makedirs(composer_dir, exist_ok=True)
        os.makedirs(mockserver_dir, exist_ok=True)

    def generate_base_folder(self):
        dirs = BaseDirGenerator(self.param)
        return dirs.generate()

    def create_samples(self, folder, test_folder):
        names = self.param.project.split("-")
        project = names[-1]
        capitalize = project[0].upper() + project[1:]
        if self.param.samples:
            self.generate_samples(project, capitalize, folder, test_folder)
            self.remove_default_test(os.path.join(test_folder, "Start{}Tests.java".format(capitalize)))
        return project

    def remove_application_properties(self, resources_dir):
        application_properties = RemoveFile(os.path.join(resources_dir, "application.properties"))
        application_properties.remove()

    def create_docker_compose(self, composer_dir):
        docker_compose = GenerateDockerCompose(path=os.path.join(composer_dir, 'docker-compose.yml'), param=self.param)
        docker_compose.generate()

    def create_mockserver(self, mockserver_dir):
        mockserver = GenerateMockServer(path=mockserver_dir, param=self.param)
        mockserver.generate()

    def create_subfolders(self, project_dir, project_test_dir):
        """Create subfolders in the project directory."""
        subfolders = [
            const.CQRS_AGGREGATE_IMPL,
            const.CQRS_CONTROLLERS_COMMANDS,
            const.CQRS_CONTROLLERS_QUERIES,
            const.CQRS_ENTITIES,
            const.CQRS_INFRA,
            const.CQRS_INFRA_EXCEPTIONS,
            const.CQRS_PROTOCOLS,
            const.CQRS_REPOSITORIES,
            const.CQRS_COMMAND,
            const.CQRS_SERVICES_COMMANDS_IMPL,
            const.CQRS_QUERY,
            const.CQRS_SERVICES_QUERIES_IMPL,
            const.CQRS_UTILS,
            const.CQRS_VALIDATOR
        ]

        for subfolder in subfolders:
            os.makedirs(os.path.join(project_dir, subfolder), exist_ok=True)
            os.makedirs(os.path.join(project_test_dir, subfolder), exist_ok=True)

    def create_yaml(self, file, project, package):
        application_yml = ApplicationYmlGenerator(self.param, file, project, package)
        application_yml.generate()

    def generate_samples(self, project, capitalize, folder, test_folder):
        generator = CqrsCodeGenerator(self.param, project, capitalize, folder, test_folder)
        generator.all()
        manipulator = JavaFileManipulator(os.path.join(folder, "Start{}.java".format(capitalize)))
        manipulator.manipulate_cqrs_arch(self.param)

    def add_application_properties_test(self, file):
        creator = PropertiesCreator(file)
        creator.create_test_properties()

    def remove_default_test(self, file):
        remover = RemoveFile(file)
        remover.remove()

    def create_banner(self, resources_dir):
        banner = SpringBootBannerGenerator(self.param.banner_text, resources_dir)
        banner.generate_banner()
