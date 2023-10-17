"""
Data needs to be loaded from wh with the given input credentials and input features. This has helper functions to load the data
This will be used in both feature_processing and predict notebooks to load the data from warehouse.
"""

import pandas as pd

from rudderlabs.data.apps.aws.s3 import read_csv_from_s3
from rudderlabs.data.apps.wh import Connector


class DataIO:
    def __init__(self, notebook_config: dict, creds_config: dict) -> None:
        self.notebook_config = notebook_config
        self.creds_config = creds_config

        # Expect table information(name, schema, database) from data_warehouse section of
        # credentials configurations
        self.database = creds_config["data_warehouse"]["database"]
        self.schema = creds_config["data_warehouse"]["schema"]
        self.feature_store_table = creds_config["data_warehouse"][
            "feature_store_table"
        ]
        self.prediction_store_table = creds_config["data_warehouse"][
            "prediction_store_table"
        ]

    def get_warehouse_connector(self) -> Connector:
        """Returns warehouse connector

        Returns:
            Connector: Warehouse connector
        """
        warehouse_creds = self.creds_config["data_warehouse"]
        aws_config = self.creds_config["aws"]

        wh_connector = Connector(warehouse_creds, aws_config=aws_config)
        return wh_connector

    def get_data(self) -> pd.DataFrame:
        """Method for getting data from warehouse/feature store/other data sources."""

        query_string = self.notebook_config.get("query_train_data", "")
        df = pd.DataFrame()

        try:
            wh_connector = self.get_warehouse_connector()
            df = wh_connector.run_query(query_string)
        except Exception as e:
            print(str(e))

        return df

    def get_data_for_prediction(self) -> pd.DataFrame:
        """Method for getting data from warehouse/feature store/other data sources."""
        print("Getting data for prediction")
        s3_location = "s3://data-apps-sample-datasets/lead_scoring/data_for_prediction.csv"
        df = read_csv_from_s3(self.creds_config, s3_location, header=0)
        return df

    def get_data_from_s3(self, s3_location: str) -> pd.DataFrame:
        """Method for getting data from warehouse/feature store/other data sources."""
        print("Getting data from s3")
        df = read_csv_from_s3(self.creds_config, s3_location, header=0)
        return df

    def write_to_wh_table(
        self,
        df: pd.DataFrame,
        table_name: str,
        schema: str = None,
        if_exists: str = "append",
    ) -> None:
        """Writes dataframe to warehouse feature store table.

        Args:
            df (pd.DataFrame): Dataframe to be written to warehouse feature store table
            table_name (str): Feature store table name
            schema (str, optional): Schema name, Defaults to None.
            if_exists (str, optional): {"append", "replace", "fail"} Defaults to "append".
                fail: If the table already exists, the write fails.
                replace: If the table already exists, the table is dropped and the write is executed.
                append: If the table already exists, the write is executed with new rows appended to existing table
        """
        print("Writing to warehouse")
        warehouse_creds = self.creds_config["data_warehouse"]
        aws_config = self.creds_config["aws"]

        wh_connector = Connector(warehouse_creds, aws_config=aws_config)
        wh_connector.write_to_table(df, table_name, schema, if_exists)

    def update_wh_table(
        self, data: dict, table_name: str, schema: str, where: str
    ) -> None:
        """Updates warehouse table with data.

        Args:
            data (dict): Data to be updated in warehouse table
            table_name (str): Table name
            schema (str, optional): Schema name, Defaults to None.
        """
        print("Updating warehouse")
        wh_connector = self.get_warehouse_connector()
        update_values = ", ".join([f"{k} = '{v}'" for k, v in data.items()])
        sql_query = (
            f"UPDATE {schema}.{table_name} SET {update_values} WHERE {where}"
        )

        wh_connector.run_query(sql_query)
