### Lambda Function
data "aws_s3_object" "order_retrieval_zip" {
  bucket = var.orders_bucket_name
  key    = "${var.lambda_payloads_dir}/${var.order_retrieval_lambda_name}.zip"
}

resource "aws_lambda_function" "order_retrieval" {
  function_name    = "${var.resource_prefix}-order-retrieval"
  handler          = "main.lambda_handler"  # Update this line
  runtime          = "python3.9"
  role             = aws_iam_role.order_retrieval_lambda_role.arn
  s3_bucket        = var.orders_bucket_name
  s3_key           = "${var.lambda_payloads_dir}/${var.order_retrieval_lambda_name}.zip"
  source_code_hash = data.aws_s3_object.order_retrieval_zip.etag

  environment {
    variables = {
      SQS_QUEUE_URL = var.queue_url
      API_KEY       = aws_api_gateway_api_key.order_api_key.value
    }
  }
  depends_on = [aws_api_gateway_api_key.order_api_key]
}


resource "aws_iam_role" "order_retrieval_lambda_role" {
  name = "${var.resource_prefix}-order-retrieval_-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "order_retrieval_lambda_policy" {
  name = "${var.resource_prefix}-order-retrieval-lambda-policy"
  role = aws_iam_role.order_retrieval_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            Action = [
            "sqs:ReceiveMessage",
            "sqs:DeleteMessage",
            "sqs:GetQueueAttributes"
            ]
            Effect   = "Allow"
            Resource = var.queue_arn
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
  })
}

### API Gateway
resource "aws_api_gateway_rest_api" "order_api" {
  name = "${var.resource_prefix}-OrderProcessingAPI"
}

resource "aws_api_gateway_resource" "process_resource" {
  rest_api_id = aws_api_gateway_rest_api.order_api.id
  parent_id   = aws_api_gateway_rest_api.order_api.root_resource_id
  path_part   = "process"
}

resource "aws_api_gateway_method" "process_method" {
  rest_api_id   = aws_api_gateway_rest_api.order_api.id
  resource_id   = aws_api_gateway_resource.process_resource.id
  http_method   = "POST"
  authorization = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_integration" "process_integration" {
  rest_api_id             = aws_api_gateway_rest_api.order_api.id
  resource_id             = aws_api_gateway_resource.process_resource.id
  http_method             = aws_api_gateway_method.process_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.order_retrieval.invoke_arn
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.order_retrieval.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.order_api.execution_arn}/*/*"
}

resource "aws_api_gateway_api_key" "order_api_key" {
  name = "${var.resource_prefix}-OrderAPIKey"
  enabled = true
}

resource "aws_api_gateway_stage" "order_api_stage" {
  rest_api_id = aws_api_gateway_rest_api.order_api.id
  deployment_id = aws_api_gateway_deployment.order_api_deployment.id
  stage_name = "${var.resource_prefix}-prod"
}

resource "aws_api_gateway_deployment" "order_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.order_api.id

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_method.process_method,
    aws_api_gateway_integration.process_integration
  ]
}

resource "aws_api_gateway_usage_plan" "order_api_usage_plan" {
  name = "${var.resource_prefix}-OrderUsagePlan"

  api_stages {
    api_id = aws_api_gateway_rest_api.order_api.id
    stage  = aws_api_gateway_stage.order_api_stage.stage_name
  }
}

resource "aws_api_gateway_usage_plan_key" "order_api_key_usage" {
  key_id        = aws_api_gateway_api_key.order_api_key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.order_api_usage_plan.id
}