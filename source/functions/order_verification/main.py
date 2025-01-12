import json
import os
import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')
s3 = boto3.client('s3')
TABLE_NAME = os.environ['DYNAMODB_TABLE']
QUEUE_URL = os.environ['SQS_QUEUE_URL']

def lambda_handler(event, context):
    print(f"Received event: {event}")
    print(f"Received context: {context}")
    print(f"Received SQS_QUEUE_URL: {QUEUE_URL}")
    print(f"Received TABLE_NAME: {TABLE_NAME}")
    
    table = dynamodb.Table(TABLE_NAME)
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        
        # Fetch the JSON file from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        order = json.loads(response['Body'].read().decode('utf-8'))
        
        for item in order['items']:  # Iterate over all items
            product_id = item['productId']  # Access each productId
            print(f"Processing product ID: {product_id}")
            try:
                response = table.get_item(Key={'productId': product_id})
                if 'Item' not in response:
                    raise ValueError(f"Product {product_id} not available")

                sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps(order))
            except ClientError as e:
                print(f"DynamoDB Error: {e}")
            except ValueError as e:
                print(f"Validation Error: {e}")