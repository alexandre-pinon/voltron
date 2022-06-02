import json
import time
import uuid
import hashlib

import boto3
import botocore.exceptions
import sure  # noqa # pylint: disable=unused-import
from botocore.exceptions import ClientError
from freezegun import freeze_time
from moto import mock_sqs, settings

from unittest import SkipTest, mock

import pytest
from moto.core import ACCOUNT_ID
from moto.sqs.models import (
    Queue,
    MAXIMUM_MESSAGE_SIZE_ATTR_LOWER_BOUND,
    MAXIMUM_MESSAGE_SIZE_ATTR_UPPER_BOUND,
    MAXIMUM_MESSAGE_LENGTH,
)
from uuid import uuid4

TEST_POLICY = """
{
  "Version":"2012-10-17",
  "Statement":[
    {
      "Effect": "Allow",
      "Principal": { "AWS": "*" },
      "Action": "sqs:SendMessage",
      "Resource": "'$sqs_queue_arn'",
      "Condition":{
        "ArnEquals":{
        "aws:SourceArn":"'$sns_topic_arn'"
        }
      }
    }
  ]
}
"""

@mock_sqs
def test_create_fifo_queue():
    # given
    region_name = "us-east-1"
    sqs = boto3.client("sqs", region_name=region_name)
    queue_name = f"{str(uuid4())[0:6]}.fifo"

    # when
    queue_url = sqs.create_queue(
        QueueName=queue_name, Attributes={"FifoQueue": "true"}
    )["QueueUrl"]

    # then
    queue_url.should.contain(queue_name)

    attributes = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["All"])[
        "Attributes"
    ]
    attributes["ApproximateNumberOfMessages"].should.equal("0")
    attributes["ApproximateNumberOfMessagesNotVisible"].should.equal("0")
    attributes["ApproximateNumberOfMessagesDelayed"].should.equal("0")
    attributes["CreatedTimestamp"].should.be.a(str)
    attributes["ContentBasedDeduplication"].should.equal("false")
    attributes["DeduplicationScope"].should.equal("queue")
    attributes["DelaySeconds"].should.equal("0")
    attributes["LastModifiedTimestamp"].should.be.a(str)
    attributes["FifoQueue"].should.equal("true")
    attributes["FifoThroughputLimit"].should.equal("perQueue")
    attributes["MaximumMessageSize"].should.equal("262144")
    attributes["MessageRetentionPeriod"].should.equal("345600")
    attributes["QueueArn"].should.equal(
        f"arn:aws:sqs:{region_name}:{ACCOUNT_ID}:{queue_name}"
    )
    attributes["ReceiveMessageWaitTimeSeconds"].should.equal("0")
    attributes["VisibilityTimeout"].should.equal("30")

@mock_sqs
def test_create_queue():
    sqs = boto3.resource("sqs", region_name="us-east-1")

    q_name = str(uuid4())[0:6]
    new_queue = sqs.create_queue(QueueName=q_name)
    new_queue.should.have.property("url").should.contain(q_name)

    queue = sqs.get_queue_by_name(QueueName=q_name)
    queue.attributes.get("QueueArn").split(":")[-1].should.equal(q_name)
    queue.attributes.get("QueueArn").split(":")[3].should.equal("us-east-1")
    queue.attributes.get("VisibilityTimeout").should.equal("30")

@mock_sqs
def test_get_queue_url():
    client = boto3.client("sqs", region_name="us-east-1")
    q_name = str(uuid4())[0:6]
    client.create_queue(QueueName=q_name)

    response = client.get_queue_url(QueueName=q_name)

    response.should.have.key("QueueUrl").which.should.contain(q_name)

@mock_sqs
def test_message_send_without_attributes():
    sqs = boto3.resource("sqs", region_name="us-east-1")
    queue = sqs.create_queue(QueueName=str(uuid4())[0:6])
    msg = queue.send_message(MessageBody="derp")
    msg.get("MD5OfMessageBody").should.equal("58fd9edd83341c29f1aebba81c31e257")
    msg.shouldnt.have.key("MD5OfMessageAttributes")
    msg.get("MessageId").should_not.contain(" \n")

    messages = queue.receive_messages()
    messages.should.have.length_of(1)


@mock_sqs
def test_message_send_with_attributes():
    sqs = boto3.resource("sqs", region_name="us-east-1")
    queue = sqs.create_queue(QueueName=str(uuid4())[0:6])
    msg = queue.send_message(
        MessageBody="derp",
        MessageAttributes={
            "SOME_Valid.attribute-Name": {
                "StringValue": "1493147359900",
                "DataType": "Number",
            }
        },
    )
    msg.get("MD5OfMessageBody").should.equal("58fd9edd83341c29f1aebba81c31e257")
    msg.get("MD5OfMessageAttributes").should.equal("36655e7e9d7c0e8479fa3f3f42247ae7")
    msg.get("MessageId").should_not.contain(" \n")

    messages = queue.receive_messages()
    messages.should.have.length_of(1)

@mock_sqs
def test_send_receive_message_without_attributes():
    sqs = boto3.resource("sqs", region_name="us-east-1")
    conn = boto3.client("sqs", region_name="us-east-1")
    q_resp = conn.create_queue(QueueName=str(uuid4())[0:6])
    queue = sqs.Queue(q_resp["QueueUrl"])

    body_one = "this is a test message"
    body_two = "this is another test message"

    queue.send_message(MessageBody=body_one)
    queue.send_message(MessageBody=body_two)

    messages = conn.receive_message(QueueUrl=queue.url, MaxNumberOfMessages=2)[
        "Messages"
    ]

    message1 = messages[0]
    message2 = messages[1]

    message1["Body"].should.equal(body_one)
    message2["Body"].should.equal(body_two)

    message1.shouldnt.have.key("MD5OfMessageAttributes")
    message2.shouldnt.have.key("MD5OfMessageAttributes")

    message1.should_not.have.key("Attributes")
    message2.should_not.have.key("Attributes")


@mock_sqs
def test_send_receive_message_with_attributes():
    sqs = boto3.resource("sqs", region_name="us-east-1")
    conn = boto3.client("sqs", region_name="us-east-1")
    q_resp = conn.create_queue(QueueName=str(uuid4())[0:6])
    queue = sqs.Queue(q_resp["QueueUrl"])

    body_one = "this is a test message"
    body_two = "this is another test message"

    queue.send_message(
        MessageBody=body_one,
        MessageAttributes={
            "timestamp": {"StringValue": "1493147359900", "DataType": "Number"}
        },
    )

    queue.send_message(
        MessageBody=body_two,
        MessageAttributes={
            "timestamp": {"StringValue": "1493147359901", "DataType": "Number"}
        },
    )

    messages = conn.receive_message(
        QueueUrl=queue.url, MaxNumberOfMessages=2, MessageAttributeNames=["timestamp"]
    )["Messages"]

    message1 = messages[0]
    message2 = messages[1]

    message1.get("Body").should.equal(body_one)
    message2.get("Body").should.equal(body_two)

    message1.get("MD5OfMessageAttributes").should.equal(
        "235c5c510d26fb653d073faed50ae77c"
    )
    message2.get("MD5OfMessageAttributes").should.equal(
        "994258b45346a2cc3f9cbb611aa7af30"
    )
