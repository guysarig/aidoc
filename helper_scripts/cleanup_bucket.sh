LAMBDA_PAYLOADS_DIR=lambda_payloads
BUCKET_NAME=aidoc-devops-test
aws s3 rm s3://$BUCKET_NAME --recursive
