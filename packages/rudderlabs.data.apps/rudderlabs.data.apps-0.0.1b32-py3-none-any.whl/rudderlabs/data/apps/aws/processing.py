#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sagemaker processors for launcing and managering ML/Deep Learning jobs."""

from sagemaker.local import LocalSession
from sagemaker.sklearn.processing import SKLearnProcessor

from ..log import get_logger
from .session import get_sagemaker_session

logger = get_logger(__name__)


def get_sklearn_processor(
    creds: dict, instance_type: str, job_name: str
) -> SKLearnProcessor:
    """Creates a sklearn processor

    Args:
        creds (str): Credentials to use for the session
        instance_type (str): The instance type to use for the amazon sagemaker notebook instance.
        job_name (str): The name of the job.

    Returns:
        SKLearnProcessor: sklearn processor object
    """

    logger.info("Getting sklearn processor")
    role_arn = creds["aws"]["roleArn"]
    logger.info(f"Role ARN: {role_arn}")
    logger.info(f"Instance type: {instance_type}")

    if instance_type == "local":
        sagemaker_session = LocalSession()
        sagemaker_session.config = {"local": {"local_code": True}}
    else:
        sagemaker_session = get_sagemaker_session(creds)

    processor = SKLearnProcessor(
        framework_version="0.20.0",
        role=role_arn,
        instance_type=instance_type,
        instance_count=1,
        base_job_name=job_name,
        sagemaker_session=sagemaker_session,
    )

    return processor
