"""Provide functions for dealing with files."""

import os
from pathlib import Path
from tempfile import gettempdir
from typing import Union


def print_file_contents(file_path: Union[str, Path]):
    """Print a file's contents to the console.
    :param file_path: a string or Path object
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    if file_path.is_file():
        print(f'File "{file_path}" found!')
        print(file_path.read_text(encoding="utf-8"))


def print_current_directory(print_yaml=False):
    """Print the contents of the current directory and its path
    :param bool print_yaml: should the contents of the yaml file be printed?
    """
    current_dir = os.getcwd()
    print(f"Current Working Directory: {current_dir}")
    if print_yaml:
        init_file = os.path.join(current_dir, "init.yaml")
        print_file_contents(init_file)


class CustomTempFile:
    def __init__(self, filename, delete: bool = True):
        self.temp_dir = gettempdir()
        self.temp_filename = os.path.join(self.temp_dir, filename)
        self.delete = delete
        self.temp_file = None

    def __enter__(self):
        # Open the file with read/write permissions
        self.temp_file = open(self.temp_filename, "w+")
        return self.temp_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the file
        if self.temp_file:
            self.temp_file.close()

        # Optionally, delete the file
        if self.delete:
            os.remove(self.temp_filename)
