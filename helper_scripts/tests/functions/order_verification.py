import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

TABLE_NAME = "ProductAvailability"
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/388200338775/test"

def verify_order(event, context):
    table = dynamodb.Table(TABLE_NAME)
    for record in event['Records']:
        order = json.loads(record['body'])
        product_id = order['items'][0]['productId']

        try:
            response = table.get_item(Key={'productId': product_id})
            if 'Item' not in response:
                raise ValueError("Product not available")

            # sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps(order))
        except ClientError as e:
            print(f"DynamoDB Error: {e}")
        except ValueError as e:
            print(f"Validation Error: {e}")
