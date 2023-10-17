#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module for handling various warehouse connections"""

from typing import Union

from .connector_base import connector_classes
from .redshift_connector import RedShiftConnector
from .snowflake_connector import SnowflakeConnector

def ProfilesConnector(config: dict, **kwargs) -> Union[RedShiftConnector, SnowflakeConnector]:
    """Creates a connector object based on the config provided

    Args:
        config: A dictionary containing the credentials and database information for the connector.
        **kwargs: Additional keyword arguments to pass to the connector.

    Returns:
        ConnectorBase: Connector object.

    Raises:
        Exception: Connector not found
    """

    warehouse_type = config.get("type").lower()
    connector = connector_classes.get(warehouse_type, None)
    if connector is None:
        raise Exception(f"Connector {warehouse_type} not found")

    aws_config = kwargs["aws_config"];  
    creds = {
        "user": config.get("user"),
        "password": config.get("password"),
        "account_identifier": config.get("account"),
        "warehouse": config.get("warehouse"),
        "host": config.get("host"),
        "port": config.get("port"),
        "s3Bucket": aws_config.get("bucket"),
        "s3SubDirectory": aws_config.get("path")
    }

    if "role" in config:
        creds["role"] = config.get("role")

    db_config = {
        "database": config.get("dbname"),
        "schema": config.get("schema")
    }

    connector = connector(creds, db_config, **kwargs)
    return connector

def ConnectorNew(config: dict, warehouse: str, **kwargs) -> Union[RedShiftConnector, SnowflakeConnector]:
    """Creates a connector object based on the config provided

    Args:
        config: A dictionary containing the credentials and database information for the connector.
        warehouse: The warehouse name to be used
        **kwargs: Additional keyword arguments to pass to the connector.

    Returns:
        ConnectorBase: Connector object.

    Raises:
        Exception: Connector not found
    """

    connector = connector_classes.get(warehouse.lower(), None)
    if connector is None:
        raise Exception(f"Connector {warehouse} not found")

    creds = {
        "user": config.get("user"),
        "password": config.get("password"),
        "account_identifier": config.get("account"),
        "warehouse": config.get("warehouse")
    }

    db_config = {
        "database": config.get("dbname"),
        "schema": config.get("schema")
    }

    connector = connector(creds, db_config, **kwargs)
    return connector

def Connector(
    config: dict, **kwargs
) -> Union[RedShiftConnector, SnowflakeConnector]:
    """Creates a connector object based on the config provided

    Args:
        config: A dictionary containing the configuration for the connector.
        **kwargs: Additional keyword arguments to pass to the connector.

    Returns:
        ConnectorBase: Connector object.

    Raises:
        Exception: No Credentials found
        Exception: Connector not found
    """

    #When using explicit warehouse name, config can be treated as credentials
    name = config.get("name").lower() if "name" in config else ""
    creds = config.get(name) if name in config else None

    if creds is None:
        raise Exception("No credentials found for {}".format(name))

    connector = connector_classes.get(name, None)
    if connector is None:
        raise Exception(f"Connector {name} not found")

    connector = connector(creds, config, **kwargs)
    return connector
