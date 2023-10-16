import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab


# Represents a software Project
class PipelinesSchedules(AbstractGitLab):

	def __init__(self,personal_access_token, gitlab_url = None):
		super(PipelinesSchedules,self).__init__(personal_access_token=personal_access_token,gitlab_url=gitlab_url)
	
	def get_by_project_function(self, project_id,**kwargs):
		
		function = kwargs["function"]

		commit_list = []

		try:
			logging.info("Start function: get_Pipelines Schedules")
			project = self.gl.projects.get(project_id)
			logging.info("Start function: getPipelines Schedules:"+project.name )
			pipelines = project.pipelineschedules.list(iterator=True,all=True)
			project = project.asdict()
			for	pipeline in pipelines:
				pipeline = pipeline.asdict()
				pipeline['project'] = project
				function (data=pipeline, topic=kwargs["topic"], extra_data=kwargs["extra_data"])
				commit_list.append(pipeline)
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Pipelines Schedules")
		
		return commit_list

	
	
	def get_all(self, today=False): 
		
		result = []
		commit_list = []

		try:
			logging.info("Start function: get_Pipelines Schedules")
			result = self.gl.projects.list(owned=True, iterator=True)

			for project in result:
				logging.info("Start function: getPipelines Schedules:"+project.name )
				pipelines = project.pipelineschedules.list(iterator=True,all=True)
				project = project.asdict()
				for	pipeline in pipelines:
					pipeline = pipeline.asdict()
					pipeline['project'] = project
					
					
					commit_list.append(pipeline)
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Pipelines Schedules")
		
		return commit_list
