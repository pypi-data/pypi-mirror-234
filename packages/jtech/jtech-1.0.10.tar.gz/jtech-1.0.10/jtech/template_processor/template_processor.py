import os
import pkg_resources
from jinja2 import Environment


class TemplateProcessor:
    """
    Class Jinja2 Processor. Read template file and change values.
    """

    def __init__(self, template_file, target_dir):
        self.template_file = template_file
        self.target_dir = target_dir

    def process_template(self, data, target_filename):
        """
        Process template file
        :param data: Data to change in template .tlp
        :param target_filename: Target file name .java
        :return: Created file.
        """
        template_content = pkg_resources.resource_string(__name__, self.template_file).decode("utf-8")
        template = Environment().from_string(template_content)

        rendered_content = template.render(data)
        target_file = os.path.join(self.target_dir, target_filename)

        with open(target_file, "w") as file:
            file.write(rendered_content)
