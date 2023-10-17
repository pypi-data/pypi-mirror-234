#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Constants used for building and more."""

from .log import get_logger

logger = get_logger(__name__)

SAGEMAKER_CONTAINER_PATH_MAIN = "/opt/ml/processing"
"""Path to the main folder in the sagemaker container."""

CONDA_ENV_NAME = "py3710_data_apps"
"""Name of the conda environment to use for data apps project."""

EXCLUDE_FOLDERS = [
    "__pycache__",
    "tests",
    "tests_data",
    "conda",
    "eggs",
    "build",
    "dist",
    ".git",
    "*.egg-info",
]
"""Folders to exclude from the zip, while compressing data apps repository code."""

EXCLUDE_FILES = [
    "*.pyc",
    "*.pyo",
    "*.dist-info",
    "*.DS_Store",
    "*.gitignore",
    "*.gitmodules",
    "*.gitattributes",
    "*.gitkeep",
]
"""Files to exclude from the zip, while compressing data apps repository code."""
