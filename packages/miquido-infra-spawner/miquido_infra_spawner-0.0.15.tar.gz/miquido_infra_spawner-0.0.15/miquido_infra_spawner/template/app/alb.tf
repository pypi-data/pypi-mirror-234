module "alb" {
  count                               = var.top_domain != null ? 1 : 0
  source                              = "git::https://github.com/miquido/terraform-alb.git?ref=tags/3.1.18"
  name                                = ""
  domain                              = var.top_domain
  project                             = var.project
  environment                         = var.environment
  tags                                = var.tags
  vpc_id                              = local.vpc_id
  subnet_ids                          = module.vpc[0].public_subnet_ids
  security_group_ids                  = [aws_security_group.main.id]
  enable_redirect_http_to_https       = true
  https_ssl_policy                    = "ELBSecurityPolicy-FS-1-2-2019-08"
  access_logs_s3_bucket_force_destroy = true
  access_logs_enabled                 = true
  acm_certificate_arn                 = module.acm_alb.arn
  idle_timeout                        = 600
}

resource "aws_security_group" "main" {
  name        = "main ${var.project}-${var.environment}"
  description = "Main sg for ${var.project}-${var.environment}"
  vpc_id      = local.vpc_id
  tags        = var.tags
}

resource "aws_security_group_rule" "inbound" {
  type                     = "ingress"
  from_port                = 0
  to_port                  = 65535
  protocol                 = "tcp"
  security_group_id        = aws_security_group.main.id
  source_security_group_id = aws_security_group.main.id
}

resource "aws_security_group_rule" "outbound" {
  type              = "egress"
  to_port           = 65535
  protocol          = "-1"
  from_port         = 0
  security_group_id = aws_security_group.main.id
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = ["::/0"]
}
