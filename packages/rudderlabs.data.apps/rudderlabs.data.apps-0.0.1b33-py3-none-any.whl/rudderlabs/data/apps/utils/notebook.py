#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Jupyter Notebook utilities."""

import subprocess

from typing import Optional

from ..log import get_logger

logger = get_logger(__name__)


def run_notebook(notebook_path: str, params: Optional[dict] = None) -> str:
    """
    Run a notebook in a subprocess and returns the output file path

    Args:
        notebook_path (str): notebook path
        params (Optional[dict], optional): papermill params to the notebook. Defaults to None.

    Returns:
        str: _description_
    """
    # Run the notebook in a subprocess
    # cmd = f"jupyter nbconvert  --to notebook --inplace --ExecutePreprocessor.timeout=600 --ExecutePreprocessor.kernel_name=python3 --execute {notebook_path}".split()
    output_nb_path = f"{notebook_path.rpartition('.')[0]}_output.ipynb"
    logger.info("Running notebook")
    cmd = f"papermill {notebook_path} {output_nb_path} -k python3".split()
    if params is not None:
        for param, val in params.items():
            cmd.extend(["-p", str(param), str(val)])

    logger.info(f"Command: {' '.join(cmd)}")
    subprocess.run(cmd)
    return output_nb_path


def get_html_from_notebook(notebook_path: str) -> str:
    """Convert a notebook to html and returns the path of the html file.

    Args:
        notebook_path: Notebook path

    Returns:
        str: html file path
    """
    # Convert the notebook to html
    logger.info("Converting notebook to html")
    cmd = f"jupyter nbconvert --to html --TemplateExporter.exclude_input=True {notebook_path}".split()

    logger.info(f"Command: {' '.join(cmd)}")
    subprocess.run(cmd)

    # Get the path of the html file
    html_path = notebook_path.replace(".ipynb", ".html")
    return html_path
