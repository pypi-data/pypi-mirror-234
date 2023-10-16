#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shows how to use the AWS SDK for Python (Boto3) to register an AWS Lambda function
that is invoked by Amazon EventBridge on a regular schedule.
"""

import time
import boto3
from botocore.exceptions import ClientError

from . import lambda_utils
from ..log import get_logger

logger = get_logger(__name__)

def schedule_lambda_function(
        eventbridge_client, event_rule_name, event_schedule,
        lambda_client, lambda_function_name, lambda_function_arn) -> str:
    """ Schedules the specified AWS Lambda function to be invoked by EventBridge.

    Args:
        eventbridge_client: The Boto3 EventBridge client.
        event_rule_name: The name of the rule to update.
        event_schedule: The schedule to invoke the AWS Lambda function.
        lambda_client: The Boto3 Lambda client.
        lambda_function_name: The name of the AWS Lambda function to invoke.
        lambda_function_arn: The ARN of the AWS Lambda function to invoke.

    Returns:
        str: The ARN of the scheduled event.

    Raises:
        Exception : ClientError: When failed to put the event rule.
        Exception : ClientError: When couldn't add permission to eventBridge to invoke Lambda.
        Exception : ClientError: When failed to set lambda function as target.
    """
    try:
        response = eventbridge_client.put_rule(
            Name=event_rule_name, ScheduleExpression=event_schedule)
        event_rule_arn = response['RuleArn']
        logger.info("Put rule %s with ARN %s.", event_rule_name, event_rule_arn)
    except ClientError:
        logger.exception("Couldn't put rule %s.", event_rule_name)
        raise

    try:
        lambda_client.add_permission(
            FunctionName=lambda_function_name,
            StatementId=f'{lambda_function_name}-invoke',
            Action='lambda:InvokeFunction',
            Principal='events.amazonaws.com',
            SourceArn=event_rule_arn)
        logger.info(
            "Granted permission to let Amazon EventBridge call function %s",
            lambda_function_name)
    except ClientError:
        logger.exception(
            "Couldn't add permission to let Amazon EventBridge call function %s.",
            lambda_function_name)
        raise

    try:
        response = eventbridge_client.put_targets(
            Rule=event_rule_name,
            Targets=[{'Id': lambda_function_name, 'Arn': lambda_function_arn}])
        if response['FailedEntryCount'] > 0:
            logger.error(
                "Couldn't set %s as the target for %s.",
                lambda_function_name, event_rule_name)
        else:
            logger.info(
                "Set %s as the target of %s.", lambda_function_name, event_rule_name)
    except ClientError:
        logger.exception(
            "Couldn't set %s as the target of %s.", lambda_function_name,
            event_rule_name)
        raise

    return event_rule_arn


def update_event_rule(eventbridge_client, event_rule_name, enable) -> None:
    """ Updates the schedule event rule by enabling or disabling it.

    Args:
        eventbridge_client: The Boto3 EventBridge client.
        event_rule_name: The name of the rule to update.
        enable: True to enable the rule, False to disable it.

    Returns:
        None:  

    Raises:
         Exception : ClientError: When failed to update the event rule.
    """
    try:
        if enable:
            eventbridge_client.enable_rule(Name=event_rule_name)
        else:
            eventbridge_client.disable_rule(Name=event_rule_name)
        logger.info(
            "%s is now %s.", event_rule_name, 'enabled' if enable else 'disabled')
    except ClientError:
        logger.exception(
            "Couldn't %s %s.", 'enable' if enable else 'disable', event_rule_name)
        raise


def get_event_rule_enabled(eventbridge_client, event_rule_name) -> bool:
    """ Gets the enabled status of the specified event rule.

    Args:
        eventbridge_client: The Boto3 EventBridge client.
        event_rule_name: The name of the rule to get the enabled status of.

    Returns:
        bool: True if the rule is enabled, False if it is disabled.

    Raises:
        Exception :  ClientError: When failed to get the event rule status.
    """
    try:
        response = eventbridge_client.describe_rule(Name=event_rule_name)
        enabled = response['State'] == 'ENABLED'
        logger.info("%s is %s.", event_rule_name, response['State'])
    except ClientError:
        logger.exception("Couldn't get state of %s.", event_rule_name)
        raise
    else:
        return enabled

def delete_event_rule(eventbridge_client, event_rule_name, lambda_function_name) -> None:
    """ Deletes the specified event rule.

    Args:
        eventbridge_client: The Boto3 EventBridge client.
        event_rule_name: The name of the rule to delete.
        lambda_function_name: The name of the AWS Lambda function to invoke.

    Returns:
        None:  

    Raises:
        Exception : ClientError: When failed to delete the event rule.
    """
    try:
        eventbridge_client.remove_targets(
            Rule=event_rule_name, Ids=[lambda_function_name])
        eventbridge_client.delete_rule(Name=event_rule_name)
        logger.info("Removed rule %s.", event_rule_name)
    except ClientError:
        logger.exception("Couldn't remove rule %s.", event_rule_name)
        raise
