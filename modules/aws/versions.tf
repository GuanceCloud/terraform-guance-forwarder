terraform {
  required_version = ">= 1.0"

  required_providers {
    guance = {
      source = "GuanceCloud/guance"
    }
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.9"
    }
  }
}