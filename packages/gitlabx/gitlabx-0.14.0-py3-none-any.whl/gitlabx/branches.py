import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab

# Represents a software Project
class Branches(AbstractGitLab):

	def __init__(self,personal_access_token, gitlab_url = None):
		super(Branches,self).__init__(personal_access_token=personal_access_token,gitlab_url=gitlab_url)

	def create (self, project_id, name, ref="main"):
		try:
			logging.info("Start function: create branch")
			project = self.gl.projects.get(project_id)
			return project.branches.create({'branch': name, 'ref': ref})
		
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project``s Commits")
	

	def get_by_project_function(self, project_id,**kwargs):
		
		branch_list = []
		
		try:
			logging.info("Start function: get_commit_projeto")
			project = self.gl.projects.get(project_id)
			
			function = kwargs["function"]

			logging.info("Start function: get_Commits:"+project.name )
			branchs = project.branches.list(iterator=True,get_all=True)
			project = project.asdict()
			for	branch in branchs:
				branch = branch.asdict()
				branch['project'] = project

				function (data=branch, topic=kwargs["topic"], extra_data=kwargs["extra_data"])

				branch_list.append(branch)			
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project``s Commits")
		
		return branch_list
	
	
	def get_by_project(self, project_id):
		
		branch_list = []

		try:
			logging.info("Start function: get_commit_projeto")
			project = self.gl.projects.get(project_id)

			logging.info("Start function: get_Commits:"+project.name )
			branchs = project.branches.list(iterator=True,get_all=True)
			project = project.asdict()
			for	branch in branchs:
				branch = branch.asdict()
				branch['project'] = project['id']
				branch_list.append(branch)			
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project``s Commits")
		
		return branch_list
	
	
	def get_all(self, today=False): 
		
		result = []
		branch_list = []

		try:
			logging.info("Start function: get_Branches")
			result = self.gl.projects.list(owned=True, iterator=True)
			for project in result:
				branches = project.branches.list()
				project = project.asdict()
				for	branch in branches:
					branch = branch.asdict()
					branch['project'] = project['id']
					branch_list.append(branch)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Branches")
		
		return branch_list
