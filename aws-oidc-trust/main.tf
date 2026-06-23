terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Establish Google Cloud as a trusted Identity Provider in AWS
resource "aws_iam_openid_connect_provider" "gke_oidc" {
  url             = "https://container.googleapis.com/v1/projects/alert-hall-466720-c0/locations/us-central1/clusters/dev-sagc-cluster"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["08745487e891c19e3078c1f2a07e452950ef36f6"]
}

# Generate the strictly scoped trust policy document
data "aws_iam_policy_document" "gke_trust_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.gke_oidc.arn]
    }

    # Fail-closed boundary: Only this specific namespace and ServiceAccount
    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.gke_oidc.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:agentic:litellm-wif-sa"]
    }

    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.gke_oidc.url, "https://", "")}:aud"
      values   = ["sts.amazonaws.com"]
    }
  }
}

# Manage the existing Bedrock role to inject the new trust policy
resource "aws_iam_role" "dev_litellm_bedrock_role" {
  name               = "dev-litellm-bedrock-role"
  assume_role_policy = data.aws_iam_policy_document.gke_trust_policy.json
}

resource "aws_iam_role_policy" "bedrock_invoke_policy" {
  name = "bedrock-invoke-policy"
  role = aws_iam_role.dev_litellm_bedrock_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:bedrock:us-east-1:229502947368:inference-profile/*",
          "arn:aws:bedrock:us-east-1::foundation-model/*"
        ]
      }
    ]
  })
}
