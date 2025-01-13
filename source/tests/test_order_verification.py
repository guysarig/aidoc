import os
import json
import pytest
import boto3
from time import sleep
import botocore

LOCALSTACK_URL = "http://localhost:4566"
REGION_NAME    = "eu-central-1"

os.environ["DYNAMODB_TABLE"] = "test-table"
os.environ["SQS_QUEUE_URL"]  = "http://localhost:4566/000000000000/test-queue"  # or your ARNs

# Suppose your application code imports these env vars
# from lambdafunctions.order_verification.main import lambda_handler

def create_s3_bucket_if_not_exists(s3_client, bucket_name):
    """Create an S3 bucket only if it does not already exist."""
    try:
        # Check if the bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except botocore.exceptions.ClientError as e:
        # If the bucket does not exist (404), create it
        if e.response['Error']['Code'] == '404':
            print(f"Bucket '{bucket_name}' does not exist. Creating it.")
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": REGION_NAME}
            )
        else:
            # Raise other errors
            raise


@pytest.fixture(scope="session", autouse=True)
def setup_localstack_resources():
    """
    One-time setup to create the local resources (S3 bucket, DynamoDB table, SQS queue) in LocalStack.
    """
    s3_client = boto3.client("s3", endpoint_url=LOCALSTACK_URL, region_name=REGION_NAME)

    # Create S3 bucket and add policy
    create_s3_bucket_if_not_exists(s3_client, "my-test-bucket1")
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::my-test-bucket1/*"
            }
        ]
    }
    s3_client.put_bucket_policy(Bucket="my-test-bucket1", Policy=json.dumps(bucket_policy))

    # Debugging
    print("Bucket policy applied:", s3_client.get_bucket_policy(Bucket="my-test-bucket1")["Policy"])

    # Create DynamoDB table
    ddb_client = boto3.client("dynamodb", endpoint_url=LOCALSTACK_URL, region_name=REGION_NAME)
    try:
        ddb_client.create_table(
            TableName="test-table",
            KeySchema=[{"AttributeName": "productId", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "productId", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
    except ddb_client.exceptions.ResourceInUseException:
        print("DynamoDB table 'test-table' already exists.")

    # Create SQS queue
    sqs_client = boto3.client("sqs", endpoint_url=LOCALSTACK_URL, region_name=REGION_NAME)
    try:
        sqs_client.create_queue(QueueName="test-queue")
    except sqs_client.exceptions.QueueNameExists:
        print("SQS queue 'test-queue' already exists.")

    yield


def test_integration_localstack():
    """
    Example integration test calling your lambda_handler
    that expects an S3 event, checks DynamoDB, and sends a message to SQS.
    """
    # Setup test data
    s3_client = boto3.client("s3", endpoint_url=LOCALSTACK_URL, region_name=REGION_NAME)
    ddb_client = boto3.client("dynamodb", endpoint_url=LOCALSTACK_URL, region_name=REGION_NAME)
    sqs_client = boto3.client("sqs", endpoint_url=LOCALSTACK_URL, region_name=REGION_NAME)

    # Put an item in the DDB table
    ddb_client.put_item(
        TableName="test-table",
        Item={"productId": {"S": "123"}}
    )

    # Upload a JSON order file to S3
    order_data = {"items": [{"productId": "123"}]}
    s3_client.put_object(
        Bucket="my-test-bucket1",
        Key="orders/order123.json",
        Body=json.dumps(order_data),
    )

    # Create a test S3 event
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "my-test-bucket1"},
                    "object": {"key": "orders/order123.json"},
                }
            }
        ]
    }

    # Call your lambda handler
    from lambdafunctions.order_verification.main import lambda_handler
    lambda_handler(event, None)

    # Check the queue for messages
    queue_url = "http://localhost:4566/000000000000/test-queue"
    msgs = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
    messages = msgs.get("Messages", [])
    assert len(messages) == 1, "Expected exactly one SQS message"
    body = json.loads(messages[0]["Body"])
    assert body == order_data, "Message body should match the uploaded order data"
