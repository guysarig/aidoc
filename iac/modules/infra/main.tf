resource "aws_sqs_queue" "order_queue" {
  name = "${var.resource_prefix}-${var.order_queue_name}"
}

resource "aws_dynamodb_table" "product_table" {
  name           = "${var.resource_prefix}-${var.product_table_name}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "productId"

  attribute {
    name = "productId"
    type = "S"
  }
} 