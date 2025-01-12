import json
import boto3
import os

sqs = boto3.client('sqs')
QUEUE_URL = os.environ.get("SQS_QUEUE_URL")
VALID_API_KEY = os.environ.get("API_KEY")

def lambda_handler(event, context):
    # Validate API Key 
    headers = event.get("headers", {})
    api_key = headers.get("x-api-key")

    if api_key != VALID_API_KEY:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "Unauthorized"})
        }

    try:
        # Retrieve a message from the SQS queue
        response = sqs.receive_message(QueueUrl=QUEUE_URL, MaxNumberOfMessages=1)
        print(f"SQS response: {response}")

        if "Messages" not in response:
            return {"statusCode": 404, "body": json.dumps({"error": "No orders available"})}

        # Extract and delete the message
        message = response["Messages"][0]
        sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=message["ReceiptHandle"])

        return {
            "statusCode": 200,
            "body": json.dumps({"order": json.loads(message["Body"])}),
        }

    except Exception as e:
        print(f"Error retrieving order: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to retrieve order", "details": str(e)})
        }