import os


class FileManager:
    @staticmethod
    def create_dir(path=None):
        if path is not None:
            if not os.path.isdir(path):
                os.makedirs(path)
        return os.path.isdir(path)
