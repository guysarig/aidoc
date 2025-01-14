import os
import pytest
import json
from moto import mock_aws
import boto3

# Set environment variables before importing the module
os.environ['DYNAMODB_TABLE'] = 'test-table'
os.environ['SQS_QUEUE_URL'] = 'https://sqs.eu-central-1.amazonaws.com/123456789012/test-queue'

from lambdafunctions.order_verification.main import lambda_handler

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'

@pytest.fixture
def s3(aws_credentials):
    with mock_aws():
        yield boto3.client('s3', region_name='eu-central-1')

@pytest.fixture
def dynamodb(aws_credentials):
    with mock_aws():
        yield boto3.resource('dynamodb', region_name='eu-central-1')

@pytest.fixture
def sqs(aws_credentials):
    with mock_aws():
        yield boto3.client('sqs', region_name='eu-central-1')

def test_lambda_handler(s3, dynamodb, sqs):
    # Set up mock S3
    bucket_name = 'aidoc-devops-cloud-ex-bucket3'
    object_key = 'orders/order123456.json'
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'}
    )
    order_data = {
        "items": [
            {"productId": "123"}, 
            {"productId": "456"}
        ]
    }
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=json.dumps(order_data))

    # Set up mock DynamoDB
    table = dynamodb.create_table(
        TableName='test-table',
        KeySchema=[
            {'AttributeName': 'productId', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'productId', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.put_item(Item={'productId': '123'})

    # Set up mock SQS
    sqs.create_queue(QueueName='test-queue')

    # Define the event
    event = {
        'Records': [{
            's3': {
                'bucket': {'name': bucket_name},
                'object': {'key': object_key}
            }
        }]
    }

    # Call the lambda_handler
    lambda_handler(event, None)

    # Verify SQS message
    response = sqs.receive_message(QueueUrl='https://sqs.eu-central-1.amazonaws.com/123456789012/test-queue')
    messages = response.get('Messages', [])
    assert len(messages) == 1
    message_body = json.loads(messages[0]['Body'])
    assert message_body == order_data