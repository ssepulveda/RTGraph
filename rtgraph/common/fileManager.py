import os


class FileManager:
    """
    Wrappers for file operations.
    """

    @staticmethod
    def create_dir(path=None):
        """
        Creates a directory if the specified doesn't exists.
        :param path: Directory name or full path.
        :type path: basestring.
        :return: True if the specified directory exists.
        :rtype: bool.
        """
        if path is not None:
            if not os.path.isdir(path):
                os.makedirs(path)
        return os.path.isdir(path)

    @staticmethod
    def create_file(filename, extension="txt", path=None):
        """
        Creates a file full path based on parameters.
        :param filename: Name for the file.
        :type filename: basestring.
        :param extension: Extension for the file.
        :type extension: basestring.
        :param path: Path for the file, if needed.
        :type path: basestring.
        :return: Full path for the specified file.
        :rtype: basestring.
        """
        if path is None:
            full_path = str("{}.{}".format(filename, extension))
        else:
            full_path = str("{}/{}.{}".format(path, filename, extension))
        return full_path

    @staticmethod
    def file_exists(filename):
        """
        Checks if a file exists.
        :param filename: Name of the file, including path.
        :type filename: basestring.
        :return: True if the file exists.
        :rtype: bool.
        """
        if filename is not None:
            return os.path.isfile(filename)
