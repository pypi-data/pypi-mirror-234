import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab

# Represents a software Project
class RepositoryTree(AbstractGitLab):

	def __init__(self,personal_access_token, gitlab_url = None):
		super(RepositoryTree,self).__init__(personal_access_token=personal_access_token,gitlab_url=gitlab_url)
	
	def get_by_project_function(self, project_id,**kwargs):
		
		project_repository_tree = []

		try:
			logging.info("Start function: get_project_repository_tree function")
			project = self.gl.projects.get(project_id)
			branchs = project.branches.list(iterator=True,get_all=True)
			function = kwargs["function"]
			for branch in branchs:

				logging.info("Start function: get_project_repository_tree function {} {}:".format(project.name, branch.name) )
				project_repository_tree_return = project.repository_tree(ref=branch.name, get_all=True, iterator=True, recursive=True)
				
				for item in project_repository_tree_return:
					if item["type"] == 'blob':
						file_info =  project.repository_blob(item["id"])
						del file_info["content"]
						del file_info["encoding"]
						item["file_info"] = file_info
					
					item["project"] = project.asdict()
					item["branch"] = branch.asdict()

					function (data=item, topic=kwargs["topic"], extra_data=kwargs["extra_data"])

					project_repository_tree.append(item)				
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve get_project_repository_tree function")
		
		return project_repository_tree
	
	
	def get_by_project(self, project_id):
		
		project_repository_tree = []

		try:
			logging.info("Start function: get_project_repository_tree")
			project = self.gl.projects.get(project_id)

			logging.info("Start function: get_project_repository_tree:"+project.name )
			project_repository_tree_return = project.repository_tree(get_all=True, iterator=True)
			
			for item in project_repository_tree_return:
				if item["type"] == 'blob':
					file_info =  project.repository_blob(item["id"])
					item["file_info"] = file_info
				item["project_id"] = project.id
				project_repository_tree.append(item)				
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve get_project_repository_tree")
		
		return project_repository_tree
	
	def get_all(self, today=False):
		
		projects = []
		project_repository_tree = []

		try:
			logging.info("Start function: get_projects_repository_tree")
			
			projects = self.gl.projects.list(owned=True, iterator=True)

			for project in projects:
				try:
					logging.info("ProjectName:"+project.name)	
					project_repository_tree_return = project.repository_tree(get_all=True, iterator=True)
					
					for item in project_repository_tree_return:
						if item["type"] == 'blob':
							file_info =  project.repository_blob(item["id"])
							item["file_info"] = file_info
						
						item["project_id"] = project.id
						project_repository_tree.append(item)
						
											
				except Exception as e: 
					logging.error("OS error: {0}".format(e))
					logging.error(e.__dict__) 

			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Projects Repository Tree")
		
		return project_repository_tree	