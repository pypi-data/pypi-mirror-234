#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import tempfile

from datetime import datetime

import click
import jinja2

from click_plugins import with_plugins
from pkg_resources import iter_entry_points
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.sklearn.processing import SKLearnProcessor

from ..aws.events import (
    delete_event_rule,
    schedule_lambda_function,
    update_event_rule,
)
from ..aws.lambda_utils import (
    check_labmda_policy,
    create_iam_role_for_lambda,
    create_lambda_deployment_package,
    delete_lambda_function,
    deploy_lambda_function,
    exponential_retry,
)
from ..aws.processing import get_sklearn_processor
from ..aws.s3 import download_s3_directory, get_s3_resource, parse_s3_path
from ..aws.session import get_boto_session
from ..config import read_yaml
from ..constants import (
    CONDA_ENV_NAME,
    EXCLUDE_FILES,
    EXCLUDE_FOLDERS,
    SAGEMAKER_CONTAINER_PATH_MAIN,
)
from ..log import get_logger, verbosity_option
from ..utils import render_template
from ..utils.zip import zip_directory
from . import rudderlabs

logger = get_logger(__name__)


def prepare_scripts(template_dir: str, context: dict, templates: list) -> str:
    """Prepare scripts for processing

    Args:
        template_dir: Path to the template directory
        context: Context for the template
        templates: List of template files to use
    Returns:
        str: Path to the scripts zip file
    """


def prepare_input_data(
    repository_path: str, input_path: str
) -> (ProcessingInput, bool):
    """Prepare input data for processing

    Args:
        repository_path: Path to the repository
        input_path: Path to the input data
    Returns:
        ProcessingInput: Input data for processing
        bool: Whether the input data is S3 or not
    """

    if input_path is None or input_path == "":
        return None, False

    sagemaker_input_path = os.path.join(SAGEMAKER_CONTAINER_PATH_MAIN, "data")

    logger.info(f"Input data is {input_path}")

    # s3 Location
    if input_path.startswith("s3://"):
        return (
            ProcessingInput(
                source=input_path,
                s3_data_type="S3Prefix",
                s3_data_distribution_type="FullyReplicated",
                destination=sagemaker_input_path,
            ),
            True,
        )

    # Local path
    # check input data path weather it is relative to repository or absolute
    if not os.path.isabs(input_path):
        input_path = os.path.join(repository_path, input_path)

    if not os.path.exists(input_path):
        return None, False

    logger.info("Preparing input data")
    input_data_zip_path = zip_directory(input_path)

    return (
        ProcessingInput(
            source=input_data_zip_path,
            destination=sagemaker_input_path,
        ),
        False,
    )


def prepare_output_data(
    output_data_path: str, output_name: str, running_mode: str = "remote"
) -> (ProcessingOutput, bool):
    """Prepare output data for processing

    Args:
        output_data_path: Path to the output data
        output_name: Name of the output data folder
        running_mode: Running mode of the pipeline (local or remote)

    Returns:
        ProcessingOutput: Output data for processing
        bool: Whether the output data is S3 or not
    """

    sagemaker_output_data_path = os.path.join(
        SAGEMAKER_CONTAINER_PATH_MAIN, "output"
    )

    logger.info(f"Output data is {output_data_path}")

    # s3 Location
    if output_data_path.startswith("s3://"):
        return (
            ProcessingOutput(
                source=sagemaker_output_data_path,
                output_name=output_name,
                destination=output_data_path,
                s3_upload_mode="EndOfJob"
                if running_mode == "local"
                else "Continuous",
            ),
            True,
        )
    else:
        return (
            ProcessingOutput(
                source=sagemaker_output_data_path, output_name=output_name
            ),
            False,
        )


def download_output_data(
    sklearn_processor: SKLearnProcessor,
    running_mode: str,
    local_output_path: str,
    creds: dict,
    job_id: str,
    output_name: str,
) -> None:
    """Download output data from S3 to local directory

    Args:
        sklearn_processor: SKLearnProcessor object
        running_mode: Running mode of the pipeline (local or remote)
        local_output_path: Local path to download output data
        creds: Credentials for S3
        job_id: Job ID of the pipeline
        output_name: Name of the processing output

    Returns:
        None:
    """
    s3_bucket = None
    process_job_output_path = None

    if running_mode != "local":
        s3_bucket = creds["s3Bucket"]
        process_job_output_path = (
            f"{sklearn_processor.latest_job.job_name}/output/output-1/{job_id}"
        )
    else:
        preprocessing_job_description = sklearn_processor.jobs[-1].describe()
        output_config = preprocessing_job_description["ProcessingOutputConfig"]

        for output in output_config["Outputs"]:
            if output["OutputName"] != output_name:
                continue

            output_s3_url = output["S3Output"]["S3Uri"]
            s3_bucket, process_job_output_path = parse_s3_path(output_s3_url)

    logger.info(f"S3 bucket: {s3_bucket}")
    logger.info(f"Process job output path: {process_job_output_path}")

    if s3_bucket is not None and process_job_output_path is not None:
        # Downloading model output files into local
        s3_resource = get_s3_resource(creds)

        download_s3_directory(
            s3_resource, s3_bucket, process_job_output_path, local_output_path
        )


def run_pipeline_step(
    pipeline_step_info: dict,
    creds: dict,
    instance_type: str,
    job_id: str,
    repository_path: str,
    exclude_folders: list,
    exclude_files: list,
) -> None:
    """Runs given pipeline step in sci-kit learn processor in amazon sagemaker

    Args:
        pipeline_step_info: Pipeline step information
        creds: AWS credentials
        instance_type: Instance type to use for the sagemaker job
        job_id: all the outputs will be saved under the folder with this name
        repository_path: Path to the repository
        exclude_folders: List of directories to be excluded from the zip
        exclude_files: List of files to be excluded from the zip

    Returns:
        None: None
    """
    # Get sklearn processor
    logger.info(f"Pipeline step: {pipeline_step_info['name']}")
    job_name = (
        f"{pipeline_step_info['name']}-{pipeline_step_info['job_suffix']}"
    )
    sklearn_processor = get_sklearn_processor(creds, instance_type, job_name)

    # Prepare source code and input data
    logger.info("Preparing source code")
    source_code_zip_path = zip_directory(
        repository_path,
        exclude_folders=exclude_folders,
        exclude_files=exclude_files,
    )

    sagemaker_code_path = os.path.join(SAGEMAKER_CONTAINER_PATH_MAIN, "code")
    sagemaker_req_path = os.path.join(
        SAGEMAKER_CONTAINER_PATH_MAIN, "requirements"
    )

    local_req_path = os.path.join(repository_path, "requirements.txt")

    # script parameters
    script_params = {f"{k}": v for k, v in pipeline_step_info["params"].items()}

    # Pass job id to the pipeline script as a parameter
    script_params["--job-id"] = job_id

    input_path = pipeline_step_info.get("input_path")
    input_path = (
        ""
        if input_path is None
        else input_path.replace("<job_id>", f"{job_id}")
    )

    # Prepare input data
    processing_input, input_location_is_s3 = prepare_input_data(
        repository_path, input_path
    )

    if not input_location_is_s3 and processing_input is not None:
        script_params["--input-data-zip"] = os.path.join(
            processing_input.destination,
            os.path.basename(processing_input.source),
        )

    if processing_input is not None:
        script_params["--input-data-path"] = processing_input.destination

    # Prepare output data
    output_path = pipeline_step_info.get("output_path")
    if output_path is None:
        raise ValueError("Output path is not specified")
        return

    output_path = output_path.replace("<job_id>", f"{job_id}")
    processing_output, output_location_is_s3 = prepare_output_data(
        output_path, pipeline_step_info["name"], instance_type
    )

    script_params["--output-data-path"] = processing_output.source

    script_params["--source-code-zip"] = os.path.join(
        sagemaker_code_path, os.path.basename(source_code_zip_path)
    )
    script_params["--requirements-path"] = os.path.join(
        sagemaker_req_path, "requirements.txt"
    )

    arguments = []
    for k, v in script_params.items():
        arguments.append(f"{k}")
        arguments.append(f"{v}")

    logger.info(f"Arguments: {arguments}")
    inputs = [
        ProcessingInput(
            source=source_code_zip_path, destination=sagemaker_code_path
        ),
        ProcessingInput(source=local_req_path, destination=sagemaker_req_path),
    ]

    if processing_input:
        inputs.append(processing_input)

    sklearn_processor.run(
        code=pipeline_step_info["code"],
        inputs=inputs,
        outputs=[processing_output],
        arguments=arguments,
    )

    if not output_location_is_s3:
        # Uploading model output files from s3 to local
        local_output_path = os.path.join(
            repository_path, pipeline_step_info["output_path"]
        )

        output_name = pipeline_step_info["name"]
        download_output_data(
            sklearn_processor,
            instance_type,
            local_output_path,
            creds,
            job_id,
            output_name,
        )

    # Cleaning up latest job files
    try:
        s3_bucket = sklearn_processor.sagemaker_session.default_bucket()
        root_prefix = sklearn_processor.latest_job.job_name

        logger.info(
            f"Cleaning S3 data located at bucket: {s3_bucket}, prefix :{root_prefix}"
        )

        s3_resource = get_s3_resource(creds)
        s3_resource.Bucket(s3_bucket).objects.filter(
            Prefix=root_prefix
        ).delete()
    except Exception as e:
        logger.error(f"Error deleting S3 object: {e}")


@click.command(
    epilog="""
    The command to run given notebookes in the pipeline.

    Examples:

        $ rlabs aws run-pipeline --pipeline-config-file pipeline.yaml --credentials-file credentials.yaml --repository-path /path/to/repository --instance-type ml.t3.xlarge --job-id my-job-id

        $ rlabs aws run-pipeline -p pipeline.yaml -c credentials.yaml -r /path/to/repository -i local -j my-job-id
    """
)
@click.option(
    "-j",
    "--job-id",
    default=None,
    help="Job id to be used for the pipeline, used to store output files in S3/local",
)
@click.option(
    "-c",
    "--credentials-file",
    type=click.Path(exists=True, readable=True, resolve_path=True),
    show_default=True,
    default=os.path.join(os.path.realpath(os.curdir), "credentials.yaml"),
)
@click.option(
    "-i",
    "--instance-type",
    default="ml.t3.xlarge",
    show_default=True,
    help="The instance type to use for the amazon sagemaker notebook instance.",
)
@click.option(
    "-p",
    "--pipeline-config-file",
    type=click.Path(exists=True, readable=True, resolve_path=True),
    help="The pipeline config file to use.",
)
@click.option(
    "-r",
    "--repository-path",
    default=os.path.realpath(os.curdir),
    show_default=True,
    type=click.Path(exists=True, readable=True, resolve_path=True),
    help="The repository path to use.",
)
@verbosity_option()
@rudderlabs.raise_on_error
def run(
    job_id: str,
    credentials_file: click.Path,
    instance_type: str,
    pipeline_config_file: click.Path,
    repository_path: click.Path,
) -> None:
    """Run the pipeline defined in the pipeline config file."""
    logger.info("Running pipeline")
    logger.info("credentials_file: %s", credentials_file)
    logger.info("Instance type: %s", instance_type)

    if job_id is None:
        job_id = int(datetime.now().timestamp())

    # Load the pipeline config file
    pipeline_config = read_yaml(pipeline_config_file)
    logger.info("Pipeline config: %s", pipeline_config)

    # Load the credentials file
    config = read_yaml(credentials_file)
    exclude_folders = (
        pipeline_config.get("exclude_folders", []) + EXCLUDE_FOLDERS
    )
    exclude_files = pipeline_config.get("exclude_files", []) + EXCLUDE_FILES

    # Runing pipeline
    for pipeline_step in pipeline_config["pipeline"]:
        logger.info("\n\n\nRUNNING PIPELINE STEP: %s", pipeline_step["name"])

        run_pipeline_step(
            pipeline_step_info=pipeline_step,
            creds=config,
            instance_type=instance_type,
            job_id=job_id,
            repository_path=repository_path,
            exclude_folders=exclude_folders,
            exclude_files=exclude_files,
        )


@click.command(epilog="""See rlabs aws pipeline --help for more information.""")
@click.option(
    "-id",
    "--instance-id",
    required=True,
    help="The instance id to use for scheduling the pipeline.",
)
@click.option(
    "-sit",
    "--sagemaker-instance-type",
    default="ml.t3.xlarge",
    show_default=True,
    help="The instance type to use for the amazon sagemaker notebook instance.",
)
@click.option(
    "-p",
    "--pem-file",
    required=True,
    type=click.Path(exists=True, resolve_path=True),
    help="The pem key file for communicating with the instance.",
)
@click.option(
    "-u",
    "--ec2-username",
    default="ec2-user",
    show_default=True,
    help="EC2 username for the instance.",
)
@click.option(
    "-r",
    "--repository-path",
    default=os.path.realpath(os.curdir),
    show_default=True,
    type=click.Path(exists=True, readable=True, resolve_path=True),
    help="The repository path to use.",
)
@click.option(
    "-pn",
    "--project-name",
    default=None,
    type=str,
    help="Name of the project, this will be used as a prefix for creating roles, lambda functions, event rules etc.",
)
@click.option(
    "-pc",
    "--pipeline-config-file",
    type=click.Path(exists=True, readable=True, resolve_path=True),
    help="The pipeline config file to use. relative to the repository path.",
)
@click.option(
    "-c",
    "--credentials-file",
    type=click.Path(exists=True, readable=True, resolve_path=True),
    show_default=True,
    default=os.path.join(os.path.realpath(os.curdir), "credentials.yaml"),
    help="The credentials file to use. relative to the repository path.",
)
@click.option(
    "-es",
    "--event-schedule",
    default="rate(1 day)",
    show_default=True,
    help="The specified schedule in either cron or rate format. More info at https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html",
)
@click.option(
    "-rn",
    "--role-name",
    default=None,
    help="The name of the role to use for the lambda function. If not specified, a new role will be created with the name <repository_name>-lambda-role",
)
@verbosity_option()
@rudderlabs.raise_on_error
def schedule(
    instance_id: str,
    sagemaker_instance_type: str,
    pem_file: str,
    ec2_username: str,
    repository_path: str,
    project_name: str,
    pipeline_config_file: str,
    credentials_file: str,
    event_schedule: str,
    role_name: str,
) -> None:
    """
    Setup the instance and schedule the pipeline.
    """
    logger.info("Setting up instance: %s", instance_id)

    if sagemaker_instance_type == "local":
        logger.error("Local instance type is not supported")
        return

    # Load the credentials file
    creds = read_yaml(credentials_file)
    boto_session = get_boto_session(creds)
    ec2_resource = boto_session.resource("ec2")
    instance = ec2_resource.Instance(instance_id)

    # Adding trailing slash to repository path if not present
    # This can be used to find relative path of pipeline config file and credentials file
    # And can be useful while rsyncing to defferent project folder, it will be the case
    # when specifying project name is different from the repository directory name
    repository_path = os.path.join(repository_path, "")

    if instance.state["Name"] != "running":
        logger.info("Instance is not running, starting instance")
        instance.start()

        logger.info("Waiting for instance to start")
        instance.wait_until_running()

        logger.info("Waiting for status ok")
        waiter = ec2_resource.meta.client.get_waiter("instance_status_ok")
        waiter.wait(InstanceIds=[instance_id])

    credentials_path_relative = os.path.relpath(
        credentials_file, repository_path
    )

    if project_name is None:
        project_name = os.path.basename(repository_path[:-1])

    # take relative path for pipeline config file
    pipeline_config_file_relative = pipeline_config_file.replace(
        repository_path, ""
    )

    pipeline_run_command = f"rlabs aws pipeline run -p {pipeline_config_file_relative} -c {credentials_path_relative} -i {sagemaker_instance_type}"
    logger.info("Pipeline run command: %s", pipeline_run_command)

    # Jinja2 context for the template
    context = dict(
        user=ec2_username,
        project_name=project_name,
        conda_env=CONDA_ENV_NAME,
        project_dir=f"/home/{ec2_username}/{project_name}",
        pipeline_run_command=pipeline_run_command,
        instance_id=instance_id,
        credentials_file=credentials_path_relative,
        region=creds["aws"]["region"],
        sagemaker_instance_type=sagemaker_instance_type,
    )

    # base jinja2 engine
    template_loader = jinja2.PackageLoader(
        "rudderlabs.data.apps", os.path.join("templates", "scripts")
    )
    env = jinja2.Environment(
        loader=template_loader,
        autoescape=jinja2.select_autoescape(["html", "xml"]),
    )

    # Render the templates
    scripts_dir = tempfile.mkdtemp()
    accepted_extensions = [".sh", ".py"]
    for k in template_loader.list_templates():
        ext = os.path.splitext(k)[1]
        if ext not in accepted_extensions:
            continue
        render_template(env, k, context, scripts_dir)

    logger.info("Copying setup scripts to instance")
    host = f"{ec2_username}@{instance.public_ip_address}"
    host_scripts_dir = f"/home/{ec2_username}/scripts"

    logger.info("Syncing project repository")
    subprocess.run(
        [
            "rsync",
            "-rav",
            "-e",
            f"ssh -i {pem_file} -o StrictHostKeyChecking=no",
            "--exclude",
            "data",
            "--exclude",
            ".git",
            repository_path,
            f"{host}:/home/{ec2_username}/{project_name}",
        ]
    )

    subprocess.run(
        [
            "scp",
            "-o",
            "StrictHostKeyChecking=no",
            "-i",
            pem_file,
            "-r",
            scripts_dir,
            f"{host}:{host_scripts_dir}",
        ]
    )
    subprocess.run(
        [
            "scp",
            "-o",
            "StrictHostKeyChecking=no",
            "-i",
            pem_file,
            f"{scripts_dir}/run_pipeline.sh",
            f"{host}:/home/{ec2_username}/run_pipeline.sh",
        ]
    )

    logger.info("Creating conda environment")
    subprocess.run(
        [
            "ssh",
            "-i",
            pem_file,
            host,
            "sh",
            f"{host_scripts_dir}/create_conda_env.sh",
        ]
    )

    logger.info("Creating cron job")
    subprocess.run(
        [
            "ssh",
            "-i",
            pem_file,
            host,
            "sh",
            f"{host_scripts_dir}/add_cron_job.sh",
        ]
    )

    logger.info("Removing setup scripts from instance")
    subprocess.run(["ssh", "-i", pem_file, host, "rm", "-rf", host_scripts_dir])

    lambda_function_filename = os.path.join(scripts_dir, "lambda_start_ec2.py")
    project_prefix = project_name.replace("_", "-").replace(".", "-").lower()
    lambda_handler_name = "lambda_start_ec2.lambda_handler"
    create_iam_role = True if role_name is None else False
    lambda_role_name = (
        f"{project_prefix}-lambda-role" if role_name is None else role_name
    )

    # Extracting pipeline name from pipeline config file
    pipeline_name = os.path.splitext(os.path.basename(pipeline_config_file))[0]

    lambda_function_name = f"{project_prefix}-{pipeline_name}-lambda-scheduled"
    event_rule_name = f"{project_prefix}-{pipeline_name}-event-scheduled"

    iam_resource = boto_session.resource("iam")
    lambda_client = boto_session.client("lambda")
    eventbridge_client = boto_session.client("events")

    logger.info(
        f"Creating AWS Lambda function {lambda_function_name} from the "
        f"{lambda_handler_name} function in {lambda_function_filename}..."
    )

    deployment_package = create_lambda_deployment_package(
        lambda_function_filename
    )
    if create_iam_role:
        iam_role = create_iam_role_for_lambda(iam_resource, lambda_role_name)
    else:
        iam_role = iam_resource.Role(lambda_role_name)

        found_required_policies = check_labmda_policy(
            iam_role,
            "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
        )
        found_required_policies = (
            check_labmda_policy(
                iam_role, "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
            )
            and found_required_policies
        )

        if not found_required_policies:
            logger.warning(
                f"Lambda role {lambda_role_name} does not have required policies attached. Please attach the following policies to the role: "
                f"arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole, "
                f"arn:aws:iam::aws:policy/AmazonEC2FullAccess"
            )

            logger.warning(
                "The specified role name must possess policies enabling it to execute lambda functions and initiate EC2 Instances, "
                "which can either be Amazon-managed or custom-created policies."
            )

    logger.info(
        f"Attempting to delete existing Lambda function {lambda_function_name}..."
    )
    try:
        delete_lambda_function(lambda_client, lambda_function_name)
        logger.info(f"Deleted existing Lambda function {lambda_function_name}")
    except Exception as e:
        logger.info(
            f"Failed to delete or Lambda function {lambda_function_name} not found."
        )
        logger.info(str(e))
        pass

    lambda_function_arn = exponential_retry(
        deploy_lambda_function,
        "InvalidParameterValueException",
        lambda_client,
        lambda_function_name,
        lambda_handler_name,
        iam_role,
        deployment_package,
    )

    logger.info(
        f"Attempting to delete existing Event Rule {event_rule_name}..."
    )
    try:
        delete_event_rule(
            eventbridge_client, event_rule_name, lambda_function_name
        )
        logger.info(f"Deleted existing Event Rule {event_rule_name}")
    except Exception as e:
        logger.info(
            f"Failed to delete or Event Rule {event_rule_name} not found."
        )
        logger.info(str(e))
        pass

    logger.info(
        f"Scheduling {lambda_function_name} to run with rate {event_schedule}..."
    )
    schedule_lambda_function(
        eventbridge_client,
        event_rule_name,
        event_schedule,
        lambda_client,
        lambda_function_name,
        lambda_function_arn,
    )

    logger.info("Removing setup scripts from local machine temporary directory")
    shutil.rmtree(scripts_dir)


def enable_or_disable_event_bridge_rule(
    credentials_file: str,
    project_name: str,
    pipeline: str,
    enabled: bool = True,
):
    """Enable or disable an event bridge rule.

    Args:
        credentials_file: Path to the AWS credentials file.
        project_name: Name of the project.
        enabled: True to enable the rule, False to disable the rule.
    """
    creds = read_yaml(credentials_file)
    boto_session = get_boto_session(creds)
    eventbridge_client = boto_session.client("events")

    pipeline_name = os.path.splitext(os.path.basename(pipeline))[0]
    project_prefix = project_name.replace("_", "-").replace(".", "-").lower()
    event_rule_name = f"{project_prefix}-{pipeline_name}-event-scheduled"
    update_event_rule(eventbridge_client, event_rule_name, enabled)


@click.command(epilog="""Disable event bridge rule for the project.""")
@click.option(
    "-c",
    "--credentials-file",
    default="credentials.yaml",
    help="Path to the AWS credentials file.",
)
@click.option(
    "-p",
    "--pipeline",
    required=True,
    type=click.Path(exists=True),
    help="Path to the pipeline configuration file.",
)
@click.option(
    "-pn",
    "--project-name",
    required=True,
    type=str,
    help="Path to the project repository.",
)
@verbosity_option()
@rudderlabs.raise_on_error
def disable_scheduling(credentials_file, pipeline, project_name):
    """Disable an event bridge rule for the project."""
    enable_or_disable_event_bridge_rule(
        credentials_file, project_name, pipeline, False
    )


@click.command(epilog="""Enable event bridge rule for the project.""")
@click.option(
    "-c",
    "--credentials-file",
    default="credentials.yaml",
    help="Path to the AWS credentials file.",
)
@click.option(
    "-p",
    "--pipeline",
    required=True,
    type=click.Path(exists=True),
    help="Path to the pipeline configuration file.",
)
@click.option(
    "-pn",
    "--project-name",
    required=True,
    type=str,
    help="Path to the project repository.",
)
@verbosity_option()
@rudderlabs.raise_on_error
def enable_scheduling(credentials_file, pipeline, project_name):
    """Enable an event bridge rule for the project."""
    enable_or_disable_event_bridge_rule(
        credentials_file, project_name, pipeline, True
    )


# the group command must be at the end of this file for plugins to work.
@with_plugins(iter_entry_points("rlabs.aws.pipeline.cli"))
@click.group(
    epilog="""Examples:

\b
    # Running pipeline
    ------------------

    $ rlabs aws pipeline run --pipeline-config-file pipeline.yaml --credentials-file credentials.yaml --repository-path /path/to/repository --instance-type ml.t3.xlarge --job-id my-job-id

    $ rlabs aws pipeline run -p pipeline.yaml -c credentials.yaml -r /path/to/repository -i local -j  Scheduling pipeline
    -----------------------

    $ rlabs aws pipeline schedule --instance-id <instance_id> --pem-file <path_to_pem_file> -u <aws_instance_user_name> --pipeline-config-file pipeline.yaml --credentials-file credentials.yaml --repository-path /path/to/repository --sagemaker-instance-type ml.t3.xlarge --event-schedule rate(1 hour) --role-name <aws_role_name> -vv

    $ rlabs aws pipeline schedule -id i-07c3cedbe6988ed49 -p ~/.ssh/instance.pem -u ubuntu -pc pipelines/sample_pipeline.yaml -c credentials_modified.yaml -es "rate(10 minutes)" -vv

    # Enabling and disabling pipeline event rule
    --------------------------------------------

    $ rlabs aws pipeline enable-scheduling --credentials-file credentials.yaml --repository-path /path/to/repository

    $ rlabs aws pipeline disable-scheduling --credentials-file credentials.yaml --repository-path /path/to/repository

"""
)
def pipeline():
    """Pipeline deployment scripts"""
    pass
