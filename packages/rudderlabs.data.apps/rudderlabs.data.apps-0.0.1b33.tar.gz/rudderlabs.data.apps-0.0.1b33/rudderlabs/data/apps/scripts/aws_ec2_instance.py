#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scripts for starting and stoping aws instances"""

import os
import boto3
import click

from click_plugins import with_plugins
from pkg_resources import iter_entry_points

from . import rudderlabs
from ..config import read_yaml
from ..log import get_logger, verbosity_option
from ..aws.session import get_boto_session

logger = get_logger(__name__)

def get_ec2_instance(credentials_file: str, instance_id: str) -> object:
    """ Get an instance from the given credentials file and instance id

    Args:
        credentials_file:  The path to the credentials file
        instance_id: The instance id to get

    Returns:
        object:  The instance
    """
    # Load the credentials file
    creds = read_yaml(credentials_file)
    session = get_boto_session(creds)
    ec2 = session.resource('ec2')
    return ec2.Instance(instance_id)

@click.command(epilog=""" See 'rlabs aws instance --help' for more information.""")
@click.option(
    "-c",
    "--credentials-file",
    default=os.path.join(os.path.realpath(os.curdir), "credentials.yaml"),
    type=click.Path(exists=True),
    help="Path to the AWS credentials file",
)
@click.option(
    "-i",
    "--instance-id",
    help="Instance ID to start or stop",
    required=True,
)
@verbosity_option()
@rudderlabs.raise_on_error
def stop(credentials_file: click.Path, instance_id: str) -> None:
    """ Stop an instance 

    Args:
        credentials_file:  Path to the credentials file
        instance_id: Instance id to stop

    Returns:
        None: None
    """
    logger.info(f"Stopping instance {instance_id}")

    instance = get_ec2_instance(credentials_file, instance_id)
    instance.stop()

@click.command(epilog=""" See 'rlabs aws instance --help' for more information.""")
@click.option(
    "-c",
    "--credentials-file",
    default=os.path.join(os.path.realpath(os.curdir), "credentials.yaml"),
    type=click.Path(exists=True),
    help="Path to the AWS credentials file",
)
@click.option(
    "-i",
    "--instance-id",
    help="Instance ID to start or stop",
    required=True,
)
@verbosity_option()
@rudderlabs.raise_on_error
def start(credentials_file: click.Path, instance_id: str) -> None:
    """ Start an instance 

    Args:
        credentials_file:  Path to the credentials file
        instance_id: Instance id to stop

    Returns:
        None: None
    """
    logger.info(f"Starting instance {instance_id}")

    instance = get_ec2_instance(credentials_file, instance_id)
    instance.start()

# the group command must be at the end of this file for plugins to work.
@with_plugins(iter_entry_points("rlabs.aws.instance.cli"))
@click.group(
    epilog="""Examples:

\b
    # Starting AWS Instance
    $ rlabs aws instance start --credentials-file credentials.yaml --instance-id i-0a9f9f9f9f9f9f9f
    $ rlabs aws instance start -c credentials.yaml -i i-0a9f9f9f9f9f9f9f
\b
    # Stopping AWS Instance
    $ rlabs aws instance stop --credentials-file credentials.yaml --instance-id i-0a9f9f9f9f9f9f9f
    $ rlabs aws instance stop -c credentials.yaml -i i-0a9f9f9f9f9f9f9f

    """
)
def instance():
    """Start and stop AWS instances"""
    pass
