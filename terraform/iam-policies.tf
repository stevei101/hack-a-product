# IAM Policies for The Product Mindset - Agentic Application
# Based on patterns from aws-ec2-terraform-github-actions

# Data source for current AWS account
data "aws_caller_identity" "current" {}

# Data source for current AWS region
data "aws_region" "current" {}

# OIDC Provider for GitHub Actions (if not already exists)
resource "aws_iam_openid_connect_provider" "github" {
  count = var.create_github_oidc_provider ? 1 : 0
  
  url = "https://token.actions.githubusercontent.com"
  
  client_id_list = [
    "sts.amazonaws.com",
  ]
  
  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1",
    "1c58a3a8518e8759bf075b76b750d4f2df264fcd"
  ]
  
  tags = {
    Name        = "github-oidc-provider"
    Environment = var.environment
    Project     = "product-mindset"
  }
}

# IAM Policy for Terraform Cloud User
resource "aws_iam_policy" "terraform_cloud_policy" {
  name        = "${var.project_name}-terraform-cloud-${var.environment}"
  description = "Policy for Terraform Cloud to manage infrastructure for ${var.project_name}"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          # S3 permissions for static website hosting
          "s3:CreateBucket",
          "s3:PutBucketWebsite",
          "s3:PutBucketPolicy",
          "s3:GetBucketPolicy",
          "s3:DeleteBucketPolicy",
          "s3:DeleteBucket",
          "s3:GetBucketLocation",
          "s3:ListBucket",
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject"
        ]
        Resource = [
          "arn:aws:s3:::${var.project_name}-*",
          "arn:aws:s3:::${var.project_name}-*/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          # CloudFront permissions
          "cloudfront:CreateDistribution",
          "cloudfront:UpdateDistribution",
          "cloudfront:GetDistribution",
          "cloudfront:DeleteDistribution",
          "cloudfront:CreateOriginAccessControl",
          "cloudfront:DeleteOriginAccessControl",
          "cloudfront:GetOriginAccessControl",
          "cloudfront:UpdateOriginAccessControl",
          "cloudfront:ListDistributions",
          "cloudfront:GetDistributionConfig"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          # IAM permissions for creating the GitHub Actions role
          "iam:CreateRole",
          "iam:DeleteRole",
          "iam:GetRole",
          "iam:AttachRolePolicy",
          "iam:DetachRolePolicy",
          "iam:PutRolePolicy",
          "iam:DeleteRolePolicy",
          "iam:PassRole"
        ]
        Resource = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.project_name}-github-actions-${var.environment}"
      }
    ]
  })
  
  tags = {
    Name        = "${var.project_name}-terraform-cloud-policy"
    Environment = var.environment
    Project     = var.project_name
  }
}

# IAM Role for GitHub Actions with OIDC
resource "aws_iam_role" "github_actions_role" {
  name = "${var.project_name}-github-actions-${var.environment}"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github[0].arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_organization}/${var.github_repository}:ref:refs/heads/${var.environment == "prod" ? "main" : var.environment}"
          }
        }
      }
    ]
  })
  
  tags = {
    Name        = "${var.project_name}-github-actions-role"
    Environment = var.environment
    Project     = var.project_name
  }
}

# IAM Policy for GitHub Actions
resource "aws_iam_policy" "github_actions_policy" {
  name        = "${var.project_name}-github-actions-${var.environment}"
  description = "Policy for GitHub Actions to deploy ${var.project_name}"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          # S3 permissions for deployment
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:DeleteObject",
          "s3:PutObjectAcl"
        ]
        Resource = [
          "arn:aws:s3:::${var.bucket_name}",
          "arn:aws:s3:::${var.bucket_name}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          # CloudFront permissions for cache invalidation
          "cloudfront:CreateInvalidation",
          "cloudfront:GetInvalidation",
          "cloudfront:ListInvalidations"
        ]
        Resource = "arn:aws:cloudfront::${data.aws_caller_identity.current.account_id}:distribution/${aws_cloudfront_distribution.s3_distribution.id}"
      }
    ]
  })
  
  tags = {
    Name        = "${var.project_name}-github-actions-policy"
    Environment = var.environment
    Project     = var.project_name
  }
}

# Attach policy to GitHub Actions role
resource "aws_iam_role_policy_attachment" "github_actions_policy_attachment" {
  role       = aws_iam_role.github_actions_role.name
  policy_arn = aws_iam_policy.github_actions_policy.arn
}