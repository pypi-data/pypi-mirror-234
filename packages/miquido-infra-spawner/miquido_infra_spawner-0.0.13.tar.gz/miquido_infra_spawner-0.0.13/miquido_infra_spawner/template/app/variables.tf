variable "tags" {
  type        = map(string)
  description = "Default tags to apply on all created resources"
  default     = {}
}

variable "environment" {
  type        = string
  description = "Environment name"
}

variable "project" {
  type        = string
  description = "Account/Project Name"
}

variable "route53_zone_id" {
  type = string
  description = "data.aws_route53_zone.id"
  default = null
}

variable "ecs_service_settings" {
  type = object({
    gitlab_repo  = string
    task_cpu     = number
    task_memory  = number
    min_capacity = number
    max_capacity = number
    domain_pref = string
    security_group_ids = optional(list(string))
    env_variables = map(string)
    secrets = map(string)
  })
  description = "Task settings image tag, cpu, memory, autoscaling minimum capacity and maximum capacity"
}

variable "vpc_id" {
  type = string
  default = null
}

variable http_listener_arn {
  type = string
  default = null
}

variable https_listener_arn {
  type = string
  default = null
}

variable alb_arn_suffix {
  type = string
  default = null
}

variable alb_dns_name {
  type = string
  default = null
}

variable alb_zone_id {
  type = string
  default = null
}

variable ecs_cluster_arn {
  type = string
  default = null
}

variable ecs_cluster_name {
  type = string
  default = null
}

variable private_subnet_ids {
  type = list(string)
  default = null
}

variable alb_priority {
  type = string
  description = "Rule priority in ALB"
  default = 90
}

variable "gitlab_registry_token" {
  type = string
}

variable "top_domain" {
  type = string
  default = null
}