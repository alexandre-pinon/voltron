import datetime
import time
import pytest

import boto3
from botocore.exceptions import ClientError

from dateutil.tz import tzlocal

from moto import mock_kinesis
from moto.core import ACCOUNT_ID

import sure  # noqa # pylint: disable=unused-import

@mock_kinesis
def test_put_records_boto3():
    client = boto3.client("kinesis", region_name="eu-west-2")

    stream_name = "my_stream_summary"
    client.create_stream(StreamName=stream_name, ShardCount=1)
    stream = client.describe_stream(StreamName=stream_name)["StreamDescription"]
    shard_id = stream["Shards"][0]["ShardId"]

    data = b"hello world"
    partition_key = "1234"

    response = client.put_record(
        StreamName=stream_name, Data=data, PartitionKey=partition_key
    )
    response["SequenceNumber"].should.equal("1")

    resp = client.get_shard_iterator(
        StreamName=stream_name, ShardId=shard_id, ShardIteratorType="TRIM_HORIZON"
    )
    shard_iterator = resp["ShardIterator"]

    resp = client.get_records(ShardIterator=shard_iterator)
    resp["Records"].should.have.length_of(1)
    record = resp["Records"][0]

    record["Data"].should.equal(b"hello world")
    record["PartitionKey"].should.equal("1234")
    record["SequenceNumber"].should.equal("1")

@mock_kinesis
def test_get_records_after_sequence_number_boto3():
    client = boto3.client("kinesis", region_name="eu-west-2")
    stream_name = "my_stream_summary"
    client.create_stream(StreamName=stream_name, ShardCount=1)
    stream = client.describe_stream(StreamName=stream_name)["StreamDescription"]
    shard_id = stream["Shards"][0]["ShardId"]

    for index in range(1, 5):
        client.put_record(
            StreamName=stream_name,
            Data=f"data_{index}".encode("utf-8"),
            PartitionKey=str(index),
        )

    resp = client.get_shard_iterator(
        StreamName=stream_name, ShardId=shard_id, ShardIteratorType="TRIM_HORIZON"
    )
    shard_iterator = resp["ShardIterator"]

    # Retrieve only 2 records
    resp = client.get_records(ShardIterator=shard_iterator, Limit=2)
    sequence_nr = resp["Records"][1]["SequenceNumber"]

    # Then get a new iterator starting at that id
    resp = client.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType="AFTER_SEQUENCE_NUMBER",
        StartingSequenceNumber=sequence_nr,
    )
    shard_iterator = resp["ShardIterator"]

    resp = client.get_records(ShardIterator=shard_iterator)
    # And the first result returned should be the second item
    resp["Records"][0]["SequenceNumber"].should.equal("3")
    resp["Records"][0]["Data"].should.equal(b"data_3")
    resp["MillisBehindLatest"].should.equal(0)


@mock_kinesis
def test_get_records_latest_boto3():
    client = boto3.client("kinesis", region_name="eu-west-2")
    stream_name = "my_stream_summary"
    client.create_stream(StreamName=stream_name, ShardCount=1)
    stream = client.describe_stream(StreamName=stream_name)["StreamDescription"]
    shard_id = stream["Shards"][0]["ShardId"]

    for index in range(1, 5):
        client.put_record(
            StreamName=stream_name,
            Data=f"data_{index}".encode("utf-8"),
            PartitionKey=str(index),
        )

    resp = client.get_shard_iterator(
        StreamName=stream_name, ShardId=shard_id, ShardIteratorType="TRIM_HORIZON"
    )
    shard_iterator = resp["ShardIterator"]

    # Retrieve only 2 records
    resp = client.get_records(ShardIterator=shard_iterator, Limit=2)
    sequence_nr = resp["Records"][1]["SequenceNumber"]

    # Then get a new iterator starting at that id
    resp = client.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType="LATEST",
        StartingSequenceNumber=sequence_nr,
    )
    shard_iterator = resp["ShardIterator"]

    client.put_record(
        StreamName=stream_name, Data=b"last_record", PartitionKey="last_record"
    )

    resp = client.get_records(ShardIterator=shard_iterator)
    # And the first result returned should be the second item
    resp["Records"].should.have.length_of(1)
    resp["Records"][0]["SequenceNumber"].should.equal("5")
    resp["Records"][0]["PartitionKey"].should.equal("last_record")
    resp["Records"][0]["Data"].should.equal(b"last_record")
    resp["MillisBehindLatest"].should.equal(0)
