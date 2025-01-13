
# Root level outputs
output "queue_url" {
  value = module.infra.queue_url
}

output "dynamodb_table_name" {
  value = module.infra.dynamodb_table_name
}

output "order_verification_lambda_arn" {
  value = module.services.order_verification_lambda_arn
}

output "order_api_key" {
  value = module.services.order_api_key
  sensitive = true
}

output "order_api_gateway_url" {
  value = module.services.api_gateway_url
}