resource "gitlab_project_variable" "aws_role" {
  project           = data.gitlab_project.service.id
  key               = "ROLE_ARN"
  value             = aws_iam_role.cicd.arn
  environment_scope = var.environment
}

resource "gitlab_project_variable" "aws_region" {
  project           = data.gitlab_project.service.id
  key               = "AWS_DEFAULT_REGION"
  environment_scope = var.environment
  value             = data.aws_region.current.id
}

resource "gitlab_project_variable" "service_ecs_cluster_name" {
  project           = data.gitlab_project.service.id
  key               = "ECS_CLUSTER_NAME"
  value             = local.ecs_cluster_name
  environment_scope = var.environment
}

resource "gitlab_project_variable" "service_ecs_service_name" {
  project           = data.gitlab_project.service.id
  key               = "ECS_SERVICE_NAME"
  value             = module.ecs-service.service_name
  environment_scope = var.environment
}

resource "gitlab_project_variable" "service_container_name" {
  project           = data.gitlab_project.service.id
  key               = "CONTAINER_NAME"
  value             = lower("${var.project}-${var.environment}-${local.ecs_service_name}")
  environment_scope = var.environment
}
