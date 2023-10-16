provider "aws" {
  region = "eu-central-1"
  assume_role {
    role_arn = "<ROLE_ARN>"
  }
}
