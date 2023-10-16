import os

from jtech.template_processor.template_processor import TemplateProcessor


class Processor:
    def __init__(self, project_dir, data):
        self.project_dir = project_dir
        self.data = data

    def exec(self, template_name, source, target):
        tpl_name = "../resources/tpl/{}.tpl".format(template_name)
        tpl_folder = os.path.join(self.project_dir, source)
        processor = TemplateProcessor(tpl_name, tpl_folder)
        processor.process_template(self.data, target)
