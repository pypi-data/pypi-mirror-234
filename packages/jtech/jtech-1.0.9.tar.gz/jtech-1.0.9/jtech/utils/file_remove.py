import os


class RemoveFile:
    """
    Class for remove HELP.md created by Spring Boot
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def remove(self):
        """
        Remove HELP.md from project.
        """
        os.remove(self.file_path)
