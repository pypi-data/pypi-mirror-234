#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Amazon RedShift Connector."""

import urllib.parse
import pandas as pd
import pandas_redshift as pr

from sqlalchemy import create_engine
from sqlalchemy import orm as sa_orm

from ..log import get_logger
from .connector_base import ConnectorBase, register_connector

logger = get_logger(__name__)

@register_connector
class RedShiftConnector(ConnectorBase):
    def __init__(self, creds: dict, db_config: dict, **kwargs) -> None:
        super().__init__(creds, db_config, **kwargs)

        if "aws_config" not in kwargs:
            Exception("No aws_config found")

        self.aws_config = kwargs["aws_config"]
        encoded_password = urllib.parse.quote(creds["password"], safe="")
        connection_string = f"postgresql://{creds['user']}:{encoded_password}@{creds['host']}:{creds['port']}/{db_config['database']}"
        self.engine = create_engine(connection_string)

        Session = sa_orm.sessionmaker()
        Session.configure(bind=self.engine)
        self.connection = Session()
        if db_config.get("schema", None):
            self.connection.execute(f"SET search_path TO {db_config['schema']}")
            self.connection.commit()

    def write_to_table(
        self,
        df: pd.DataFrame,
        table_name: str,
        schema: str = None,
        if_exists: str = "append",
    ):
        table_name, schema = (
            table_name.split(".") if "." in table_name else (table_name, schema)
        )

        try:
            pr.connect_to_redshift(
                dbname=self.db_config["database"],
                host=self.creds["host"],
                port=self.creds["port"],
                user=self.creds["user"],
                password=self.creds["password"],
            )

            s3_bucket = self.creds.get("s3Bucket", None)
            s3_bucket = (
                s3_bucket if s3_bucket is not None else self.aws_config["s3Bucket"]
            )

            s3_sub_dir = self.creds.get("s3SubDirectory", None)
            s3_sub_dir = (
                s3_sub_dir
                if s3_sub_dir is not None
                else self.aws_config["s3SubDirectory"]
            )

            pr.connect_to_s3(
                aws_access_key_id=self.aws_config["access_key_id"],
                aws_secret_access_key=self.aws_config["access_key_secret"],
                bucket=s3_bucket,
                subdirectory=s3_sub_dir
                # As of release 1.1.1 you are able to specify an aws_session_token (if necessary):
                # aws_session_token = <aws_session_token>
            )

            # Write the DataFrame to S3 and then to redshift
            pr.pandas_to_redshift(
                data_frame=df,
                redshift_table_name=f"{schema}.{table_name}",
                append=if_exists == "append",
            )
        except Exception as e:
            logger.error(f"Error while writing to Redshift: {e}")

            #Check for non existing schema
            if "cannot copy into nonexistent table" in str(e).lower():
                self.create_table(df, table_name, schema)
                # Try again
                logger.info("Trying again")
                self.write_to_table(df, table_name, schema, if_exists)
