import os
import pathlib
from typing import Dict, Iterable, Optional, Union


def get_py_files(root_dir: Optional[Union[str, pathlib.Path]] = None) -> Iterable[pathlib.Path]:
    """Get all python-files recursively from a directory

    Args:
        root_dir: Directory to search

    Returns:
        Iterator for all python-files
    """
    if root_dir is None:
        root_dir = os.getcwd()

    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)


def get_py_files_abs2rel_mapping(
    root_dir: Optional[Union[str, pathlib.Path]] = None, prefix: Optional[str] = ""
) -> Dict[pathlib.Path, pathlib.Path]:
    """Get dict which maps result of get_py_files from absolute to relative path

    Args:
        root_dir: Root directory to search for .py-files in
        prefix: Relative path prefix

    Returns:
        Dictionary of python-files mapped from absolute to relative path
    """
    if root_dir is None:
        root_dir = os.getcwd()

    return {f: prefix + f[len(root_dir) + 1 :] for f in get_py_files(root_dir)}
