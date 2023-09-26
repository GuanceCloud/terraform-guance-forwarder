# Aws Lambda Guance Forwarder

This module creates a Lambda function that forwards logs to Guance Cloud.

## Usage

See [example files](../../examples/aws/README.md) for example usage.

<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | n/a |
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_iam_policy.lambda_logging](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.lambda_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.lambda_logs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_function.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_permission.cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [aws_lambda_permission.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [archive_file.lambda](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [aws_iam_policy_document.lambda_logging](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_cloudwatch_events_enabled"></a> [cloudwatch\_events\_enabled](#input\_cloudwatch\_events\_enabled) | Enable CloudWatch events | `bool` | `false` | no |
| <a name="input_cloudwatch_events_rule_arn"></a> [cloudwatch\_events\_rule\_arn](#input\_cloudwatch\_events\_rule\_arn) | CloudWatch event rule arn | `string` | `""` | no |
| <a name="input_cloudwatch_logs_enabled"></a> [cloudwatch\_logs\_enabled](#input\_cloudwatch\_logs\_enabled) | Enable CloudWatch logs | `bool` | `false` | no |
| <a name="input_cloudwatch_logs_log_group_arn"></a> [cloudwatch\_logs\_log\_group\_arn](#input\_cloudwatch\_logs\_log\_group\_arn) | CloudWatch log group arn | `string` | `""` | no |
| <a name="input_environment_variables"></a> [environment\_variables](#input\_environment\_variables) | A map of environment variables for the lambda function | `map(string)` | `{}` | no |
| <a name="input_function_name"></a> [function\_name](#input\_function\_name) | The name for the Lambda function | `string` | n/a | yes |
| <a name="input_guance_endpoint"></a> [guance\_endpoint](#input\_guance\_endpoint) | Guance endpoint for upload data, such as datakit: 127.0.0.1:9529 | `string` | n/a | yes |
| <a name="input_guance_workspace_token"></a> [guance\_workspace\_token](#input\_guance\_workspace\_token) | The token must be set when guance\_endpoint is not a datakit endpoint | `string` | n/a | yes |
| <a name="input_layers"></a> [layers](#input\_layers) | List of Lambda Layer Version ARNs (maximum of 5) to attach to the forwarder lambda | `list(string)` | `[]` | no |
| <a name="input_memory_size"></a> [memory\_size](#input\_memory\_size) | The amount of memory in MB allocated to the Lambda function | `number` | `128` | no |
| <a name="input_publish"></a> [publish](#input\_publish) | Whether to publish creation/change as a new Lambda Function Version | `bool` | `false` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | A mapping of tags to assign to the lambda function | `map(string)` | `{}` | no |
| <a name="input_timeout"></a> [timeout](#input\_timeout) | The amount of time in seconds that Lambda allows a function to run before stopping it | `number` | `10` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->
