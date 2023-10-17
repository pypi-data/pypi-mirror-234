#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

from pathlib import Path

import click


@click.command(
    epilog="""
    Script for running a notebook in a sagemaker job.

    Example:

        $ rudderlabs run_notebook_wrapper --notebook_path ./notebooks/notebook.ipynb --params {"param1": "value1", "param2": "value2"}
    """
)
# These manditory options for every script
@click.option(
    "-j",
    "--job-id",
    required=True,
    type=click.STRING,
    help="Job id to be passed to notebook execution script",
)
@click.option(
    "-i",
    "--input-data-zip",
    required=False,
    type=click.Path(exists=True),
    help="Path to input data zip file",
)
@click.option(
    "-ip",
    "--input-data-path",
    required=False,
    type=click.Path(exists=True),
    help="Path to input data directory",
)
@click.option(
    "-o",
    "--output-data-path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the output directory",
)
@click.option(
    "-s",
    "--source-code-zip",
    required=True,
    type=click.Path(exists=True),
    help="Path to the source code zip file",
)
@click.option(
    "-r",
    "--requirements-path",
    required=True,
    type=click.Path(exists=True),
    help="Path to the requirements.txt file",
)
# These are optional parameters specific to this script, and these parameters will come from
# the pipeline config
# Example:(content of sample pipeline)
# pipeline:
#  - name: "sample_step"
#    job_suffix: "S"
#    code: "run_notebook_wrapper.py"
#    input_data: "data/<job_id>"
#    output_path: "data"
#    params:
#      notebook_path: "notebook/sample_notebook.ipynb"
#      train_id: "1"
#
#
#   While running above "sample_step" using this script the optional params will be
# --notebook_path "notebook/sample_notebook.ipynb" --train_id "1"
#
#  Specify the optoins in accordance with the pipeline config
@click.option(
    "-n",
    "--notebook-path",
    required=True,
    type=click.Path(exists=False),
    help="Path to the notebook to be executed",
)
@click.option(
    "-t",
    "--train-id",
    default=0,
    required=False,
    type=click.INT,
    help="Train id to be passed to notebook execution script",
)
@click.option(
    "-vop",
    "--validation-output-path",
    required=False,
    type=click.STRING,
    help="Path to the output directory for validation data",
)
def notebook_run_script(
    job_id: click.STRING,
    input_data_zip: click.Path,
    input_data_path: click.Path,
    output_data_path: click.Path,
    source_code_zip: click.Path,
    requirements_path: click.Path,
    notebook_path: click.Path,
    train_id: click.INT,
    validation_output_path: click.STRING,
) -> None:
    print("Params:")
    print("\tjob_id: {}".format(job_id))
    print("\tinput_data_zip: {}".format(input_data_zip))
    print("\tinput_data_path: {}".format(input_data_path))
    print("\toutput_data_path: {}".format(output_data_path))
    print("\tsource_code_zip: {}".format(source_code_zip))
    print("\trequirements_path: {}".format(requirements_path))
    print("\tnotebook_path: {}".format(notebook_path))
    print("\ttrain_id: {}".format(train_id))
    print("\tvalidation_output_path: {}".format(validation_output_path))
    print("")

    # First install requirements so that rudderlabs/data/apps/templates/notebook_execution_script.py can be run
    # It is expected that the requirements are already there in the sagemaker container path
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            requirements_path,
            "--quiet",
        ]
    )

    from rudderlabs.data.apps.log import setup_file_logger
    from rudderlabs.data.apps.utils import change_dir_permissions, list_files
    from rudderlabs.data.apps.utils.notebook import (
        get_html_from_notebook,
        run_notebook,
    )
    from rudderlabs.data.apps.utils.zip import unzip_directory

    logfile_name = os.path.splitext(os.path.basename(__file__))[0] + ".log"
    logfile_path = os.path.join(output_data_path, "logs", logfile_name)
    if not os.path.exists(logfile_path):
        os.makedirs(os.path.dirname(logfile_path))

    logger = setup_file_logger(logfile_path)

    # Unzip the code zip file
    logger.info("Unzipping code zip file")
    source_code_path = os.path.dirname(source_code_zip)
    unzip_directory(source_code_zip, source_code_path)
    list_files(source_code_path)

    # Unzip the input data zip file
    if input_data_zip is not None:
        logger.info("Unzipping input data zip file")
        input_data_path = os.path.dirname(input_data_zip)
        unzip_directory(input_data_zip, input_data_path)

    if input_data_path is not None:
        list_files(input_data_path)

    nb_params = {
        "train_id": train_id,
        "job_id": job_id,
        "code_path": source_code_path,
        "local_input_path": input_data_path,
        "local_output_path": output_data_path,
        "validation_output_path": validation_output_path,
    }

    logger.info("Running notebook")
    logger.info(
        f"Notebook path: {os.path.join(source_code_path, notebook_path)}"
    )
    logger.info(f"Notebook params: {nb_params}")

    abs_notebook_path = os.path.join(source_code_path, notebook_path)
    print(abs_notebook_path)
    output_notebook_path = run_notebook(abs_notebook_path, nb_params)
    html_path = get_html_from_notebook(output_notebook_path)

    Path(output_data_path).mkdir(parents=True, exist_ok=True)

    # Change permissions of the output directory
    # this is important because the output directory is mounted in the sagemaker container
    # and the user running the notebook is not the same as the user who mounted the directory
    #
    # beacause of this sagemaker process is not able to delete the output directory
    print("Changing permissions of the output directory")
    change_dir_permissions(output_data_path, 0o777)

    # Copy html file to output path
    subprocess.run(
        f"mv {html_path} {os.path.join(output_data_path, os.path.basename(html_path))}".split()
    )


if __name__ == "__main__":
    notebook_run_script()
