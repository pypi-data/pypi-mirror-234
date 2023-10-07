variable "tags" {
  type        = map(string)
  description = "Default tags to apply on all created resources"
}

variable "gitlab_registry_token" {
  type = string
}

variable "project" {
  type = string
}

variable "domain_prefix" {
  type = string
}

variable "alb_priority" {
  type = number
  default = null
}

variable "gitlab_repo" {
  type = string
}

variable "environment" {
  type = string
}

variable "top_domain" {
  type = string
  default = null
}