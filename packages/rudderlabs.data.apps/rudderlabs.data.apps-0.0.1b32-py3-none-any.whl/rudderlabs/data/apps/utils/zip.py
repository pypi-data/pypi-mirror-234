#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compress and decompress a directory."""

import os
import tempfile
import zipfile

from fnmatch import fnmatch

from ..log import get_logger

TEMP_DIR = tempfile.gettempdir()
logger = get_logger(__name__)


def can_exclude(name: str, exclude_list: list) -> bool:
    """Check if the name can be excluded

    Args:
        name: Name to exclude
        exlude_list: List of names to be excluded can be regular expressions

    Returns:
        bool: True if the name can be excluded
    """
    for exclude_name in exclude_list:
        if fnmatch(name, exclude_name):
            return True
    return False


def zip_directory(
    dir_path: str, exclude_folders: list = [], exclude_files: list = []
) -> str:
    """Zip the directory

    Args:
        dir_path (str):  Path to the directory to zip
        exclude_folders (list): List of directories to be excluded from the zip
        exclude_files (list): List of files to be excluded from the zip

    Returns:
        str: Path to the zip file

    Raises:
        ValueError: If the directory does not exist
    """
    logger.info("Zipping directory")
    if not os.path.exists(dir_path):
        raise ValueError(f"Directory {dir_path} does not exist")

    dir_name = os.path.basename(dir_path)
    zip_path = os.path.join(TEMP_DIR, dir_name + ".zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(dir_path):

            # Exclude folders
            dirs_to_remove = []
            for dirname in dirs:
                if can_exclude(dirname, exclude_folders):
                    dirs_to_remove.append(dirname)

            for dirname in dirs_to_remove:
                dirs.remove(dirname)

            for file in files:
                # Exclude files
                if can_exclude(file, exclude_files):
                    continue

                abs_file_path = os.path.join(root, file)
                zip_file.write(
                    abs_file_path, abs_file_path.replace(dir_path, "")
                )

    return zip_path


def unzip_directory(zip_path: str, out_dir_path: str) -> None:
    """Unzip the directory

    Args:
        zip_path: Path to the zipped directory
        dir_path: Output directory path

    Returns:
        None: None

    Raises:
        ValueError: If the zip file does not exist
        ValueError: If the output directory does not exist
    """
    logger.info("Unzipping directory")
    if not os.path.exists(zip_path):
        raise ValueError(f"Zip file {zip_path} does not exist")

    if not os.path.exists(out_dir_path):
        raise ValueError(f"Output directory {out_dir_path} does not exist")

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall(out_dir_path)
