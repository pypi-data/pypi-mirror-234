module "acm_alb" {
  source = "git::https://github.com/miquido/terraform-acm-request-certificate.git?ref=tags/3.0.7"

  providers = {
    aws.acm = aws
    aws.dns = aws
  }

  domain_name               = local.ecs_service_domain
  ttl                       = "300"
  subject_alternative_names = []
  hosted_zone_id            = local.route53_zone_id

  wait_for_certificate_issued = true
  tags                        = var.tags
}

resource "aws_lb_listener_certificate" "default" {
  count           = var.https_listener_arn != null ? 1 : 0
  listener_arn    = var.https_listener_arn
  certificate_arn = module.acm_alb.arn
}