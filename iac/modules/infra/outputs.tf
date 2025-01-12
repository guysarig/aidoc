output "queue_arn" {
  value = aws_sqs_queue.order_queue.arn
}

output "queue_url" {
  value = aws_sqs_queue.order_queue.url
}

output "dynamodb_table_arn" {
  value = aws_dynamodb_table.product_table.arn
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.product_table.name
} 