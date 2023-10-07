resource "aws_ssm_parameter" "service_secrets" {
  count = length(var.ecs_service_settings.secrets)
  name  = "/${var.project}/${var.environment}/${local.service_secrets[count.index].name}"
  type  = "SecureString"
  value = local.service_secrets[count.index].value
}

resource "aws_secretsmanager_secret" "gitlab" {
  name = "${var.project}/${var.environment}-gitlab"
  recovery_window_in_days = 0

}

resource "aws_secretsmanager_secret_version" "gitlab" {
  secret_id     = aws_secretsmanager_secret.gitlab.id
  secret_string = jsonencode({
     "username" : "token",
     "password" : var.gitlab_registry_token
})
}