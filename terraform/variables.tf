# Variables for The Product Mindset - Agentic Application Infrastructure

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "product-mindset"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "github_org" {
  description = "GitHub organization name"
  type        = string
  default     = "stevei101"  # Based on your GitHub profile
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
  default     = "hack-a-product"
}

variable "create_github_oidc_provider" {
  description = "Whether to create the GitHub OIDC provider"
  type        = bool
  default     = true
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Project     = "product-mindset"
    Environment = "dev"
    ManagedBy   = "terraform"
    Owner       = "stevei101"
  }
}