# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-01-19 19:23:57
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Compress methods.
"""


from typing import List, Optional
from zipfile import ZipFile, is_zipfile, ZIP_DEFLATED
from os import getcwd as os_getcwd, walk as os_walk
from os.path import (
    basename as os_basename,
    splitext as os_splitext,
    join as os_join,
    isdir as os_isdir,
    dirname as os_dirname,
)


__all__ = (
    "compress",
    "decompress",
    "rzip"
)


def compress(obj_path: str, build_dir: Optional[str] = None, overwrite: bool = True) -> None:
    """
    Compress file or folder.

    Parameters
    ----------
    obj_path : File or folder path.
    build_dir : Build directory.
        - `None` : Work directory.
        - `str` : Use this value.

    overwrite : Whether to overwrite.
    """

    # Handle parameter.
    if build_dir is None:
        build_dir = os_getcwd()
    if overwrite:
        mode = "w"
    else:
        mode = "x"

    # Generate build path.
    basename = os_basename(obj_path)
    build_name = os_splitext(basename)[0]
    build_name += ".zip"
    build_path = os_join(build_dir, build_name)

    # Compress.
    with ZipFile(build_path, mode, ZIP_DEFLATED) as zip_file:
        zip_file.write(obj_path)
        is_dir = os_isdir(obj_path)

        ## Recursive compress.
        if is_dir:
            dirname = os_dirname(obj_path)
            dirname_len = len(dirname)
            dirs = os_walk(obj_path)
            for folder_name, sub_folders_name, files_name in dirs:
                for sub_folder_name in sub_folders_name:
                    sub_folder_path = os_join(folder_name, sub_folder_name)
                    zip_path = sub_folder_path[dirname_len:]
                    zip_file.write(sub_folder_path, zip_path)
                for file_name in files_name:
                    file_path = os_join(folder_name, file_name)
                    zip_path = file_path[dirname_len:]
                    zip_file.write(file_path, zip_path)


def decompress(obj_path: str, build_dir: Optional[str] = None, password: Optional[str] = None) -> None:
    """
    Decompress compressed object.

    Parameters
    ----------
    obj_path : Compressed object path.
    build_dir : Build directory.
        - `None` : Work directory.
        - `str` : Use this value.

    passwrod : Unzip Password.
        - `None` : No Unzip Password.
        - `str` : Use this value.
    """

    # Check object whether can be decompress.
    is_support = is_zipfile(obj_path)
    if not is_support:
        raise AssertionError("file format that cannot be decompressed")

    # Handle parameter.
    if build_dir is None:
        build_dir = os_getcwd()

    # Decompress.
    with ZipFile(obj_path) as zip_file:
        zip_file.extractall(build_dir, pwd=password)


def rzip(obj_path: str, build_dir: Optional[str] = None) -> None:
    """
    Automatic judge and compress or decompress object.

    Parameters
    ----------
    obj_path : File or folder or compressed object path.
    output_path : Build directory.
        - `None` : Work directory.
        - `str` : Use this value.
    """

    # Judge compress or decompress.
    is_support = is_zipfile(obj_path)

    # Execute.
    if is_support:
        decompress(obj_path, build_dir)
    else:
        compress(obj_path, build_dir)