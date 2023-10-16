import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab

# Represents a software Project
class Events(AbstractGitLab):

	def __init__(self,personal_access_token, gitlab_url = None):
		super(Events,self).__init__(personal_access_token=personal_access_token,gitlab_url=gitlab_url)
	
	
	def get_by_project_function(self, project_id,**kwargs):
		
		event_list = []
		function = kwargs["function"]

		try:
			logging.info("Start function: get_Events")
			
			events = project.events.list(iterator=True)
			project = project.asdict()
			for	event in events:
				event = event.asdict()
				event["project"] = project
				function (data=event, topic=kwargs["topic"], extra_data=kwargs["extra_data"])
				
				event_list.append(event)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Events")
		
		return event_list

	
	
	def get_all(self, today=False): 
		
		result = []
		event_list = []

		try:
			logging.info("Start function: get_Events")
			result = self.gl.projects.list(owned=True, iterator=True)
			for project in result:
				events = project.events.list(iterator=True)
				project = project.asdict()
				for	event in events:
					event = event.asdict()
					event["project"] = project
					event_list.append(event)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Events")
		
		return event_list
