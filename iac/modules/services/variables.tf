variable "region" {
  description = "The AWS region"
  type        = string
}
variable "resource_prefix" {
  description = "Prefix to be used for all resource names"
  type        = string
}

variable "queue_url" {
  description = "URL of the SQS queue"
  type        = string
}

variable "queue_arn" {
  description = "ARN of the SQS queue"
  type        = string
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
}

variable "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  type        = string
}

variable "orders_bucket_name" {
  description = "Name of the S3 bucket for orders"
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

variable "lambda_payloads_dir" {
  description = "Directory for Lambda payloads"
  type        = string
}