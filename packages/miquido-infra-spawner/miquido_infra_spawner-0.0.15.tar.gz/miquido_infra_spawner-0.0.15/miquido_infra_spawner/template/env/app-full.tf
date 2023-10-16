module "app" {
  source = "../app"
  providers = {
    aws = aws
  }
  environment = var.environment
  ecs_service_settings = {
    gitlab_repo = var.gitlab_repo
    task_cpu     = 512
    task_memory  = 2048
    min_capacity = 1
    max_capacity = 2
    domain_pref = var.domain_prefix
    secrets = {}
    env_variables = {}
  }
  project = var.project
  gitlab_registry_token = var.gitlab_registry_token

  top_domain = var.top_domain
}
