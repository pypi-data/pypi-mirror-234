resource "aws_route53_zone" "default" {
  count = var.route53_zone_id != null ? 0 : 1
  name = var.top_domain
}