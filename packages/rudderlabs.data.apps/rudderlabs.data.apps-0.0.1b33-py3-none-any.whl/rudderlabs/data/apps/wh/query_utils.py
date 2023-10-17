#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provides utility functions for query execution."""

from typing import Optional

from ..log import get_logger

logger = get_logger(__name__)


def get_timestamp_where_condition(
    timestamp_column: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> Optional[str]:
    """Prepares time stamp where condition for SQL query.

    Args:
        timestamp_column (str): Timestamp column name
        start_time (Optional[str]): Start time
        end_time (Optional[str]): End time

    Returns:
        Optional[str]: Where condition or None if no time condition is needed
    """
    if start_time:
        if end_time:
            logger.debug(
                "Feature start date and end date too are given, "
                "so they is used to filter the data"
            )
            timestamp_condition = (
                f"{timestamp_column} between '{start_time}' and '{end_time}'"
            )
        else:
            logger.debug(
                "Feature start date is given, so it is used to filter the data"
            )
            timestamp_condition = f"{timestamp_column} >= '{start_time}'"
    elif end_time:
        logger.debug(
            "Feature end date is given, so it is used to filter the data"
        )
        timestamp_condition = f"{timestamp_column} <= '{end_time}'"
    else:
        logger.debug(
            "Neither start time nor end time defined. So the query runs on all dataset"
        )
        timestamp_condition = None
    return timestamp_condition
