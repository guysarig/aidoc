LAMBDA_PAYLOADS_DIR=lambda_payloads
BUCKET_NAME=aidoc-devops-cloud-ex-bucket3
# aws s3 rm s3://$BUCKET_NAME --recursive
# aws dynamodb put-item --table-name aidoc-Devops1-ex-ProductAvailability --item '{"productId": {"S": "P001"}, "productName": {"S": "Wireless Mouse"}, "quantity": {"N": "2"}, "price": {"N": "25.99"}}'
# python3 helper_scripts/init_s3_backend.py $BUCKET_NAME eu-west-1 tf/wrapper
cd source
sh ../helper_scripts/build_lambda.sh lambdafunctions order_verification requirements.txt $LAMBDA_PAYLOADS_DIR $BUCKET_NAME
sh ../helper_scripts/build_lambda.sh lambdafunctions order_retrieval requirements.txt $LAMBDA_PAYLOADS_DIR $BUCKET_NAME
cd ..
# cd iac && terraform init && terraform apply && cd ..
