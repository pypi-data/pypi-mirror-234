from pathlib import Path
from sys import platform
from packaging import version


class File:
    @staticmethod
    def temp_dir():
        home = str(Path.home())
        is_win = platform.startswith("win")
        if is_win:
            return "%s\\AppData\\Local\\Temp\\Robomotion" % home
        return "/tmp/robomotion"


class Version:
    @staticmethod
    def is_version_less_than(ver: str, other: str) -> bool:
        v = version.parse(ver)
        v2 = version.parse(other)
        return v < v2
