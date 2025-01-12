import json
import boto3
from flask import Flask, request, jsonify
from functools import wraps
from aws_lambda_wsgi import response as wsgi_response, WSGIHandler

# Initialize Flask app
app = Flask(__name__)

# Initialize SQS client
sqs = boto3.client('sqs')
QUEUE_URL = "your-queue-url"

# Authentication decorator
def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or auth != "Bearer your-token":
            return jsonify({"message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Expose /process endpoint
@app.route('/process', methods=['POST'])
# @authenticate
def process_order():
    response = sqs.receive_message(QueueUrl=QUEUE_URL, MaxNumberOfMessages=1)
    if 'Messages' not in response:
        return jsonify({"statusCode": 404, "body": "No orders available"})

    order = response['Messages'][0]
    sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=order['ReceiptHandle'])

    return jsonify({"statusCode": 200, "body": json.loads(order['Body'])})

# Lambda handler
def lambda_handler(event, context):
    # Convert API Gateway event to WSGI request
    return wsgi_response(app, event, context)
