import json
import pytest
import boto3
from botocore.stub import Stubber
from functions.order_verification import verify_order

def test_verify_order_success():
    dynamodb = boto3.client('dynamodb')
    sqs = boto3.client('sqs')

    dynamodb_stub = Stubber(dynamodb)
    sqs_stub = Stubber(sqs)

    dynamodb_stub.add_response(
        "get_item",
        {"Item": {"productId": {"S": "P001"}}},
        {"TableName": "ProductAvailability", "Key": {"productId": {"S": "P001"}}}
    )

    sqs_stub.add_response(
        "send_message",
        {"MessageId": "msg123"},
        {"QueueUrl": "your-queue-url", "MessageBody": json.dumps({"orderId": "123456"})}
    )

    event = {
        "Records": [
            {"body": json.dumps({"orderId": "123456", "items": [{"productId": "P001"}]})}
        ]
    }

    # Activate stubs
    dynamodb_stub.activate()
    sqs_stub.activate()

    with dynamodb_stub, sqs_stub:
        # try:
        verify_order(event, None)
        # except Exception as e:
        #     print(f"Error during verify_order execution: {e}")
        dynamodb_stub.assert_no_pending_responses()
        # sqs_stub.assert_no_pending_responses()