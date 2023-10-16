import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab
import json

# Represents a software Project
class ProjectLanguages(AbstractGitLab):

	def __init__(self,personal_access_token, gitlab_url = None):
		super(ProjectLanguages,self).__init__(personal_access_token=personal_access_token,gitlab_url=gitlab_url)
	
	def get_all(self, today=False): 
		
		result = []
		languages = []

		try:
			logging.info("Start function: get_projectsLanguages")
			result = self.gl.projects.list(owned=True, iterator=True, simple=True)
			for project in result:
				json_string = json.dumps(project.languages(), indent= 4)
				json_obj = json.loads(json_string)
				json_obj['projeto_id'] = project.get_id()
				languages.append(json_obj)				

		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Projects Languages")
		
		return languages	

