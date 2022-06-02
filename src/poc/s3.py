import datetime
import os
from urllib.parse import urlparse, parse_qs
from gzip import GzipFile
from io import BytesIO
import zlib
import pickle
import uuid

import json
import boto3
from botocore.client import ClientError
import botocore.exceptions
from botocore.handlers import disable_signing
from freezegun import freeze_time
import requests

from moto.s3.responses import DEFAULT_REGION_NAME
from unittest import SkipTest
import pytest

import sure  # noqa # pylint: disable=unused-import

from moto import settings, mock_s3, mock_config
import moto.s3.models as s3model
from uuid import uuid4

class MyModel(object):
    def __init__(self, name, value, metadata=None):
        self.name = name
        self.value = value
        self.metadata = metadata or {}

    def save(self):
        s3 = boto3.client("s3", region_name=DEFAULT_REGION_NAME)
        s3.put_object(
            Bucket="mybucket", Key=self.name, Body=self.value, Metadata=self.metadata
        )

@mock_s3
def test_my_model_save():
    # Create Bucket so that test can run
    conn = boto3.resource("s3", region_name=DEFAULT_REGION_NAME)
    conn.create_bucket(Bucket="mybucket")

    model_instance = MyModel("steve", "is awesome")
    model_instance.save()

    body = conn.Object("mybucket", "steve").get()["Body"].read().decode()

    assert body == "is awesome"

@mock_s3
def test_bucket_deletion():
    s3 = boto3.resource("s3", region_name=DEFAULT_REGION_NAME)
    client = boto3.client("s3", region_name=DEFAULT_REGION_NAME)
    client.create_bucket(Bucket="foobar")

    key = s3.Object("foobar", "the-key")
    key.put(Body=b"some value")

    # Try to delete a bucket that still has keys
    with pytest.raises(ClientError) as ex:
        client.delete_bucket(Bucket="foobar")
    ex.value.response["Error"]["Code"].should.equal("BucketNotEmpty")
    ex.value.response["Error"]["Message"].should.equal(
        "The bucket you tried to delete is not empty"
    )

    client.delete_object(Bucket="foobar", Key="the-key")
    client.delete_bucket(Bucket="foobar")

    # Delete non-existent bucket
    with pytest.raises(ClientError) as ex:
        client.delete_bucket(Bucket="foobar")
    ex.value.response["Error"]["Code"].should.equal("NoSuchBucket")
    ex.value.response["Error"]["Message"].should.equal(
        "The specified bucket does not exist"
    )
