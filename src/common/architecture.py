import platform
import sys

from enum import Enum


class Architecture:
    @staticmethod
    def get_os():
        tmp = str(Architecture.get_os_string())
        if "Linux" in tmp:
            return OSType.linux
        elif "Windows" in tmp:
            return OSType.windows
        elif "Darwin" in tmp:
            return OSType.macosx
        else:
            return OSType.unknown

    @staticmethod
    def get_os_string():
        return platform.platform()

    @staticmethod
    def get_path():
        return sys.path[0]

    @staticmethod
    def get_python_version():
        return sys.version[0:5]


class OSType(Enum):
    linux = 1
    macosx = 2
    windows = 3
    unknown = 0

