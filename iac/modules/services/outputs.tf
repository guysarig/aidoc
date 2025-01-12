output "order_verification_lambda_arn" {
  value = aws_lambda_function.order_verification.arn
}

output "order_verification_lambda_name" {
  value = aws_lambda_function.order_verification.function_name
} 

output "order_api_key" {
  value = aws_api_gateway_api_key.order_api_key.value
  sensitive = true  # Mark as sensitive to prevent it from being logged
}

output "api_gateway_url" {
  value = "https://${aws_api_gateway_rest_api.order_api.id}.execute-api.${var.region}.amazonaws.com/prod/${aws_api_gateway_resource.process_resource.path_part}"
  description = "The full URL of the API Gateway endpoint for the process resource"
}