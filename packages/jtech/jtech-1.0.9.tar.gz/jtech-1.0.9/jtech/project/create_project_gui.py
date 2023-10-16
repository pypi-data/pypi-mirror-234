from jtech.project.create_project import CreateProject
from jtech.wizards.project import Project


class CreateProjectGui:
    def __init__(self, project_name,
                 group,
                 artifact,
                 package,
                 java_version,
                 spring_boot_version,
                 dependencies,
                 banner_text,
                 architecture,
                 choice_with_samples):
        self.banner_text = banner_text
        self.dependencies = dependencies
        self.spring_boot_version = spring_boot_version
        self.java_version = java_version
        self.package = package
        self.artifact = artifact
        self.group = group
        self.project_name = project_name
        self.architecture = architecture
        self.choice_with_samples = choice_with_samples

    def create(self):
        cp = CreateProject()

        project = Project(self.project_name,
                          self.group,
                          self.artifact,
                          self.package,
                          self.java_version,
                          self.spring_boot_version,
                          self.dependencies.split(","),
                          self.banner_text, True)
        filename = cp.download_default_project(project)
        cp.extract_default_project_and_delete_zip(filename, project.gui)
        if self.architecture == "Clean Architecture":
            cp.create_clean_architecture(project, self.choice_with_samples, self.dependencies)
        if self.architecture == "CQRS":
            cp.create_cqrs_architecture(project, self.choice_with_samples, self.dependencies)

        cp.manipulate_build_gradle(project, self.dependencies)
        cp.create_gradle_properties(project)
        cp.remove_unnecessary_files(project)

