import os
import shutil
import subprocess

from miquido_infra_spawner.GitlabService import GitlabService

internal_devops_top_domain = "tf.miquido.dev"


class InfraSpawner:
    def __init__(self, service: GitlabService, gitlab_token: str):
        self.service = service
        self.gitlab_token = gitlab_token
        self.parent_group_id = os.getenv('PARENT_GROUP_ID', '76178606')

    def spawn_new_account(self, name, env, domain_prefix, top_domain, gitlab_repo, role_arn, auth_role_arn):
        path = self.spawn(name, env, domain_prefix, f'{domain_prefix}.{top_domain}', gitlab_repo, role_arn, auth_role_arn)
        os.remove(f'{env}/app.tf')
        os.remove(f'{env}/data.tf')
        self.add_top_domain_to_vaiables_tf(top_domain, env)
        self.push_repo(path)
        return path

    def spawn_internal(self, name, env, domain_prefix, alb_priority, gitlab_repo):
        path = self.spawn(name, env, domain_prefix, f'{domain_prefix}.{internal_devops_top_domain}',
                          gitlab_repo, 'arn:aws:iam::230562640235:role/AdministratorAccess', 'arn:aws:iam::230562640235:role/shared-TF')
        os.remove(f'{env}/app-full.tf')
        self.add_alb_priority_to_vaiables_tf(alb_priority, env)
        self.push_repo(path)
        return path

    def spawn(self, name, env, domain_prefix, service_url, gitlab_repo, role_arn, auth_role_arn):
        source_dir = f'{os.path.dirname(__file__)}/template'
        gr_access_token = self.service.create_project_gitlab_registry_access_token(gitlab_repo)
        project_api_access_token = self.service.create_project_api_access_token(gitlab_repo)
        project_id, path = self.service.create_project(name, self.parent_group_id)
        self.service.create_gitlab_token_environment_variable(project_id, project_api_access_token)
        api_access_token = self.service.create_project_api_access_token(project_id)
        self.service.create_backend_state_token_environment_variable(project_id, api_access_token)
        self.service.create_secrets_file(project_id, gr_access_token)
        self.service.create_tf_role_arn_environment_variable(project_id, auth_role_arn)
        destination_dir = name
        shutil.copytree(source_dir, destination_dir)
        os.chdir(destination_dir)
        os.rename('env', env)
        web_url = self.service.get_project_web_url(project_id)
        self.write_values_tf(domain_prefix, env, gitlab_repo, name, web_url)
        self.write_provider_file(env, role_arn)
        self.write_state_file(env, project_id)
        self.write_gitlab_ci(service_url, env, auth_role_arn)
        return path

    def push_repo(self, path):
        subprocess.call(["git", "init"])
        subprocess.call(
            ["git", "remote", "add", "origin", f"https://xd:{self.gitlab_token}@gitlab.com/{path}.git"])
        subprocess.call(["git", "add", "."])
        subprocess.call(["git", "commit", "-m", '"Initial commit"'])
        subprocess.call(["git", "push", "--set-upstream", 'origin', 'main'])

    def write_gitlab_ci(self, service_url, env, role_arn):
        with open('.gitlab-ci.yml', 'r') as file:
            filedata = file.read()
        filedata = filedata.replace('<ENVIRONMENT>', env)
        filedata = filedata.replace('<SERVICE_URL>', f'https://{service_url}')
        filedata = filedata.replace('<ROLE_ARN>', role_arn)

        with open('.gitlab-ci.yml', 'w') as file:
            file.write(filedata)

    def write_state_file(self, env, project_id):
        with open(f'{env}/state.tf', 'r') as file:
            filedata = file.read()
        filedata = filedata.replace('<PROJECT_ID>', str(project_id))
        with open(f'{env}/state.tf', 'w') as file:
            file.write(filedata)

    def write_provider_file(self, env, role_arn):
        with open(f'{env}/provider.tf', 'r') as file:
            filedata = file.read()
        filedata = filedata.replace('<ROLE_ARN>', role_arn)
        with open(f'{env}/provider.tf', 'w') as file:
            file.write(filedata)

    def write_values_tf(self, domain_prefix, env, gitlab_repo, project, web_url):
        values = f'''
            project="{project}"
            domain_prefix="{domain_prefix}"
            gitlab_repo="{gitlab_repo}"
            environment="{env}"
            tags={{
                Terraformed = "true"
                Respo = "{web_url}"
            }}
            '''
        with open(f'{env}/variables.auto.tfvars', 'w') as f:
            f.write(values)

    def add_top_domain_to_vaiables_tf(self, top_domain, env):
        with open(f'{env}/variables.auto.tfvars', 'r') as file:
            filedata = file.read()
        values = f'''
            top_domain="{top_domain}"
            '''
        filedata = filedata + values
        with open(f'{env}/variables.auto.tfvars', 'w') as f:
            f.write(filedata)

    def add_alb_priority_to_vaiables_tf(self, alb_priority, env):
        with open(f'{env}/variables.auto.tfvars', 'r') as file:
            filedata = file.read()
        values = f'''
            alb_priority="{alb_priority}"
            '''
        filedata = filedata + values
        with open(f'{env}/variables.auto.tfvars', 'w') as f:
            f.write(filedata)
