data "aws_iam_openid_connect_provider" "gitlab" {
  url = "https://gitlab.com"
}

resource "aws_iam_role" "cicd" {
  name               = "${var.project}-${var.environment}-CICD"
  description        = "Role used for Gitlab"
  assume_role_policy = data.aws_iam_policy_document.gitlab.json
}

data "aws_iam_policy_document" "gitlab" {
  version = "2012-10-17"

  statement {
    sid     = "AllowAssumeRole"
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [data.aws_iam_openid_connect_provider.gitlab.arn]
    }

    condition {
      test     = "StringLike"
      variable = "gitlab.com:sub"
      values   = ["project_path:${data.gitlab_project.service.path_with_namespace}:ref_type:branch:ref:main"]
    }
  }
}