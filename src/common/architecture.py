import platform
import sys

from enum import Enum


class Architecture:
    """
    Wrappers for commons architecture specific methods
    """

    @staticmethod
    def get_os():
        """
        Gets the current OS type of the host.
        :return: OS type by OSType enum.
        """
        tmp = str(Architecture.get_os_name())
        if "Linux" in tmp:
            return OSType.linux
        elif "Windows" in tmp:
            return OSType.windows
        elif "Darwin" in tmp:
            return OSType.macosx
        else:
            return OSType.unknown

    @staticmethod
    def get_os_name():
        """
        Gets the current OS name string of the host.
        Host OS name as reported by platform.
        :return: OS name.
        """
        return platform.platform()

    @staticmethod
    def get_path():
        """
        Gets the PWD or CWD of the currently running application.
        :return: Path of the PWD or CWD.
        """
        return sys.path[0]

    @staticmethod
    def get_python_version():
        """
        Gets the running Python version (Major, minor, release).
        :return: Python version formated as major.minor.release.
        """
        version = sys.version_info
        return str("{}.{}.{}".format(version[0], version[1], version[2]))

    @staticmethod
    def is_python_version(major, minor=0):
        """
        Checks if the running Python version is equals or greater to the specified version.
        :param major: Major value of the version.
        :param minor: Minor value of the version.
        :return: True if the version specified is equal or greater than the current version.
        """
        version = sys.version_info
        if version[0] >= major and version[1] >= minor:
            return True
        return False


class OSType(Enum):
    """
    Enum to list OS types.
    """

    unknown = 0
    linux = 1
    macosx = 2
    windows = 3

