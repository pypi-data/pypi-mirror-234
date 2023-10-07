data "aws_ecs_cluster" "main" {
  cluster_name = "devops-shared-main"
}

data "aws_lb" "main" {
  name = "devops-shared"
}

data "aws_lb_listener" "https" {
  load_balancer_arn = data.aws_lb.main.arn
  port              = 443
}

data "aws_lb_listener" "http" {
  load_balancer_arn = data.aws_lb.main.arn
  port              = 80
}

data "aws_route53_zone" "tf" {
  name         = "tf.miquido.dev."
}