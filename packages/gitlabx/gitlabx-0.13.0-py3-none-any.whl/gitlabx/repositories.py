import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab

# Represents a software Project
class Repositories(AbstractGitLab):

	def __init__(self,personal_access_token, gitlab_url = None):
		super(Repositories,self).__init__(personal_access_token=personal_access_token,gitlab_url=gitlab_url)
	
	def get_all(self, today=False): 
		
		result = []
		repository_list = []

		try:
			logging.info("Start function: get_Repositories")
			result = self.gl.projects.list(owned=True, iterator=True)
			for project in result:
				repositories = project.repositories.list(iterator=True)
				project = project.asdict()
				for	repository in repositories:
					repository = repository.asdict()
					repository['project_id'] = project['id']
					repository_list.append(repository)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Repositories")
		
		return repository_list
