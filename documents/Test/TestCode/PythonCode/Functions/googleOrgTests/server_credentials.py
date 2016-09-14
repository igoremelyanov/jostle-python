import os,sys
from configobj import ConfigObj

def server_credentials(self, servername):
	# @servername: name of the server (e.g. usqa, caqa)

	configFilePath = os.path.abspath(os.path.join(__file__, "../config_files/"+servername+".properties"))
	# print configFilePath
	#Check if config file exists
	if not os.path.isfile(configFilePath):
		print "Error: Requested configuration file does not exist:\t"+configFilePath
		sys.exit(-1)
	else:
		#Load properties file for reading
		credentialsConfig =  ConfigObj(configFilePath)

		#Server credentials
		self.serverInfo = {"initializer":credentialsConfig.get("initializer"),
		"baseUrl":credentialsConfig.get("baseUrl"),
		"loginUrl":credentialsConfig.get("loginUrl"),
		"initializerPass":credentialsConfig.get("initializerPass")}

		#Google Credentials
		self.googleInfo = {"googleMailUrl":credentialsConfig.get("googleMailUrl"),
		"user":credentialsConfig.get("googleUsername"),
		"password":credentialsConfig.get("googleUserPass")}

		return self


if __name__ == "__main__":
	
	class A:
		# Init.
		def __init__(self, value):
			self.__value = value

	server_credentials(A,"usqa")
	print A.serverInfo
	print A.googleInfo