import os,sys
from configobj import ConfigObj # Need to install this package locally: https://pypi.python.org/pypi/configobj/

def server_credentials_people(self, servername):
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

		#people1 - scenario
		self.peopleInfo = {"stdPass":credentialsConfig.get("stdPass")}


		self.peopleEmailFilteredWallInfo = {"peopleUser":credentialsConfig.get("peopleUser")}
		self.peopleFuzzySearch_AlotsInfo = {"peopleUser":credentialsConfig.get("peopleUser")}
		self.peopleFuzzySearch_BaumlerInfo = {"peopleUser":credentialsConfig.get("peopleUser")}
		# self.peopleFuzzySearch_lporte_ispyInfo = {"tomik":credentialsConfig.get("tomik")}
		self.peopleFuzzySearch_VerInfo = {"peopleUser":credentialsConfig.get("peopleUser")}
		self.peopleOnlineNowCustomBadgeInfo = {"peopleUser":credentialsConfig.get("peopleUser")}
		self.peopleSharefileDeepSearchInfo = {"peopleUser":credentialsConfig.get("peopleUser")}
		self.peopleStartOpenDiscussionInfo = {"peopleUser":credentialsConfig.get("peopleUser")}
		self.peopleStartPrivateDiscussionInfo = {"peopleUser":credentialsConfig.get("peopleUser")}
		self.peopleUTF_LoginsSearchInfo = {"peopleUser":credentialsConfig.get("peopleUser")}
		return self

if __name__ == "__main__":
	unittest.main()