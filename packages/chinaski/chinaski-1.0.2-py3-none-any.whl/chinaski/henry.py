import ntpath
import os
import pathlib
from typing import Union

import chinaski.read_lines as rl
from chinaski.finder import find_emails_in_line
from chinaski.is_email import Result, is_email

IGNORED_FOLDERS = [".git", ".idea", ".pytest_cache", "__pycache__"]


def path_leaf(path: str) -> str:
    """Retrieves the file name and extension from a given path.

    It should work in different OS.

    Obtained from:
    https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format

    :param path: path to retrieve the file from
    :return: str with the file name and extension
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class PathToFileOrDirIsNotValidException(Exception):
    def __init__(self, message="The given path to file or dir is not valid"):
        super().__init__(message)


def obtain_list_of_files(path_to_file_or_dir: Union[pathlib.Path, str]) -> list:
    """Given the path being a file, it will return a list containing 1 item,
    which is the path to that file. Given the path being a directory, it will
    return a list of every file in that directory and its subdirectories.

    There are some ignored folders/paths, since they bring no value
    right now.

    :param path_to_file_or_dir: Path to file or directory to retrieve
        all the files in it
    :return: List of paths to files to scan
    """
    list_of_files = []

    if any(ignored_folder for ignored_folder in IGNORED_FOLDERS if ignored_folder in str(path_to_file_or_dir)):
        return list_of_files

    if not os.path.isdir(path_to_file_or_dir):
        list_of_files.append(path_to_file_or_dir)

    files = pathlib.Path(path_to_file_or_dir).glob("*")
    for file in files:
        if os.path.isdir(file):
            list_of_files += obtain_list_of_files(file)
        else:
            list_of_files.append(file)

    return list_of_files


def assert_given_path_is_valid(path_to_file_or_dir: str) -> None:
    """Asserts the given path_to_file_or_dir is valid. That is, not an empty
    str and not None.

    :param path_to_file_or_dir: entry to check
    :return: None or raises PathToFileOrDirIsNotValidException if it's
        not valid.
    """
    if path_to_file_or_dir == "" or path_to_file_or_dir is None:
        raise PathToFileOrDirIsNotValidException


def core(path_to_file_or_dir: str) -> list[Result]:
    """Core function of the program.

    It will read the lines from each file given in the path and return a
    list of Result where it has found emails.

    :param path_to_file_or_dir: path to file or directory to detect
        emails in it
    :return: list of Result, containing the findings
    """
    assert_given_path_is_valid(path_to_file_or_dir)

    results = []
    list_of_files = obtain_list_of_files(path_to_file_or_dir)
    for file in list_of_files:
        lines = rl.read_lines_from_file(filename=file)
        file_name = path_leaf(file)

        for i in range(len(lines)):
            line = lines[i]
            emails_in_line = find_emails_in_line(line)

            for email in emails_in_line:
                res = is_email(line=email, line_number=i + 1, file_name=file_name)
                if res:
                    results.append(res)

    return results
