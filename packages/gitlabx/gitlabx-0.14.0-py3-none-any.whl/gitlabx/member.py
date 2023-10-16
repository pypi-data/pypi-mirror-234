import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab

# Represents a software Project
class Member(AbstractGitLab):

	def __init__(self,personal_access_token, gitlab_url = None):
		super(Member,self).__init__(personal_access_token=personal_access_token,gitlab_url=gitlab_url)

	def get_by_project_function(self, project_id,**kwargs):
		

		try:
			member_list = []
			
			logging.info("Start function: get_members")
			project = self.gl.projects.get(project_id)
			
			function = kwargs["function"]

			logging.info("Start function: get_members:"+project.name )
			members = project.members_all.list(iterator=True,all=True)
			project = project.asdict()
			for	member in members:
				member = member.asdict()
				member['project'] = project
				user =  self.gl.users.get(member['id'])
				member['user'] = user.asdict()
				
				function (data=member, topic=kwargs["topic"], extra_data=kwargs["extra_data"])
				
				member_list.append (member)			
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project``s get_members")
		
		return member_list
	
	def get_by_project(self, project_id):
		
		member_list = []

		try:
			logging.info("Start function: get_members")
			project = self.gl.projects.get(project_id)

			logging.info("Start function: get_members:"+project.name )
			members = project.members_all.list(iterator=True,all=True)
			project = project.asdict()
			for	member in members:
				member = member.asdict()
				member['project'] = project
				user =  self.gl.users.get(member['id'])
				member['user'] = user.asdict()
				member_list.append(member)			
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project``s get_members")
		
		return member_list
	
	def get_all(self, today=False): 
		
		result = []
		member_list = []

		try:
			logging.info("Start function: get_members")
			result = self.gl.projects.list(owned=True, iterator=True)

			for project in result:
				members = project.members_all.list(iterator=True,all=True)
				project = project.asdict()
				for	member in members:
					
					member = member.asdict()
					member['project'] = project
					user =  self.gl.users.get(member['id'])
					member['user'] = user.asdict()
					member_list.append(member)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Members")
		
		return member_list

