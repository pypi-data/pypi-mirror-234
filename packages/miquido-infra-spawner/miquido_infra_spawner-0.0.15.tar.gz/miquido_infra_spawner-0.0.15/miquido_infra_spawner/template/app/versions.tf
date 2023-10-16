# Note: always specify only minimum required versions to not limit modules compatibility too strictly

terraform {
  required_version = ">= 0.13"

  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = ">= 2.29.0"
    }
    gitlab = {
      source  = "gitlabhq/gitlab"
      version = ">= 3.5.0"
    }
  }

}
