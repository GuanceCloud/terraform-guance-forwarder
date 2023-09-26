variable "function_name" {
  description = "The name for the Lambda function"
  type        = string
}

variable "guance_endpoint" {
  type        = string
  description = "Guance endpoint for upload data, such as: datakit-hostname:9529"
}

variable "timeout" {
  description = "The amount of time in seconds that Lambda allows a function to run before stopping it"
  type        = number
  default     = 10
}

variable "memory_size" {
  description = "The amount of memory in MB allocated to the Lambda function"
  type        = number
  default     = 128
}

variable "tags" {
  description = "A mapping of tags to assign to the lambda function"
  type        = map(string)
  default     = {}
}

variable "layers" {
  description = "List of Lambda Layer Version ARNs (maximum of 5) to attach to the forwarder lambda"
  type        = list(string)
  default     = []
}

variable "environment_variables" {
  description = "A map of environment variables for the lambda function"
  type        = map(string)
  default     = {}
}

variable "publish" {
  description = "Whether to publish creation/change as a new Lambda Function Version"
  type        = bool
  default     = false
}

variable "cloudwatch_events_enabled" {
  type        = bool
  description = "Enable CloudWatch events"
  default     = false
}

variable "cloudwatch_events_rule_arn" {
  type        = string
  description = "CloudWatch event rule arn"
  default     = ""
}

variable "cloudwatch_logs_enabled" {
  type        = bool
  description = "Enable CloudWatch logs"
  default     = false
}

variable "cloudwatch_logs_log_group_arn" {
  type        = string
  description = "CloudWatch log group arn"
  default     = ""
}
