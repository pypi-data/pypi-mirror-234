#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Functions for interacting with AWS S3."""

import os

from pathlib import Path
from typing import Optional, Tuple

import boto3
import pandas as pd

from ..log import get_logger
from .session import get_boto_session

try:
    import StringIO
except ImportError:
    from io import StringIO

logger = get_logger(__name__)


def get_s3_resource(creds: dict) -> boto3.resources.base.ServiceResource:
    """Get an S3 resource

    Args:
        creds: AWS credentials

    Returns:
        boto3.resources.base.ServiceResource: S3 resource
    """
    logger.info("Getting S3 resource")
    return get_boto_session(creds).resource("s3")


def download_s3_directory(
    s3_resource: boto3.resources.base.ServiceResource,
    s3_bucket_name: str,
    s3_path: str,
    local_path: str,
) -> None:
    """Download an S3 directory to a local directory


    Args:
        s3_resource: Amazon S3 resource
        s3_bucket_name: S3 Bucket name
        s3_path: S3 path to download
        local_path:  Local path to download to

    Returns:
        None: None
    """
    Path(local_path).mkdir(parents=True, exist_ok=True)

    logger.info(
        f"Downloading S3 directory {s3_path} from bucket {s3_bucket_name} to {local_path}"
    )
    for obj in s3_resource.Bucket(s3_bucket_name).objects.filter(
        Prefix=s3_path
    ):
        # We want to preserve the folder structure, so we need to remove the
        # S3 path from the object key.
        s3_base_path = s3_path if s3_path.endswith("/") else s3_path + "/"
        local_file_path = os.path.join(
            local_path, obj.key.replace(s3_base_path, "")
        )
        print(f"Downloading {obj.key} to {local_file_path}")
        if not os.path.exists(os.path.dirname(local_file_path)):
            os.makedirs(os.path.dirname(local_file_path))

        s3_resource.meta.client.download_file(
            s3_bucket_name,
            obj.key,
            local_file_path,
        )


def upload_file_to_s3(
    creds: dict,
    local_file_path: str,
    s3_bucket_name: str,
    s3_path: str,
) -> None:
    """Uploads a file to an S3 directory.

    Args:
        creds: AWS credentials
        local_file_path: Local file path to upload.
        s3_bucket_name: S3 Bucket name
        s3_path: S3 path to upload the file to.
    """
    s3_resource = get_s3_resource(creds)
    s3_resource.meta.client.upload_file(
        local_file_path, s3_bucket_name, s3_path
    )


def parse_s3_path(s3_path: str) -> Tuple[str, str]:
    """Parses an S3 path into a bucket name and path.

    Args:
        s3_path: Complete S3 path.

    Returns:
        Tuple[str, str]: Tuple containing bucket name and path.
    """
    s3_bucket = s3_path.split("://")[1].split("/")[0]
    s3_file_location = "/".join(s3_path.split("://")[1].split("/")[1:])
    return s3_bucket, s3_file_location


def pd_to_csv_s3(
    df: pd.DataFrame,
    s3_bucket_name: str,
    s3_path: str,
    s3_resource,
    index: bool = False,
    header: bool = False,
) -> None:
    """Saves a pandas DataFrame to an S3 directory.

    Args:
        df: Pandas DataFrame to save.
        s3_bucket_name: S3 Bucket name
        s3_path: S3 path to save the DataFrame.
        s3_resource: Amazon S3 resource
        index: Wether to save the index while converting to CSV.
        header: Wether to save the header while converting to CSV.

    Returns:
        None: None
    """
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=index, header=header)
    s3_resource.Object(s3_bucket_name, s3_path).put(Body=csv_buffer.getvalue())


def read_csv_from_s3(
    creds: dict,
    s3_location: str,
    header: Optional[int] = None,
    index: Optional[str] = None,
) -> pd.DataFrame:
    """Reads a CSV from an S3 directory.

    Args:
        creds: AWS credentials
        s3_location: S3 location of the CSV.
        header:  Number of header rows to skip.
        index: Name of the index column.

    Returns:
        pd.DataFrame:
    """

    boto_session = get_boto_session(creds)
    s3_client = boto_session.client("s3")

    s3_bucket, s3_file_location = parse_s3_path(s3_location)
    csv_obj = s3_client.get_object(Bucket=s3_bucket, Key=s3_file_location)

    body = csv_obj["Body"]
    csv_string = body.read().decode("utf-8")
    return pd.read_csv(StringIO(csv_string), header=header, index_col=index)


def copy_s3_to_s3(
    s3_resource: boto3.resources.base.ServiceResource,
    source: str,
    destination: str,
    delete_source: bool = False,
) -> None:
    """Copy an S3 object to another S3 object.

    Args:
        s3_resource: Amazon S3 resource
        source: S3 source path
        destination: S3 destination path
        delete_source: Wether to delete the source after copying.
    """
    logger.info(
        f"Copying {source} to {destination} with delete_source={delete_source}"
    )
    source_bucket_name, source_prefix = parse_s3_path(source)
    dest_bucket_name, dest_prefix = parse_s3_path(destination)

    source_bucket = s3_resource.Bucket(source_bucket_name)
    dest_bucket = s3_resource.Bucket(dest_bucket_name)

    for obj in source_bucket.objects.filter(Prefix=source_prefix):
        logger.info(f"Copying {obj.key} to {dest_prefix}")
        source = {"Bucket": source_bucket_name, "Key": obj.key}
        new_key = obj.key.replace(source_prefix, dest_prefix, 1)
        new_obj = dest_bucket.Object(new_key)
        new_obj.copy(source)

        if delete_source:
            obj.delete()
