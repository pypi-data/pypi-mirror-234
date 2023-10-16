import os.path
import shutil
import tarfile


class GenerateMockServer:
    def __init__(self, param, path):
        self.param = param
        self.path = path

    def copy_http(self):
        src = os.path.join(os.path.dirname(__file__), '..', 'resources', 'mock', 'http.tar.gz')
        shutil.copy(src, self.path)

    def unzip(self, file):
        with tarfile.open(file, "r:gz") as tar:
            tar.extractall(self.path)
        os.remove(file)

    def generate(self):
        file = os.path.join(self.path, "http.tar.gz")
        self.copy_http()
        self.unzip(file)
