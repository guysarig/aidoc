cd iac
API_KEY=$(terraform output -raw order_api_key)
API_URL=$(terraform output -raw order_api_gateway_url)
echo "API_KEY: $API_KEY"
echo "API_URL: $API_URL"
curl -X POST "$API_URL" \
    -H "x-api-key: $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"your": "payload"}'
cd ..