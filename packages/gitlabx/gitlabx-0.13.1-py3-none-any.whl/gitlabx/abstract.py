import gitlab
from abc import ABC

class AbstractGitLab(ABC):

    def __init__(self, personal_access_token, gitlab_url = None):
        self.gitlab_url = gitlab_url if gitlab_url!= None else 'https://gitlab.com/'
        self.personal_access_token = personal_access_token
        self.gl = gitlab.Gitlab(url=self.gitlab_url, private_token = personal_access_token)

    