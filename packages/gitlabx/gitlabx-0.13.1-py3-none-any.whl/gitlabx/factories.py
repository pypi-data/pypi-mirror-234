import factory
from .project import Project
from .repositoryTree import RepositoryTree
from .branches import Branches
from .commits import Commits
from .deployments import Deployments
from .events import Events
from .issues import Issues
from .repositories import Repositories
from .projectLanguages import ProjectLanguages
from .member import Member
from .merge_request import MergeRequest
from .pipelines import Pipelines
from .pipelines_schedules import PipelinesSchedules
from .jobs import Job

class JobFactory(factory.Factory):
    
    class Meta:
        model = Job
        
    personal_access_token = None
    gitlab_url = None

class PipelinesSchedulesFactory(factory.Factory):
    
    class Meta:
        model = PipelinesSchedules
        
    personal_access_token = None
    gitlab_url = None

class PipelineFactory(factory.Factory):
    
    class Meta:
        model = Pipelines
        
    personal_access_token = None
    gitlab_url = None


class MergeRequestFactory(factory.Factory):
    
    class Meta:
        model = MergeRequest
        
    personal_access_token = None
    gitlab_url = None


class ProjectFactory(factory.Factory):
    
    class Meta:
        model = Project
        
    personal_access_token = None
    gitlab_url = None

class MembersFactory(factory.Factory):
    
    class Meta:
        model = Member
        
    personal_access_token = None
    gitlab_url = None
  
class RepositoryTreeFactory(factory.Factory):
    
    class Meta:
        model = RepositoryTree
        
    personal_access_token = None
    gitlab_url = None

class BranchesFactory(factory.Factory):
    
    class Meta:
        model = Branches
        
    personal_access_token = None
    gitlab_url = None
    
class CommitsFactory(factory.Factory):
    
    class Meta:
        model = Commits
        
    personal_access_token = None
    gitlab_url = None
class DeploymentsFactory(factory.Factory):
    
    class Meta:
        model = Deployments
        
    personal_access_token = None
    gitlab_url = None

class EventsFactory(factory.Factory):
    
    class Meta:
        model = Events
        
    personal_access_token = None
    gitlab_url = None

class IssuesFactory(factory.Factory):
    
    class Meta:
        model = Issues
        
    personal_access_token = None
    gitlab_url = None

class RepositoriesFactory(factory.Factory):
    
    class Meta:
        model = Repositories
        
    personal_access_token = None
    gitlab_url = None


class ProjectLanguagesFactory(factory.Factory):
    
    class Meta:
        model = ProjectLanguages
        
    personal_access_token = None
    gitlab_url = None
