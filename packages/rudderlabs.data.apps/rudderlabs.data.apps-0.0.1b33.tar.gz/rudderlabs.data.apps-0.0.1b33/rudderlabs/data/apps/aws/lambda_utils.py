#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Shows how to use the AWS SDK for Python (Boto3) to create an AWS Lambda function,
invoke it, and delete it.
"""
import io
import json
import os
import time
import zipfile

from typing import Any, Callable

from botocore.exceptions import ClientError

from ..log import get_logger

logger = get_logger(__name__)


def exponential_retry(func, error_code, *func_args, **func_kwargs) -> Callable:
    """
    Retries the specified function with a simple exponential backoff algorithm.
    This is necessary when AWS is not yet ready to perform an action because all
    resources have not been fully deployed.

    Args:
        func: The function to retry.
        error_code: The error code to retry. Other errors are raised again.
        func_args: The positional arguments to pass to the function.
        func_kwargs: The keyword arguments to pass to the function.

    Returns:
        function: The return value of the retried function.
    """
    sleepy_time = 1
    func_return = None
    while sleepy_time < 33 and func_return is None:
        try:
            func_return = func(*func_args, **func_kwargs)
            logger.info("Ran %s, got %s.", func.__name__, func_return)
        except ClientError as error:
            if error.response["Error"]["Code"] == error_code:
                print(
                    f"Sleeping for {sleepy_time} to give AWS time to "
                    f"connect resources."
                )
                time.sleep(sleepy_time)
                sleepy_time = sleepy_time * 2
            else:
                raise
    return func_return


def create_lambda_deployment_package(function_file_name) -> bytes:
    """
    Creates a Lambda deployment package in ZIP format in an in-memory buffer. This
    buffer can be passed directly to AWS Lambda when creating the function.

    Args:
        function_file_name: The name of the file that contains the Lambda handler function.

    Returns:
        bytes: The deployment package.
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipped:
        zipped.write(function_file_name, os.path.basename(function_file_name))
    buffer.seek(0)
    return buffer.read()


def check_labmda_policy(iam_role, policy_name) -> bool:
    """
    Checks whether the specified policy is attached to the specified IAM role.

    Args:
        iam_role: The IAM role to check.
        policy_name: The name of the policy to check.

    Returns:
        bool: True if the policy is attached to the role, otherwise False.

    """
    try:
        for policy in iam_role.attached_policies.all():
            if policy.arn == policy_name:
                return True
    except Exception as error:
        logger.error(error)

    return False


def create_iam_role_for_lambda(iam_resource, iam_role_name) -> Any:
    """
    Creates an AWS Identity and Access Management (IAM) role that grants the
    AWS Lambda function basic permission to run. If a role with the specified
    name already exists, it is used for the demo.

    Args:
        iam_resource: The Boto3 IAM resource object.
        iam_role_name: The name of the role to create.

    Returns:
        Any: The newly created role.

    """
    lambda_assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    }

    policy_arn = (
        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    )
    ec2_full_access_policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"

    try:
        role = iam_resource.create_role(
            RoleName=iam_role_name,
            AssumeRolePolicyDocument=json.dumps(lambda_assume_role_policy),
        )
        iam_resource.meta.client.get_waiter("role_exists").wait(
            RoleName=iam_role_name
        )
        logger.info("Created role %s.", role.name)

        role.attach_policy(PolicyArn=policy_arn)
        logger.info("Attached basic execution policy to role %s.", role.name)

        role.attach_policy(PolicyArn=ec2_full_access_policy_arn)
        logger.info("Attached EC2 full access policy to role %s.", role.name)

    except ClientError as error:
        if error.response["Error"]["Code"] == "EntityAlreadyExists":
            role = iam_resource.Role(iam_role_name)
            logger.warning(
                "The role %s already exists. Using it.", iam_role_name
            )
        else:
            logger.exception(
                "Couldn't create role %s or attach policy %s, %s.",
                iam_role_name,
                policy_arn,
                ec2_full_access_policy_arn,
            )
            raise

    return role


def deploy_lambda_function(
    lambda_client, function_name, handler_name, iam_role, deployment_package
) -> Any:
    """
    Deploys the AWS Lambda function.

    Args:
        lambda_client: The Boto3 AWS Lambda client object.
        function_name: The name of the AWS Lambda function.
        handler_name: The fully qualified name of the handler function. This
                      must include the file name and the function name.
        iam_role: The IAM role to use for the function.
        deployment_package: The deployment package that contains the function
                               code in ZIP format.

    Returns:
        Any: The Amazon Resource Name (ARN) of the newly created function.

    """
    try:
        response = lambda_client.create_function(
            FunctionName=function_name,
            Description="AWS Lambda demo",
            Runtime="python3.8",
            Role=iam_role.arn,
            Handler=handler_name,
            Code={"ZipFile": deployment_package},
            Publish=True,
        )
        function_arn = response["FunctionArn"]
        logger.info(
            "Created function '%s' with ARN: '%s'.",
            function_name,
            response["FunctionArn"],
        )
    except ClientError as error:
        logger.info(error)
        logger.exception("Couldn't create function %s.", function_name)
        raise
    else:
        return function_arn


def delete_lambda_function(lambda_client, function_name) -> None:
    """
    Deletes an AWS Lambda function.

    Args:
        lambda_client: The Boto3 AWS Lambda client object.
        function_name: The name of the function to delete.

    Returns:
        None:

    """
    try:
        lambda_client.delete_function(FunctionName=function_name)
    except ClientError:
        logger.exception("Couldn't delete function %s.", function_name)
        raise


def invoke_lambda_function(
    lambda_client, function_name, function_params
) -> dict:
    """
    Invokes an AWS Lambda function.

    Args:
        lambda_client: The Boto3 AWS Lambda client object.
        function_name: The name of the function to invoke.
        function_params: The parameters of the function as a dict. This dict
                         is serialized to JSON before it is sent to AWS Lambda.

    Returns:
        dict: The response from the function invocation.

    """
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            Payload=json.dumps(function_params).encode(),
        )
        logger.info("Invoked function %s.", function_name)
    except ClientError:
        logger.exception("Couldn't invoke function %s.", function_name)
        raise
    return response
