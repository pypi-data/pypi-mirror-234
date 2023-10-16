class ReadmeCreator:
    def __init__(self, file_path, project_name):
        self.file_path = file_path
        self.project_name = project_name

    def create_readme(self):
        content = f"![Jtech Logo](http://www.jtech.com.br/wp-content/uploads/2015/06/logo.png)\n\n"
        content += f"# {self.project_name}\n\n"
        content += "## What is\n\n"
        content += "## Composite by\n\n"
        content += "## Services\n\n"
        content += "## Helper\n\n"
        content += "## How to use\n\n"
        content += "## Sample\n\n"
        content += "## How to run\n\n"
        content += "## Points to improve"

        with open(self.file_path, "w") as file:
            file.write(content)
