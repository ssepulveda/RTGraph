import os


class FileManager:
    @staticmethod
    def create_dir(path=None):
        if path is not None:
            if not os.path.isdir(path):
                os.makedirs(path)
        return os.path.isdir(path)

    @staticmethod
    def create_file(filename, extension="txt", path=None):
        if path is None:
            full_path = str("{}.{}".format(filename, extension))
        else:
            full_path = str("{}/{}.{}".format(path, filename, extension))
        return full_path

    @staticmethod
    def file_exists(filename):
        if filename is not None:
            return os.path.isfile(filename)
