# Main Terraform configuration for The Product Mindset (v0.12 compatible)
terraform {
  required_version = ">= 0.12"
  
  required_providers {
    aws = "~> 3.0"
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
}
