# Forwarder role
output "role_arn" {
  description = "The forwarder lambda role arn"
  value       = try(aws_iam_role.lambda_role.arn, "")
}

output "role_id" {
  description = "The forwarder lambda role id"
  value       = try(aws_iam_role.lambda_role.id, "")
}

output "role_name" {
  description = "The forwarder lambda role name"
  value       = try(aws_iam_role.lambda_role.name, "")
}

# Forwarder Lambda Function
output "lambda_arn" {
  description = "The ARN of the forwarder lambda function"
  value       = try(aws_lambda_function.lambda.arn, "")
}

output "lambda_qualified_arn" {
  description = "The ARN of the forwarder lambda function (if versioning is enabled via publish = true)"
  value       = try(aws_lambda_function.lambda.qualified_arn, "")
}

output "lambda_version" {
  description = "Latest published version of the forwarder lambda function"
  value       = try(aws_lambda_function.lambda.version, "")
}

output "lambda_source_code_hash" {
  description = "Base64-encoded representation of raw SHA-256 sum of the zip file"
  value       = try(aws_lambda_function.lambda.source_code_hash, "")
}
