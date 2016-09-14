import os,sys
from configobj import ConfigObj

def server_credentials(self,servername,testPath):
	# @servername: name of the server (e.g. usqa, caqa)
	# @testPath: test location (used to determine the config file location)

	# Check if resources folder exist
	if not os.path.exists(testPath):
		print "Error: Request path does not exist"
		sys.exit(-1)
	else:
		configFilePath = os.path.abspath(os.path.join(testPath, "../../../resources/test."+servername+".properties"))
		# print configFilePath
		#Check if config file exists
		if not os.path.isfile(configFilePath):
			print "Error: Requested configuration file does not exist:\t"+configFilePath
			sys.exit(-1)
		else:
			# print configFilePath
			credentialsConfig =  ConfigObj(configFilePath)
			self.baseUrl = credentialsConfig.get("baseUrl")
			self.initializer = credentialsConfig.get("initializer")
			self.remover = credentialsConfig.get("remover")
			self.verifier = credentialsConfig.get("verifier")
			self.teamMember = credentialsConfig.get("teamMember")
			self.maliciousUser = credentialsConfig.get("maliciousUser")
			self.notTeamMember = credentialsConfig.get("notTeamMember")
			self.notTeamMemberName = credentialsConfig.get("notTeamMemberName")
			self.privateTeam = credentialsConfig.get("privateTeam")
			self.privateTeam = credentialsConfig.get("privateTeam")
			self.individual = credentialsConfig.get("individual")
			self.poster = credentialsConfig.get("poster")
			self.password = credentialsConfig.get("password")
			return self

	# return buildPath_CA

if __name__ == "__main__":
	server_credentials("usqa","/Users/kimar/Jostle/svn/documents/Test/TestCode/PythonCode/prototype/test/src/test/python/newsPages/newsCreateNEWSArticleORGUnit.py")