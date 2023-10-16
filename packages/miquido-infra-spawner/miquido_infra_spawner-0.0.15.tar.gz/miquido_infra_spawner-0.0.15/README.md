# About

This project is meant to automate creation of new terraform repositories. Running the script will create a git repo in `miquido/dynamic-aws-envs` gitlab group and start the pipeline deploying new environment 

## Requirements
`GITLAB_TOKEN` environment variable set with api scope and sufficient permisions for creating repo in `miquido/dynamic-aws-envs` group and adding acess tokens to the project you want to deploy 

### Install
This script is distributed as a python package via PyPi:
https://pypi.org/project/miquido-infra-spawner/

To install:
`pip install miquido-infra-spawner`

### Internal example:
running internal will deploy infrastructure in existing VPC with ALB on internal-devops account:  
```python -m miquido_infra_spawner internal --name internal --env test --domain_prefix hello --gitlab_project_id 50710355```

- --name: name of the infrastructure repository
- --env: name of the environment
- --domain_prefix: service will be available under `<domain_prefix>.tf.miquido.dev`
- --gitlab_project_id: gitlab project that you want to deploy in ECS

### External example:
running external will deploy infrastructure in any given account additionally provisioning VPC and ALB:  

`python -m miquido_infra_spawner external --name external --env ready --domain_prefix hello --gitlab_project_id 50710355 --top_domain whatever.miquido.dev --role_arn arn:aws:iam::246402711611:role/AdministratorAccess --auth_role_arn arn:aws:iam::246402711611:role/Test-TF`

- --name: name of the infrastructure repository
- --env: name of the environment
- --domain_prefix: service will be available under `<domain_prefix>.<top_domain>`
- --top_domain: service will be available under `<domain_prefix>.<top_domain>`
- --role_arn: Role used to access Admininstaror privileges on desired AWS account
- --auth_role_arn: Role used by gitlab to be able to assume <role_arn>
- --gitlab_project_id: gitlab project that you want to deploy in ECS

