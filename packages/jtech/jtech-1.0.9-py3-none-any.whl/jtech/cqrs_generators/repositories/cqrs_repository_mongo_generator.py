import getpass
import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.template_processor.processor import Processor


class CqrsRepositoryMongoGenerator:
    """
        Generate CQRS Mongo Repository

        :param params: Java package for change in template.
        :param project: Project name for use in lowercase.
        :param capitalize: Project name for use in uppercase.
        :param folder: Source for create java file.
        """

    def __init__(self, params, project, capitalize, folder):
        self.params = params
        self.project = project
        self.capitalize = capitalize
        self.folder = folder

    def generate(self):
        """Generate an interface {{Project}}Repository.java extended to JpaRepository"""
        target_filename = self.capitalize + "Repository.java"
        data = {
            "package": self.params.package,
            "className": self.capitalize,
            "project": self.folder,
            "username": getpass.getuser()
        }
        generator = Processor(self.folder, data)
        generator.exec(tpl.CQRS_REPOSITORY_MONGO, src.CQRS_REPOSITORIES, target_filename)
