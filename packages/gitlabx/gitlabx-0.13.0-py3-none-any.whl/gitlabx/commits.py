import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab


# Represents a software Project
class Commits(AbstractGitLab):

	def __init__(self,personal_access_token, gitlab_url = None):
		super(Commits,self).__init__(personal_access_token=personal_access_token,gitlab_url=gitlab_url)
	
	def get_by_id(self, project_id, short_id):
		commit = None
		try:
			logging.info("Start function: get details about one commit")
			project = self.gl.projects.get(project_id)
			commit = project.commits.get(short_id)
			return commit.asdict()
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve get details about one commit")
	
	
	def get_by_project_files_function(self, project_id, **kwargs):
		
		try:
			function = kwargs["function"]

			logging.info("Start function: get_commit_files_project")
			project = self.gl.projects.get(project_id)

			logging.info("Start function: get_commit_files_project {}".format(project.name))
			commits = project.commits.list(get_all=True,iterator=True)

			# Itere sobre os commits
			for commit in commits:
				file_details = []
				commit_details = {}
				commit_details['id'] = commit.id
				commit_details['project'] = project.asdict()
				commit_details['files'] = file_details 
				commit_details['refs'] = commit.refs() 
				# Add author e email
				commit_details['author_name'] = commit.author_name
				commit_details['author_email'] = commit.author_email
				
				diff = project.commits.get(commit.id).diff(get_all=True,iterator=True)
				for change in diff:
					file_path = change["new_path"]
					old_path = change.get("old_path")
					data = None
					if file_path not in file_details:
						data = {
							"file_path": file_path,
							"date": commit.created_at,
							"action": "created",		
						}

					elif old_path == file_path:
						data["action"] = "modified"
					file_details.append(data)

				function (data=commit_details, topic=kwargs["topic"], extra_data=kwargs["extra_data"])
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project`s Files in a commit")
	 

	def get_by_project_files(self, project_id):
		
		try:
			logging.info("Start function: get_commit_files_project")
			project = self.gl.projects.get(project_id)
			
			logging.info("Start function: get_commit_files_project {}".format(project.name))
			commits = project.commits.list(get_all=True,iterator=True)
			
			# Dicionário para armazenar os detalhes de cada arquivo
			commits_details = []

			# Itere sobre os commits
			for commit in commits:
				file_details = []
				commit_details = {}
				commit_details['id'] = commit.id
				commit_details['project'] = project_id
				commit_details['files'] = file_details 
				commit_details['refs'] = commit.refs() 
				# Add author e email
				commit_details['author_name'] = commit.author_name
				commit_details['author_email'] = commit.author_email
				
				diff = project.commits.get(commit.id).diff(get_all=True,iterator=True)
				for change in diff:
					file_path = change["new_path"]
					old_path = change.get("old_path")
					data = None
					if file_path not in file_details:
						data = {
							"file_path": file_path,
							"date": commit.created_at,
							"action": "created",		
						}

					elif old_path == file_path:
						data["action"] = "modified"
					file_details.append(data)

				commits_details.append (commit_details)
			return commits_details
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project`s Files in a commit")
	
	def get_by_project_function(self, project_id, details = False, diff = False,**kwargs):
		
		commit_list = []

		try:

			function = kwargs["function"]

			logging.info("Start function: get_commit_projeto")
			project = self.gl.projects.get(project_id)

			logging.info("Start function: get_Commits:"+project.name )

			branchs = project.branches.list(iterator=True,get_all=True)

			for branch in branchs:

				commits = project.commits.list(iterator=True,get_all=True)
				project = project.asdict()
				branch = branch.asdict()
				
				for	commit in commits:
					commitX = commit.asdict()
					commitX['project'] = project
					commitX['branch'] = branch 
					
					
					#commitX['merge_requests'] = commit.merge_requests()
					#commitX['comments'] = self.__list(commit.comments.list(iterator=True,get_all=True))
					#commitX['statuses '] = self.__list(commit.statuses.list(iterator=True,get_all=True))
					diffs = []
					for diff_x in commit.diff(iterator=True,get_all=True): 
						file_path = diff_x['new_path']
						change_type = "changed"
						if diff_x['new_file']:
							change_type = "created"
						elif diff_x['deleted_file']:
							change_type = "deleted"

						diff_x["file_path"] = file_path
						diff_x["status"] = change_type

						diffs.append(diff_x)
					
					commitX['diff'] = diffs

					function (data=commitX, topic=kwargs["topic"], extra_data=kwargs["extra_data"])
					
					commit_list.append(commitX)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project`s Commits")
		
		return commit_list
	def get_by_project(self, project_id, details = False, diff = False):
		
		commit_list = []

		try:
			logging.info("Start function: get_commit_projeto")
			project = self.gl.projects.get(project_id)

			logging.info("Start function: get_Commits:"+project.name )
			commits = project.commits.list(iterator=True,get_all=True)
			project = project.asdict()
			for	commit in commits:
				commitX = commit.asdict()
				commitX['project_id'] = project['id']
				commitX['refs'] = commit.refs() 
				
				if (details):
					commitX['merge_requests'] = commit.merge_requests()
					commitX['comments'] = self.__list(commit.comments.list(iterator=True,get_all=True))
					commitX['statuses '] = self.__list(commit.statuses.list(iterator=True,get_all=True))
					if (diff):
						diffs = []
						for diff_x in commit.diff(iterator=True,get_all=True): diffs.append(diff_x)
						commitX['diff'] = diffs


				commit_list.append(commitX)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project`s Commits")
		
		return commit_list
	
	def __list (self, elements):
		elements_list = []
		for element in elements:
			elements_list.append(element.asdict())
		return elements_list


	def get_all(self, today=False): 
		
		result = []
		commit_list = []

		try:
			logging.info("Start function: get_Commits")
			result = self.gl.projects.list(owned=True, iterator=True,get_all=True)

			for project in result:
				logging.info("Start function: get_Commits:"+project.name )
				commits = project.commits.list(iterator=True,get_all=True)
				project = project.asdict()
				for	commit in commits:
					commitX = commit.asdict()
					commitX['project_id'] = project['id']
					#commitX['merge_requests'] = commit.merge_requests()
					#commitX['refs'] = commit.refs() 
					#commitX['comments'] = commit.comments.list()
					#commitX['statuses '] = commit.statuses.list()
					
					commit_list.append(commitX)
					break
				break
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Commits")
		
		return commit_list
