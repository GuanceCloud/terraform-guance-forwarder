provider "aws" {
  region = "us-east-1"

  # Make it faster by skipping something
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_credentials_validation = true
  skip_requesting_account_id  = true
}

module "lambda_example" {
  source = "../../modules/aws"

  # Required
  function_name   = "guance-example"
  guance_endpoint = var.guance_endpoint

  # Optional
  timeout               = 10
  memory_size           = 128
  tags                  = {}
  environment_variables = var.environment_variables

  # EventBridge
  cloudwatch_events_enabled  = var.cloudwatch_events_rule_arn != ""
  cloudwatch_events_rule_arn = var.cloudwatch_events_rule_arn

  # CloudWatchLogs
  cloudwatch_logs_enabled       = var.cloudwatch_log_group_arn != ""
  cloudwatch_logs_log_group_arn = var.cloudwatch_log_group_arn
}

variable "cloudwatch_events_rule_arn" { type = string }
variable "cloudwatch_log_group_arn" { type = string }
variable "guance_endpoint" { type = string }
variable "environment_variables" {
  type    = map(string)
  default = {}
}
