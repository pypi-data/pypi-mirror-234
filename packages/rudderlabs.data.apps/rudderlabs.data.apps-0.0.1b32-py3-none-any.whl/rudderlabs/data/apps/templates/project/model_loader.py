"""
Running queries on the model registry.
"""
import tempfile

from rudderlabs.data.apps.aws.s3 import (
    download_s3_directory,
    get_s3_resource,
    parse_s3_path,
)
from rudderlabs.data.apps.wh import Connector


class ModelLoader:
    def __init__(self, creds_config: dict) -> None:
        self.creds_config = creds_config

        # Expect table information(name, schema, database) from data_warehouse section of
        # credentials configurations
        self.database = creds_config["data_warehouse"]["database"]
        self.schema = creds_config["data_warehouse"]["schema"]
        self.model_registry_table = creds_config["data_warehouse"][
            "model_registry_table"
        ]

    def get_connector(self):
        """Returns a connector object."""
        warehouse_creds = self.creds_config["data_warehouse"]
        aws_config = self.creds_config["aws"]

        wh_connector = Connector(warehouse_creds, aws_config=aws_config)
        return wh_connector

    def get_latest_model(self, model_type, job_id=None) -> dict:
        """Returns the latest model of a given type.

        Args:
            model_type: The type of model to return.
            job_id: The job_id of the model to return.

        Returns:
            dict: The latest model of the given type.
        """

        # Get the latest model staged in the model registry
        # Prepare where condition
        where_condition = f"model_type = '{model_type}'"
        if job_id:
            where_condition += f" and job_id = '{job_id}'"

        query = f"""
            SELECT * FROM {self.database}.{self.schema}.{self.model_registry_table}
            WHERE {where_condition}
            ORDER BY timestamp DESC
            LIMIT 1
        """

        connector = self.get_connector()
        df = connector.run_query(query)
        model_data = df.to_dict(orient="records")

        if len(model_data):
            model_data = model_data[0]

        return model_data

    def download_model_files_to_temp(self, model_data: dict) -> None:
        """Downloads the model files from S3 to local path.

        Args:
            model_data (dict): The model data.
            local_path (str): The local path to download the model files to.
        """
        if not model_data:
            return None

        temp_folder = tempfile.mkdtemp()
        print(f"Downloading model data to temporary location {temp_folder}")

        s3_bucket, s3_prefix = parse_s3_path(model_data["model_files_location"])
        s3_resource = get_s3_resource(self.creds_config)

        download_s3_directory(s3_resource, s3_bucket, s3_prefix, temp_folder)
        return temp_folder
