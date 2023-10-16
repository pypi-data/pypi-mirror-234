data aws_region current {}
data "aws_route53_zone" "main" {
  count = var.route53_zone_id != null ? 1 : 0
  zone_id = var.route53_zone_id
}

locals {
  ecs_service_name              = "service"
  ecs_service_domain            = "${var.ecs_service_settings.domain_pref}.${local.top_domain}"
  ecs_service_port              = 80
  ecs_service_health_check_path = "/"
  ecs_service_image_repository  = "registry.gitlab.com/${data.gitlab_project.service.path_with_namespace}"
  ecs_service_image_tag         = "latest"

  service_envs = [
    for key, value in var.ecs_service_settings.env_variables :
    {
      name  = key
      value = value
    }
  ]

  service_secrets = [
    for key, value in var.ecs_service_settings.secrets :
    {
      name  = key
      value = value
    }
  ]

  service_secrets_ssm = [
    for i, secret in aws_ssm_parameter.service_secrets :
    {
      name      = local.service_secrets[i].name
      valueFrom = secret.arn
    }
  ]

}

module "alb-service-ingress" {
  source                                     = "git::https://github.com/miquido/terraform-alb-ingress.git?ref=tags/3.1.9"
  name                                       = local.ecs_service_name
  project                                    = var.project
  environment                                = var.environment
  tags                                       = var.tags
  vpc_id                                     = local.vpc_id
  listener_arns                              = [local.http_listener_arn, local.https_listener_arn]
  hosts                                      = [local.ecs_service_domain]
  port                                       = local.ecs_service_port
  health_check_path                          = local.ecs_service_health_check_path
  health_check_healthy_threshold             = 2
  health_check_interval                      = 40
  health_check_unhealthy_threshold           = 5
  alb_target_group_alarms_enabled            = true
  alb_target_group_alarms_treat_missing_data = "notBreaching"
  alb_arn_suffix                             = local.alb_arn_suffix
  priority                                   = var.alb_priority
}

resource "aws_route53_record" "service" {
  zone_id = local.route53_zone_id
  name    = local.ecs_service_domain
  type    = "A"

  alias {
    name                   = local.alb_dns_name
    zone_id                = local.alb_zone_id
    evaluate_target_health = true
  }
}

module "ecs-service" {
  source = "git::https://github.com/miquido/terraform-ecs-alb-task.git?ref=tags/5.6.38"

  name                                      = local.ecs_service_name
  project                                   = var.project
  environment                               = var.environment
  tags                                      = var.tags
  container_image                           = local.ecs_service_image_repository
  container_tag                             = local.ecs_service_image_tag
  container_port                            = local.ecs_service_port
  health_check_grace_period_seconds         = 20
  task_cpu                                  = var.ecs_service_settings.task_cpu
  task_memory                               = var.ecs_service_settings.task_memory
  desired_count                             = var.ecs_service_settings.min_capacity
  autoscaling_min_capacity                  = var.ecs_service_settings.min_capacity
  autoscaling_max_capacity                  = var.ecs_service_settings.max_capacity
  ecs_alarms_cpu_utilization_high_threshold = 50
  autoscaling_scale_up_adjustment           = 2
  autoscaling_enabled                       = true
  ecs_alarms_enabled                        = true
  assign_public_ip                          = false
  readonly_root_filesystem                  = false
  logs_region                               = data.aws_region.current.id
  vpc_id                                    = local.vpc_id
  alb_target_group_arn                      = module.alb-service-ingress.target_group_arn
  ecs_cluster_arn                           = local.ecs_cluster_arn
  security_group_ids                        = local.security_group_ids
  subnet_ids                                = local.private_subnet_ids
  ecs_cluster_name                          = local.ecs_cluster_name
  platform_version                          = "1.4.0"
  exec_enabled                              = true
  ignore_changes_desired_count              = true
  volumes_from                              = []
  container_cpu                             = 0
  envoy_health_check_start_period           = 20
  secret_manager_enabled                    = true
  repository_credentials                    = {
    credentialsParameter = aws_secretsmanager_secret_version.gitlab.arn
  }

  healthcheck = {
    command = [
      "CMD-SHELL", "curl -s http://localhost:${local.ecs_service_port}${local.ecs_service_health_check_path}"
    ]
    interval    = 60
    retries     = 5
    startPeriod = 20
    timeout     = 4
  }

  app_mesh_enable = false

  capacity_provider_strategies = [
    {
      capacity_provider = "FARGATE_SPOT"
      weight            = 1
      base              = null
    }
  ]

  secrets = concat([], local.service_secrets_ssm)

  envs = concat([], local.service_envs)

  depends_on = [module.alb.alb_arn]
}




