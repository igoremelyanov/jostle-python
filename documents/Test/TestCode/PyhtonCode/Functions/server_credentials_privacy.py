import os,sys
from configobj import ConfigObj # Need to install this package locally: https://pypi.python.org/pypi/configobj/

def server_credentials_privacy(self, servername):
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
		self.serverInfo = {"initializer":credentialsConfig.get("initializer"),"baseUrl":credentialsConfig.get("baseUrl"),"loginUrl":credentialsConfig.get("loginUrl"),"initializerPass":credentialsConfig.get("initializerPass")}

		#privacy_patch - scenario
		self.peopleInfo = {"stdPass":credentialsConfig.get("stdPass")}


		self.privacyLibraryVolume_patchInfo = {"privacyLibrarian":credentialsConfig.get("privacyLibrarian"),
		"privacyLocationandDepartment":credentialsConfig.get("privacyLocationandDepartment"),"privacyNeither":credentialsConfig.get("privacyNeither"),
		"privacyLocation":credentialsConfig.get("privacyLocation")}

		self.privacyMainViews_patchInfo = {"privacySysAdmin":credentialsConfig.get("privacySysAdmin"),
		"privacyNewsandTeamAdmin":credentialsConfig.get("privacyNewsandTeamAdmin"),"privacyNeither":credentialsConfig.get("privacyNeither"),
		"privacyRegUser":credentialsConfig.get("privacyRegUser")}
	
		return self

if __name__ == "__main__":
	unittest.main()