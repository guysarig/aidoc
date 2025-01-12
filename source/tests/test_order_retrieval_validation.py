# import json
# import pytest
# import boto3
# from botocore.stub import Stubber
# from lambdafunctions.order_retrieval.main import lambda_handler

# def test_retrieve_order_success():
#     sqs = boto3.client('sqs')
#     sqs_stub = Stubber(sqs)
#     sqs_stub.add_response(
#         "receive_message",
#         {
#             "Messages": [
#                 {
#                     "Body": json.dumps({"orderId": "123456"}),
#                     "ReceiptHandle": "rh123"
#                 }
#             ]
#         },
#         {"QueueUrl": "your-queue-url", "MaxNumberOfMessages": 1}
#     )

#     sqs_stub.add_response(
#         "delete_message",
#         {},
#         {"QueueUrl": "your-queue-url", "ReceiptHandle": "rh123"}
#     )

#     event = {}

#     with sqs_stub:
#         response = retrieve_order(event, None)
#         assert response["statusCode"] == 200
#         assert "orderId" in json.loads(response["body"])
#         sqs_stub.assert_no_pending_responses()

# def test_retrieve_order_no_orders():
#     sqs = boto3.client('sqs')
#     sqs_stub = Stubber(sqs)
#     sqs_stub.add_response(
#         "receive_message",
#         {},
#         {"QueueUrl": "your-queue-url", "MaxNumberOfMessages": 1}
#     )

#     event = {}

#     with sqs_stub:
#         response = retrieve_order(event, None)
#         assert response["statusCode"] == 404
#         sqs_stub.assert_no_pending_responses()