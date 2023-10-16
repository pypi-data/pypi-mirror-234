import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab

# Represents a software Project
class Deployments(AbstractGitLab):

	def __init__(self,personal_access_token, gitlab_url = None):
		super(Deployments,self).__init__(personal_access_token=personal_access_token,gitlab_url=gitlab_url)
	
	def get_by_project_function(self, project_id,**kwargs):
		
		deployment_list = []
		function = kwargs["function"]

		try:
			logging.info("Start function: get_projectDeployments")
			project = self.gl.projects.get(project_id)
			deployments = project.deployments.list(iterator=True)
			project = project.asdict()
			for	deployment in deployments:
				deployment = deployment.asdict()
				deployment['project'] = project

				function (data=deployment, topic=kwargs["topic"], extra_data=kwargs["extra_data"])
				
				deployment_list.append(deployment)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Deployments")
		
		return deployment_list

	
	def get_all(self, today=False): 
		
		result = []
		deployment_list = []

		try:
			logging.info("Start function: get_projectDeployments")
			result = self.gl.projects.list(owned=True, iterator=True)
			for project in result:
				deployments = project.deployments.list(iterator=True)
				project = project.asdict()
				for	deployment in deployments:
					deployment = deployment.asdict()
					deployment['project'] = project
					deployment_list.append(deployment)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Deployments")
		
		return deployment_list
