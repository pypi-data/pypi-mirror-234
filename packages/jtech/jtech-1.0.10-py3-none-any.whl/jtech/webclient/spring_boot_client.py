import requests


class SpringBootWebClient:
    """
    WebClient for create Spring Boot Project base
    """

    def request(self, project):
        """
        Request to Spring Start a project base
        :param self:
        :param project: Project data
        """
        template = requests.Session()
        parts = project.get_name().split("-")
        name = parts[-1]
        builder = f"https://start.spring.io/starter.tgz"
        query_params = {
            "dependencies": ",".join(project.get_dependencies()),
            "type": "gradle-project",
            "language": "java",
            "packageName": project.get_package(),
            "bootVersion": project.get_spring(),
            "baseDir": project.get_name(),
            "groupId": project.get_group(),
            "artifactId": project.get_artifact(),
            "name": project.get_name(),
            "javaVersion": project.get_java(),
            "packaging": "jar",
            "applicationName": f"Start{name.capitalize()}"
        }
        response = template.post(builder, params=query_params)
        return response.content
