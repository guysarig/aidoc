variable "region" {
  description = "AWS region"
  type        = string
}

variable "provider_default_tags" {
  description = "Default tags for all resources"
  type        = map(string)
  default     = {}
}

variable "resource_prefix" {
  description = "Prefix to be used for all resource names"
  type        = string
}

variable "order_verification_lambda_name" {
  description = "Name of the Lambda function for order verification"
  type        = string
}

variable "order_retrieval_lambda_name" {
  description = "Name of the Lambda function for order retrieval"
  type        = string
}

variable "orders_bucket_name" {
  description = "Name of the S3 bucket for orders"
  type        = string
}

variable "order_queue_name" {
  description = "Name of the SQS queue"
  type        = string
}

variable "product_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
}

variable "lambda_payloads_dir" {
  description = "Directory for Lambda payloads"
  type        = string
}