import tarfile
import os


class TarGzExtractor:
    """
    Class for extract and delete zip file.
    """

    def __init__(self, file_path, gui=False):
        self.file_path = file_path
        self.gui = gui

    def extract(self):
        """
        Extract downloaded file from Spring Starter.
        """
        if not self.gui:
            target = os.getcwd()
        else:
            target = "/tmp/sb"

        with tarfile.open(self.file_path, "r:gz") as tar:
            tar.extractall(target)

    def delete(self):
        """
        Delete tar.gz file extracted.
        """
        os.remove(self.file_path)
