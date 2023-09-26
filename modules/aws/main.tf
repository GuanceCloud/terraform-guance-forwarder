data "aws_region" "current" {}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "${path.module}/index.py"
  output_path = "lambda.zip"
}

resource "aws_lambda_function" "lambda" {
  function_name = var.function_name
  role          = aws_iam_role.lambda_role.arn
  tags          = var.tags
  layers        = var.layers
  publish       = var.publish

  # Source code
  filename         = "lambda.zip"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  handler          = "index.lambda_handler"

  # Runtime
  runtime     = "python3.10"
  memory_size = var.memory_size
  timeout     = var.timeout

  environment {
    variables = merge(
      {
        GUANCE_ENDPOINT        = var.guance_endpoint
      },
      var.environment_variables,
    )
  }

  # Dependencies
  depends_on = [aws_iam_role_policy_attachment.lambda_logs]
}

# IAM configuration
resource "aws_iam_role" "lambda_role" {
  name = "${var.function_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

data "aws_iam_policy_document" "lambda_logging" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.lambda_logging.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

# EventBridge 
resource "aws_lambda_permission" "lambda" {
  count = var.cloudwatch_events_enabled ? 1 : 0

  statement_id  = "guance-cloudwatch-events"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = var.cloudwatch_events_rule_arn
}

# CloudWatch Logs
resource "aws_lambda_permission" "cloudwatch" {
  count = var.cloudwatch_logs_enabled ? 1 : 0

  statement_id  = "guance-cloudwatch-logs"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "logs.${data.aws_region.current.name}.amazonaws.com"
  source_arn    = var.cloudwatch_logs_log_group_arn
}
