#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utility functions for creating various AWS resources."""

import boto3

from sagemaker.session import Session as SagemakerSession

from ..log import get_logger

logger = get_logger(__name__)


def get_boto_session(creds: dict) -> boto3.session.Session:
    """Creates amazon boto3 session

    Args:
        creds: Credentials to use for the session

    Returns:
        boto3.session.Session: boto3 session object
    """
    # Aws credentials
    logger.info("Getting boto3 session")
    if "aws_session_token" in creds["aws"]:
        boto_session = boto3.session.Session(
            aws_access_key_id=creds["aws"]["access_key_id"],
            aws_secret_access_key=creds["aws"]["access_key_secret"],
            aws_session_token=creds["aws"]["aws_session_token"],
            region_name=creds["aws"]["region"],
        )
    else:
        boto_session = boto3.session.Session(
            aws_access_key_id=creds["aws"]["access_key_id"],
            aws_secret_access_key=creds["aws"]["access_key_secret"],
            region_name=creds["aws"]["region"],
        )

    return boto_session


def get_sagemaker_session(creds: dict) -> boto3.session.Session:
    """Creates amazon sagemaker session

    Args:
        creds: Credentials to use for the session

    Returns:
        boto3.session.Session: sagemaker session object
    """
    logger.info("Getting sagemaker session")
    boto_session = get_boto_session(creds)

    default_s3_bucket = creds["aws"]["s3Bucket"]
    sagemaker_session = SagemakerSession(
        boto_session=boto_session, default_bucket=default_s3_bucket
    )

    return sagemaker_session
