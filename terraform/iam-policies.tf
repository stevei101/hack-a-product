# terraform/iam-policies.tf

# --- GitHub Actions OIDC Role ---

# Data source for current AWS account
data "aws_caller_identity" "current" {}

# Trust policy document that allows GitHub Actions to assume the role
data "aws_iam_policy_document" "github_actions_trust_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_org}/${var.github_repo}:ref:refs/heads/develop"]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
  }
}

# The IAM role that GitHub Actions will assume
resource "aws_iam_role" "github_actions_role" {
  name               = "GitHubAction-AssumeRoleWithAction"
  assume_role_policy = data.aws_iam_policy_document.github_actions_trust_policy.json
  description        = "IAM role for GitHub Actions to deploy the frontend"
}

# Permissions policy document for the GitHub Actions role
data "aws_iam_policy_document" "github_actions_permissions_policy" {
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:DeleteObject"
    ]
    resources = [
      aws_s3_bucket.site.arn,
      "${aws_s3_bucket.site.arn}/*"
    ]
  }

  statement {
    effect    = "Allow"
    actions   = ["cloudfront:CreateInvalidation"]
    resources = [aws_cloudfront_distribution.s3_distribution.arn]
  }

  statement {
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "ecr:PutImage"
    ]
    resources = ["*"] # ECR actions are not resource-specific in the same way as S3
  }
}

# The IAM policy that grants the permissions
resource "aws_iam_policy" "github_actions_policy" {
  name        = "GitHubActions-FrontendDeploy-Policy"
  description = "Permissions for the GitHub Actions role to deploy the frontend"
  policy      = data.aws_iam_policy_document.github_actions_permissions_policy.json
}

# Attaching the policy to the role
resource "aws_iam_role_policy_attachment" "github_actions_attach" {
  role       = aws_iam_role.github_actions_role.name
  policy_arn = aws_iam_policy.github_actions_policy.arn
}
