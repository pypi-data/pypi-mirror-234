import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab


# Represents a software Project
class MergeRequest(AbstractGitLab):

	def __init__(self,personal_access_token, gitlab_url = None):
		super(MergeRequest,self).__init__(personal_access_token=personal_access_token,gitlab_url=gitlab_url)
	
	def get_by_project_function(self, project_id,**kwargs):
		
		
		function = kwargs["function"]

		commit_list = []

		try:
			logging.info("Start function: get_merge_request")
			project = self.gl.projects.get(project_id)
			logging.info("Start function: get_merge_request:"+ project.name)
			mergerequests = project.mergerequests.list(iterator=True,state='all')
			project = project.asdict()
			for	mergerequest in mergerequests:
				mergerequestX = mergerequest.asdict()
				mergerequestX['project'] = project
				mergerequestX['commits'] = mergerequest.commits()
				mergerequestX['changes'] = mergerequest.changes()
				function (data=mergerequestX, topic=kwargs["topic"], extra_data=kwargs["extra_data"])
				commit_list.append(mergerequestX)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project get_merge_request")
		
		return commit_list

	
	def get_all(self, today=False): 
		
		result = []
		commit_list = []

		try:
			logging.info("Start function: get_merge_request")
			result = self.gl.projects.list(owned=True, iterator=True)

			for project in result:
				logging.info("Start function: get_merge_request:"+ project.name)
				mergerequests = project.mergerequests.list(iterator=True,state='all')
				project = project.asdict()
				for	mergerequest in mergerequests:
					mergerequestX = mergerequest.asdict()
					mergerequestX['project'] = project
					mergerequestX['commits'] = mergerequest.commits()
					mergerequestX['changes'] = mergerequest.changes()

					commit_list.append(mergerequestX)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project get_merge_request")
		
		return commit_list
