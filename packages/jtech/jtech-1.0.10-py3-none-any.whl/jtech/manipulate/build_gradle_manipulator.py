import fileinput
import re


class BuildGradleManipulator:
    """
    Update a build.gradle file for Jtech parameters
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def add_repository(self, repository_url):
        """
        Add Jtech nexus repository        :param repository_url:  nexus
        :return: repository added.
        """
        line_exists = False
        new_line = f'\tmaven {{ url "{repository_url}" }}'

        inside_repositories = False
        inserted = False

        for line in fileinput.input(self.file_path, inplace=True):
            if line.strip() == 'repositories {':
                inside_repositories = True
            elif line.strip() == '}':
                inside_repositories = False

            if inside_repositories and not inserted and line.strip() == 'mavenCentral()':
                inserted = True
                print(new_line)

            print(line, end='')

        fileinput.close()

        if not inserted:
            with open(self.file_path, 'a') as file:
                file.write('\n' + new_line + '\n')

    def update_version(self, new_version):
        """
        Add APP_VERSION from gradle.properties
        :param new_version: APP_VERSION from gradle.properties
        :return:
        """
        with open(self.file_path, "r") as file:
            build_gradle_content = file.read()

        updated_build_gradle_content = re.sub(r"version\s*=\s*['\"]0\.0\.1-SNAPSHOT['\"]", f"version = {new_version}",
                                              build_gradle_content)

        with open(self.file_path, "w") as file:
            file.write(updated_build_gradle_content)

    def add_publishing(self):
        """
        Add publishing repository
        :return:
        """
        publishing_block = '''
publishing {
    publications {
        mavenJava(MavenPublication) {
            groupId = group
            artifactId = rootProject.name
            version = version
            from components.java
        }
    }
    repositories {
        maven {
            name 'nexus'
            url = 'https://nexus.jtech.com.br/repository/maven-' + (version.endsWith('SNAPSHOT') ? 'snapshots/' : 'releases/')
            credentials {
                username System.getenv("MAVEN_REPO_USER")
                password System.getenv("MAVEN_REPO_PASS")
            }
        }
    }
}
'''
        with open(self.file_path, "a") as file:
            file.write(publishing_block)

    def add_plugin_ids(self):
        """
        Add plugins ID
        :return:
        """
        plugin_ids = "id 'eclipse'\n    id 'maven-publish'\n    id 'jacoco'"

        with open(self.file_path, "r") as file:
            build_gradle_content = file.read()

        updated_build_gradle_content = re.sub(r"plugins\s*{", f"plugins {{\n    {plugin_ids}\n", build_gradle_content)

        with open(self.file_path, "w") as file:
            file.write(updated_build_gradle_content)

    def add_dependencies(self, dependencies, tests=False, is_mongodb=False):
        """
                Add a list of dependencies to the build.gradle file.

                :param dependencies: List of dependencies to add.
                :param tests: Add tests libs
                :param is_mongodb: Verify if jpa for not use Mongo
                """
        inside_dependencies = False

        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        with open(self.file_path, 'w') as file:
            for line in lines:
                file.write(line)
                if line.strip() == 'dependencies {':
                    inside_dependencies = True
                    for dependency in dependencies:
                        if re.search(r'\blombok\b', dependency):
                            file.write(f'\tcompileOnly "{dependency}"\n')
                            file.write(f'\tannotationProcessor "{dependency}"\n')
                        else:
                            file.write(f'\timplementation "{dependency}"\n')

                    if tests:
                        file.write(f'\ttestImplementation "org.assertj:assertj-core:3.24.2"\n')
                        file.write(f'\ttestImplementation "com.google.code.bean-matchers:bean-matchers:0.14"\n')
                        file.write(f'\ttestImplementation "org.junit.platform:junit-platform-suite-engine:1.9.2"\n')
                        file.write(f'\ttestRuntimeOnly "com.h2database:h2"\n')

                    if is_mongodb:
                        file.write(f'\ttestImplementation "org.mongounit:mongounit:2.0.1"\n')

                elif inside_dependencies and line.strip() == '}':
                    inside_dependencies = False
