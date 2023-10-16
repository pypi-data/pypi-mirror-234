import os
import argparse

import requests

from miquido_infra_spawner.GitlabService import GitlabService
from miquido_infra_spawner.InfraSpawner import InfraSpawner

if __name__ == '__main__':
    token = os.getenv('GITLAB_TOKEN')
    s = GitlabService(token)
    spawner = InfraSpawner(s, token)

    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=['internal', 'external'])
    parser.add_argument('--name', '-n', action='store', required=True)
    parser.add_argument('--environment', '-e', action='store', required=True)
    parser.add_argument('--domain_prefix', '-d', action='store', required=True)
    parser.add_argument('--gitlab_project_id', '-g', action='store', required=True)

    parser.add_argument('--alb_priority', '-ap', action='store', required=False)
    parser.add_argument('--role_arn', '-r', action='store', required=False)
    parser.add_argument('--auth_role_arn', '-ar', action='store', required=False)
    parser.add_argument('--top_domain', '-td', action='store', required=False)

    args = parser.parse_args()

    if args.type.lower() == "internal":
        if args.alb_priority is None:
            alb_priority = requests.get('https://dbvyfiv43rwoha6nv34hjix5ce0hpxuk.lambda-url.eu-central-1.on.aws').json()['priority']
        else:
            alb_priority = args.alb_priority

        path = spawner.spawn_internal(
            name=args.name,
            env=args.environment,
            domain_prefix=args.domain_prefix,
            alb_priority=alb_priority,
            gitlab_repo=args.gitlab_project_id)
    else:
        assert args.top_domain is not None, "missing top_domain"
        assert args.role_arn is not None, "missing role_arn"
        assert args.auth_role_arn is not None, "missing auth_role_arn"
        path = spawner.spawn_new_account(
            name=args.name,
            env=args.environment,
            domain_prefix=args.domain_prefix,
            gitlab_repo=args.gitlab_project_id,
            top_domain=args.top_domain,
            role_arn=args.role_arn,
            auth_role_arn=args.auth_role_arn
        )

    print(f"Your Terraform repo: https://gitlab.com/{path}. Enjoy!")
