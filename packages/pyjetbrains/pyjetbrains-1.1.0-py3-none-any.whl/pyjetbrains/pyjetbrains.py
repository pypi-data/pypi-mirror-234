import os.path
from subprocess import run as processrun, call as processcall, DEVNULL, CREATE_NO_WINDOW, PIPE
from enum import Enum

import winapps


class IDEInfo:
    def __init__(self, folderName, cmd):
        self.folderName = folderName
        self.cmd = cmd

    def __is_toolbox(self):
        return processcall(f"where.exe {self.cmd}", shell=True, stdout=DEVNULL, stderr=DEVNULL, creationflags=CREATE_NO_WINDOW) == 0

    def is_installed(self):
        return len(list(winapps.search_installed(self.folderName))) > 0 or self.__is_toolbox()

    def exec_path(self):
        if not self.is_installed():
            return None
        if self.__is_toolbox():
            return processrun("where.exe pycharm", shell=True, stderr=DEVNULL, stdout=PIPE, creationflags=CREATE_NO_WINDOW).stdout.decode("utf-8")[:-2]
        binFolder = os.path.join(next(winapps.search_installed(self.folderName)).install_location, "bin")
        return os.path.join(binFolder, [l for l in os.listdir(binFolder) if l.endswith("64.exe")][0])


class IDE(Enum):
    """
    Enumeration of all IDEs to use in all pyjetbrains functions
    """
    PYCHARM = IDEInfo("PyCharm","pycharm")
    """IDE for Python"""
    INTELLIJ_IDEA = IDEInfo("IntelliJ IDEA","idea")
    """IDE for Java"""
    PHPSTORM = IDEInfo("PhpStorm","phpstorm")
    """IDE for PHP"""
    RIDER = IDEInfo("JetBrains Rider","rider")
    """IDE for C#"""
    WEBSTORM = IDEInfo("WebStorm","webstorm")
    """IDE for HTML, CSS and JS"""
    CLION = IDEInfo("CLion","clion")
    """IDE for C and C++"""
    GOLANG = IDEInfo("GoLang","golang")
    """IDE for GoLang"""
    RUBYMINE = IDEInfo("RubyMine","rubymine")
    """IDE for Ruby"""


class IDENotFoundError(Exception):
    __module__ = Exception.__module__


def is_installed(ide):
    """
    Checks if provided IDE is installed on device.
    :param ide: JetBrains IDE as type of Enumeration
    :return: true if IDE is installed, false otherwise
    """
    if not isinstance(ide, IDE):
        raise TypeError("ide parameter is not type of IDE")
    return ide.value.is_installed()


def open(ide, *paths, line=None, column=None):
    """
    Open an arbitrary file or folder in IDE, optionally specifying where to put the caret after opening.

    When you specify the path to a file, IDE opens it in the LightEdit mode, unless it belongs to a project that is already open or there is special logic to automatically open or create a project (for example, in case of Maven or Gradle files). If you specify a directory with an existing project, IDE opens this project. If you open a directory that is not a part of a project, IDE adds the .idea directory to it, making it a project.

    :param ide: IDE you want to open files with
    :param paths: Paths to files or folders you want to open
    :param line: Line position of caret cursor
    :param column: Column position of caret cursor
    :raise IDENotFoundError: if IDE is not installed on this device
    """
    if not is_installed(ide):
        raise IDENotFoundError(f"IDE '{ide.name}' is not installed on this device.")
    for path in paths:
        if not isinstance(path, str):
            raise ValueError(f"Expected str, got {type(path)} with value {path}")
    cmd = [ide.value.exec_path()]
    if line is not None and isinstance(line, int):
        cmd += ["--line", str(line)]
    if column is not None and isinstance(column, int):
        cmd += ["--column", str(column)]
    processrun(cmd + [*paths], creationflags=CREATE_NO_WINDOW, shell=True)


def compare_files(ide, path1, path2, path3=None):
    """
    Open the diff viewer to compare two or three files from the command line. For example, you can compare the current version of a file with its backup, or your local copy of a file with its copy from the remote repository or its copy from another branch.

    :param ide: IDE you want to open files with
    :param path1: First path of file of comparison
    :param path2: Second path of file of comparison
    :param path3: Third optional path of file of comparison
    """
    if not is_installed(ide):
        raise IDENotFoundError(f"IDE '{ide.name}' is not installed on this device.")
    for order, path in [("First", path1), ("Second", path2)]:
        if not os.path.isfile(path) or not os.path.exists(path):
            raise ValueError(f"{order} path is incorrect or does not exist!")
    cmd = [ide.value.exec_path(), "diff", path1, path2]
    if path3 is not None and os.path.isfile(path3) and os.path.exists(path3):
        cmd += [path3]
    processrun(cmd, creationflags=CREATE_NO_WINDOW, shell=True)


def format_files(ide, *paths, mask=None, recursive=None):
    """
    JetBrains IDE can format your code according to the configured code style settings. You can also apply your code style formatting to the specified files from the command line.

    The pyjetbrains launches an instance of IDE in the background and applies the formatting. It will not work if another instance of specific IDE is already running. In this case, you can perform code style formatting from the running instance. Use the pyjetbrains formatter for automated regular maintenance of a large codebase with many contributors to ensure a consistent coding style.

    :param ide: IDE you want to format files with
    :param paths: Paths to files or whole folders you want to format
    :param mask: Specify a comma-separated list of file masks that define the files to be processed. You can use the * (any string) and ? (any single character) wildcards.
    :param recursive: Process specified directories recursively.
    """
    if not is_installed(ide):
        raise IDENotFoundError(f"IDE '{ide.name}' is not installed on this device.")
    for path in paths:
        if not isinstance(path, str):
            raise ValueError(f"Expected str, got {type(path)} with value {path}")
    cmd = [ide.value.exec_path(), "format"]
    if mask is not None and isinstance(mask, str):
        cmd += ["-m", mask]
    if recursive is not None and isinstance(recursive, bool) and recursive:
        cmd += ["-r"]
    processrun(cmd + [*paths], creationflags=CREATE_NO_WINDOW, shell=True)
