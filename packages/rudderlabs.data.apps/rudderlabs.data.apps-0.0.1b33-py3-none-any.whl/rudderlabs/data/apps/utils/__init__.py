#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utility functions."""

import os
from glob import glob
from ..log import get_logger

logger = get_logger(__name__)

def get_latest_folder(path: str, filter_substr: str = None) -> str:
    """Gets latest folder by timest

    Args:
        path: Path to parent directory where to search for latest folder
        filter_substr: If only certain set of folders need to be selected based on a substring match, defaults to None

    Returns:
        str: File path
    """
    files_and_folders = list(glob(os.path.join(path, "*")))
    if filter_substr:
        files_and_folders = [
            path for path in files_and_folders if filter_substr in path
        ]
    folder_paths = [path for path in files_and_folders if os.path.isdir(path)]
    recent_folder_path = max(folder_paths, key=os.path.getctime)
    return recent_folder_path

def list_files(startpath: str) -> list:
    """Lists all files in a directory

    Args:
        startpath: Path to directory

    Returns:
        list: List of files
    """
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * (level)
        print("{}{}/".format(indent, os.path.basename(root)))
        subindent = " " * 4 * (level + 1)
        for f in files:
            print("{}{}".format(subindent, f))


def change_dir_permissions(dir_path: str, mode: int) -> None:
    """Change permissions of a file or directory

    Args:
        path: Path to file or directory
        mode: Permissions to change to
    """
    for root, dirnames, filenames in os.walk(dir_path):
        os.chmod(root, mode)
        for filename in filenames:
            path = os.path.join(root, filename)
            os.chmod(path, mode)

def render_template(jenv, template, context, output_dir):
    """Renders a template to the output directory using specific context.

    Args:

      jenv: The Jinja2 environment to use for rendering the template
      template: The path to the template, from the internal templates directory
      context: A dictionary with the context to render the template with
      output_dir: Where to save the output
    """

    output_file = os.path.join(output_dir, template)

    basedir = os.path.dirname(output_file)
    if not os.path.exists(basedir):
        logger.info("mkdir %s", basedir)
        os.makedirs(basedir)

    with open(output_file, "wt") as f:
        logger.info("rendering %s", output_file)
        try:
            T = jenv.get_template(template)
            f.write(T.render(**context))
        except Exception as e:
            logger.error("Error rendering %s: %s", template, e)
            raise
