module "vpc" {
  count = var.vpc_id == null ? 1 : 0
  source = "git::https://github.com/miquido/terraform-vpc.git?ref=10.0.0"
  name                            = "main"
  project                         = var.project
  environment                     = var.environment
  tags                            = var.tags
  azs                             = ["${data.aws_region.current.id}a", "${data.aws_region.current.id}b"]
  nat_type                        = "gateway-single"
  enable_ecs_fargate_private_link = false
  subnet_type_tag_key             = "${var.project}/subnet/type"
  cidr                            = "10.0.0.0/16"
}
