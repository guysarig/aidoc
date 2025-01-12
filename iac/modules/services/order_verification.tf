data "aws_s3_object" "order_verification_zip" {
  bucket = var.orders_bucket_name
  key    = "${var.lambda_payloads_dir}/${var.order_verification_lambda_name}.zip"
}

resource "aws_lambda_function" "order_verification" {
  function_name    = "${var.resource_prefix}-order-verification"
  handler          = "main.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.order_verification.arn
  s3_bucket        = var.orders_bucket_name
  s3_key           = "${var.lambda_payloads_dir}/${var.order_verification_lambda_name}.zip"
  source_code_hash = data.aws_s3_object.order_verification_zip.etag

  environment {
    variables = {
      DYNAMODB_TABLE = var.dynamodb_table_name
      SQS_QUEUE_URL  = var.queue_url
    }
  }
}

resource "aws_iam_role" "order_verification" {
  name = "${var.resource_prefix}-order-verification_-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
      }
    ]
  })
}

resource "aws_iam_role_policy" "order_verification_policy" {
  name = "${var.resource_prefix}-lambda-exec-policy"
  role = aws_iam_role.order_verification.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = [var.queue_arn]
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query"
        ]
        Resource = [var.dynamodb_table_arn]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject"
        ]
        Resource = "*"
      },
      
    ]
  })
}


resource "aws_s3_bucket_notification" "order_notifications" {
  bucket = var.orders_bucket_name

  lambda_function {
    lambda_function_arn = aws_lambda_function.order_verification.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "orders/"
    filter_suffix       = ".json"
  }

  depends_on = [aws_lambda_permission.allow_s3]
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.order_verification.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${var.orders_bucket_name}"
}
