module "app" {
  source = "../app"
  providers = {
    aws = aws
  }
  environment = var.environment
  alb_arn_suffix = data.aws_lb.main.arn_suffix
  alb_dns_name = data.aws_lb.main.dns_name
  alb_priority = var.alb_priority
  alb_zone_id = data.aws_lb.main.zone_id
  ecs_cluster_arn = data.aws_ecs_cluster.main.arn
  ecs_cluster_name = data.aws_ecs_cluster.main.cluster_name
  ecs_service_settings = {
    gitlab_repo = var.gitlab_repo
    task_cpu     = 512
    task_memory  = 2048
    min_capacity = 1
    max_capacity = 2
    security_group_ids = ["sg-06f9c86bd2f73b923"]
    domain_pref = var.domain_prefix
    secrets = {}
    env_variables = {}
  }
  http_listener_arn = data.aws_lb_listener.http.arn
  https_listener_arn = data.aws_lb_listener.https.arn
  private_subnet_ids = ["subnet-077f8f5cbd0a1a1c2", "subnet-049f3656d4a49f217"]
  project = var.project
  route53_zone_id = data.aws_route53_zone.tf.zone_id
  vpc_id = "vpc-0e71020d37a848fdb"
  gitlab_registry_token = var.gitlab_registry_token
  tags = var.tags
}
