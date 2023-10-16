import os


class BaseDirGenerator:
    def __init__(self, param):
        self.param = param

    def generate(self):
        main_dir = os.path.join(self.param.base_dir, "src/main/java")
        resources_dir = os.path.join(self.param.base_dir, "src/main/resources")

        resources_tests_dir = os.path.join(self.param.base_dir, "src/test/resources")
        tests_dir = os.path.join(self.param.base_dir, "src/test/java")

        package_dir = self.param.package.replace(".", "/")
        project_dir = os.path.join(main_dir, package_dir)
        project_tests_dir = os.path.join(tests_dir, package_dir)

        composer_dir = os.path.join(self.param.base_dir, "composer")
        mockserver_dir = os.path.join(self.param.base_dir, "mockserver")
        return composer_dir, mockserver_dir, project_dir, resources_dir, tests_dir, resources_tests_dir, project_tests_dir
