### Install
`pip install miquido-infra-spawner`

### Internal example:
`python -m miquido_infra_spawner internal --name internal --env test --domain_prefix hello --alb_priority 130 --gitlab_project_id 50710355`

### External example:
`python -m miquido_infra_spawner external --name external --env ready --domain_prefix hello --gitlab_project_id 50710355 --top_domain whatever.miquido.dev --role_arn arn:aws:iam::246402711611:role/AdministratorAccess --auth_role_arn arn:aws:iam::246402711611:role/Test-TF`
