# Guance forwarder for AWS Lambda

This module creates a Lambda function that forwards logs to Guance Cloud.

## Usage

### Clone this repository

The first step is cloning this repository:

```bash
git clone https://github.com/GuanceCloud/terraform-guance-forwarder.git
cd terraform-guance-forwarder/examples/aws
```

### Configure the variables

Create the variables file `test.tfvars` with the following content:

```hcl
cloudwatch_log_group_arn   = "arn:aws:logs:..."
cloudwatch_events_rule_arn = "arn:aws:events:..."
guance_endpoint            = "https://datakit-hostname:9529"
```

### Apply the example

Run the following commands to apply the real resource in this example:

```bash
terraform init
terraform apply -var-file=./test.tfvars
```

## Feedback

If you have any questions or suggestions, feel free to open an issue within this repository.

## License

This project is licensed under the Apache-2.0 License.
