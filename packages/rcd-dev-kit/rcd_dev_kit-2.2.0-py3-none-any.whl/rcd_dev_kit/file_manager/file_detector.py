import os
from typing import List


def detect_path(path: str) -> None:
    """
    Function detect_path.
    Detect if a path exsit, if not then create it.

    Parameters:
          path (str): The path of a directory.

    Examples:
        >>> from rcd_dev_kit import file_manager
        >>> file_manager.detect_path("my_path")
    """
    if os.path.isdir(path):
        print(f'🥂Path "{path}" exists.')
    else:
        print(f'👉🏻Path "{path}" does not exist, creating...')
        os.makedirs(path)


def detect_all_files(root_path: str, full_path: bool = False) -> List:
    """
    Function detect_all_files.
    Detect if a path exsit, if not then create it.

    Parameters:
          root_path (str): The path of a root directory.
          full_path (bool, default False): True return full file path, False return only file name.

    Examples:
        >>> from rcd_dev_kit import file_manager
        >>> file_manager.detect_all_files(root_path="my_path")
    """
    lst_path = list()
    for root, directories, files in os.walk(root_path):
        for name in files:
            file_path = os.path.join(root, name)
            if os.path.isfile(file_path) and not name.startswith("~$"):
                lst_path.append(file_path)
        for name in directories:
            dir_path = os.path.join(root, name)
            if os.path.isdir(dir_path) and not name.startswith("~$"):
                lst_path.append(dir_path)

    if full_path is True:
        lst_file_path = [path for path in lst_path if os.path.isfile(path)]
    else:
        lst_file_path = [
            path.split(os.path.sep)[-1] for path in lst_path if os.path.isfile(path)
        ]

    return lst_file_path
