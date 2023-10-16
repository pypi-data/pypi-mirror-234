import json

import questionary
import getpass

import requests
from bs4 import BeautifulSoup


class ProjectMetadataWizard:
    """
    Metadata for create project.
    """

    def __init__(self, project_name):
        self.project_name = project_name
        self.project_user = getpass.getuser()
        self.project_group = None
        self.project_artifact = None
        self.project_description = None
        self.project_package = None
        self.project_java = None
        self.project_spring = None

    def get_available_java_versions(self):
        url = "https://start.spring.io/"
        response = requests.get(url)
        if response.status_code == 200:
            parsed = json.loads(response.content)
            ids_array = []
            java_versions = parsed['javaVersion']
            values_list = java_versions['values']
            for value in values_list:
                ids_array.append(value['id'])
            return ids_array
        return ['1.8', '17', '20']

    def get_boot_versions(self):
        url = "https://start.spring.io/"
        response = requests.get(url)
        if response.status_code == 200:
            parsed = json.loads(response.content)
            values = parsed['bootVersion']['values']
            ids = [value['name'] for value in values if 'M' not in value['name'] and 'SNAPSHOT' not in value['name']]
            return ids
        return ['3.0.9', '3.1.1', '2.7.14']

    def prompt_project_details(self):
        """
        Prompt to create Spring Boot project.
        """
        if self.project_name:
            self.project_name = questionary.text("Project name: ", default=self.project_name).ask()
        else:
            self.project_name = questionary.text("Project name: ").ask()

        self.project_group = questionary.text("Project Group:", default="br.com.sansys.services").ask()
        self.project_artifact = self.project_name
        self.project_description = questionary.text("Project Description:", default="Jtech Microservices v1.0").ask()
        package_default = self.project_group.replace("-", ".") + "." + self.project_artifact.replace("-", ".")
        self.project_package = questionary.text("Project package:", default=package_default).ask()
        self.project_java = questionary.select(
            "Select Java Version:",
            choices=self.get_available_java_versions(),
            default=self.get_available_java_versions()[0]
        ).ask()
        self.project_spring = questionary.select(
            "Select Spring Boot Version:",
            choices=self.get_boot_versions(),
            default=self.get_boot_versions()[0]
        ).ask()
        if not self.project_package:
            self.project_package = package_default

    def run(self):
        """
        Run prompt above.
        """
        self.prompt_project_details()
