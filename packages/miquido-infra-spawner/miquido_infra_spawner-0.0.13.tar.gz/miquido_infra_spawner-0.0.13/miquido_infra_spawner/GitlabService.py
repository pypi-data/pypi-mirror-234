from datetime import datetime
from dateutil.relativedelta import relativedelta

import requests as requests


class GitlabService:
    def __init__(self, token):
        self.token = token

    def create_project(self, name, namespace_id):
        res = requests.post('https://gitlab.com/api/v4/projects/',
                            headers=self.get_headers(),
                            json={'name': name, 'namespace_id': namespace_id})
        return res.json()['id'], res.json()['path_with_namespace']

    def create_project_gitlab_registry_access_token(self, project_id):
        res = requests.post(f'https://gitlab.com/api/v4/projects/{project_id}/access_tokens',
                            headers=self.get_headers(),
                            json={
                                'name': 'ECS Access',
                                'scopes': ['read_registry'],
                                'expires_at': self.__expires_at()
                            })
        return res.json()['token']

    def create_project_api_access_token(self, project_id):
        res = requests.post(f'https://gitlab.com/api/v4/projects/{project_id}/access_tokens',
                            headers=self.get_headers(),
                            json={
                                'name': 'Terraform',
                                'scopes': ['api'],
                                'expires_at': self.__expires_at()
                            })
        return res.json()['token']

    def create_gitlab_token_environment_variable(self, project_id, gitlab_token):
        requests.post(f'https://gitlab.com/api/v4/projects/{project_id}/variables',
                      headers=self.get_headers(),
                      json={'key': 'GITLAB_TOKEN',
                            'value': gitlab_token,
                            'protected': False,
                            'raw': True})

    def create_backend_state_token_environment_variable(self, project_id, gitlab_token):
        requests.post(f'https://gitlab.com/api/v4/projects/{project_id}/variables',
                      headers=self.get_headers(),
                      json={'key': 'BACKEND_STATE_TOKEN',
                            'value': gitlab_token,
                            'protected': False,
                            'raw': True})

    def create_tf_role_arn_environment_variable(self, project_id, role_arn):
        requests.post(f'https://gitlab.com/api/v4/projects/{project_id}/variables',
                      headers=self.get_headers(),
                      json={'key': 'TF_ROLE_ARN',
                            'value': role_arn,
                            'protected': False,
                            'raw': True})

    def get_project_web_url(self, project_id):
        res = requests.get(f'https://gitlab.com/api/v4/projects/{project_id}',
                           headers=self.get_headers()
                           )
        return res.json()['web_url']

    def delete_project(self, id):
        requests.delete(f'https://gitlab.com/api/v4/projects/{id}',
                        headers=self.get_headers())

    def create_secrets_file(self, project_id, gitlab_registry_token):
        res = requests.post(f'https://gitlab.com/api/v4/projects/{project_id}/variables/',
                            headers=self.get_headers(),
                            json={'key': 'SECRETS',
                                  'value': f'gitlab_registry_token="{gitlab_registry_token}"',
                                  'protected': True,
                                  'variable_type': 'file',
                                  'raw': True})

    def get_headers(self):
        return {
            'PRIVATE-TOKEN': self.token,
            'Content-Type': 'application/json'
        }

    @staticmethod
    def __expires_at():
        d = datetime.now() + relativedelta(years=1) - relativedelta(days=2)
        return d.strftime('%Y-%m-%d')
