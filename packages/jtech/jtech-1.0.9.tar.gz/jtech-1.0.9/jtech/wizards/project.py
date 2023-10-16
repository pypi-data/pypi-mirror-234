class Project:
    """
    Project representation.
    """

    def __init__(self, name, group, artifact, package, java, spring, dependencies, banner, gui=False):
        self.name = name
        self.group = group
        self.package = package
        self.artifact = artifact
        self.java = java
        self.dependencies = dependencies
        self.spring = spring
        self.banner = banner
        self.gui = gui

    def get_spring(self):
        return self.spring

    def get_name(self):
        return self.name

    def get_group(self):
        return self.group

    def get_artifact(self):
        return self.artifact

    def get_package(self):
        return self.package

    def get_java(self):
        return self.java

    def get_dependencies(self):
        return self.dependencies
