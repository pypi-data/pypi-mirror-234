import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab


# Represents a software Project
class Job(AbstractGitLab):

	def __init__(self,personal_access_token, gitlab_url = None):
		super(Job,self).__init__(personal_access_token=personal_access_token,gitlab_url=gitlab_url)
	
	def get_by_project_function(self, project_id,**kwargs):
		
		
		function = kwargs["function"]

		commit_list = []

		try:
			logging.info("Start function: Job")
			
			project = self.gl.projects.get(project_id)
			logging.info("Start function: Job:"+project.name )
			jobs = project.jobs.list(iterator=True,all=True)
			project = project.asdict()
			for	job in jobs:
				job = job.asdict()
				job['project'] = project					
				function (data=job, topic=kwargs["topic"], extra_data=kwargs["extra_data"])
			
				commit_list.append(job)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All  job")
		
		return commit_list


	
	
	def get_all(self, today=False): 
		
		result = []
		commit_list = []

		try:
			logging.info("Start function: Job")
			result = self.gl.projects.list(owned=True, iterator=True)

			for project in result:
				logging.info("Start function: Job:"+project.name )
				jobs = project.jobs.list(iterator=True,all=True)
				project = project.asdict()
				for	job in jobs:
					job = job.asdict()
					job['project'] = project					

					commit_list.append(job)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All  job")
		
		return commit_list
