locals {
  vpc_id = var.vpc_id != null ? var.vpc_id : module.vpc[0].vpc_id
  http_listener_arn = var.http_listener_arn == null ? module.alb[0].http_listener_arn : var.http_listener_arn
  https_listener_arn = var.https_listener_arn == null ? module.alb[0].https_listener_arn : var.https_listener_arn
  top_domain = var.route53_zone_id != null ? data.aws_route53_zone.main[0].name : var.top_domain
  private_subnet_ids = var.vpc_id != null ? var.private_subnet_ids : module.vpc[0].private_subnet_ids
  route53_zone_id = var.route53_zone_id != null ? var.route53_zone_id : aws_route53_zone.default[0].zone_id
  alb_arn_suffix = var.alb_arn_suffix != null ? var.alb_arn_suffix : module.alb[0].alb_arn_suffix
  alb_dns_name = var.alb_dns_name != null ? var.alb_dns_name : module.alb[0].alb_dns_name
  alb_zone_id = var.alb_zone_id != null ? var.alb_zone_id : module.alb[0].alb_zone_id
  security_group_ids = var.vpc_id != null ? var.ecs_service_settings.security_group_ids : [aws_security_group.main.id]
  ecs_cluster_arn = var.ecs_cluster_arn != null ? var.ecs_cluster_arn : aws_ecs_cluster.main[0].arn
  ecs_cluster_name = var.ecs_cluster_name != null ? var.ecs_cluster_name : aws_ecs_cluster.main[0].name
}