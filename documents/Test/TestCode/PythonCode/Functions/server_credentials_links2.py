import os,sys
from configobj import ConfigObj # Need to install this package locally: https://pypi.python.org/pypi/configobj/

def server_credentials_links2(self, servername):
	# @servername: name of the server (e.g. usqa, caqa)

	configFilePath = os.path.abspath(os.path.join(__file__, "../config_files/"+servername+"_links2.properties"))
	configFilePathForum = os.path.abspath(os.path.join(__file__, "../config_files/zendesk_forum_url.properties"))
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

		#Links2 - scenario 
		self.linksInfo = {"GroupEmailDisabledUser":credentialsConfig.get("GroupEmailDisabledUser"),
								   "GroupEmailDisabledSandboxUser":credentialsConfig.get("GroupEmailDisabledSandboxUser"),
								   "adminUser":credentialsConfig.get("adminUser"),
								   "links2url001Admin":credentialsConfig.get("links2url001Admin"),
								   "links2url001GroupEmailDisabled":credentialsConfig.get("links2url001GroupEmailDisabled"),
								   "links2url002Admin":credentialsConfig.get("links2url002Admin"),
								   "links2url002GroupSandboxDisabled":credentialsConfig.get("links2url002GroupSandboxDisabled"),
								   "stdPass":credentialsConfig.get("stdPass")}

		self.AddYourselfInfo = {"AddYourselfOnUser":credentialsConfig.get("AddYourselfOnUser"),
								   "AddYourselfOffUser":credentialsConfig.get("AddYourselfOffUser"),
								   "links2url_addYourselfAndRemove_ON":credentialsConfig.get("links2url_addYourselfAndRemove_ON"),
								   "links2url_addYourselfAndRemove_OFF":credentialsConfig.get("links2url_addYourselfAndRemove_OFF")}

		self.linksExternalCannotAddWG = {"externalCannotCreateWorkingGroupUser":credentialsConfig.get("externalCannotCreateWorkingGroupUser"),
								   "internalCanCreateWorkingGroupUser":credentialsConfig.get("internalCanCreateWorkingGroupUser"),
								   "links2url_externalCannotCreateWorkingGroup":credentialsConfig.get("links2url_externalCannotCreateWorkingGroup")}

		self.linksExternalEditDownHier = {"externalEditAdminUser":credentialsConfig.get("externalEditAdminUser"),
								   "externalEditTeamsUser":credentialsConfig.get("externalEditTeamsUser"),
								   "externalMainOrgTeamURL":credentialsConfig.get("externalMainOrgTeamURL"),
								   "externalMainOrgDownHierTeamURL":credentialsConfig.get("externalMainOrgDownHierTeamURL"),
								   "externalMainOrgAboveHierTeamURL":credentialsConfig.get("externalMainOrgAboveHierTeamURL"),
								   "externalWGTeamURL":credentialsConfig.get("externalWGTeamURL"),
								   "externalWGDownHierTeamURL":credentialsConfig.get("externalWGDownHierTeamURL"),
								   "externalWGAboveHierTeamURL":credentialsConfig.get("externalWGAboveHierTeamURL"),
								   "externalCCTeamURL":credentialsConfig.get("externalCCTeamURL"),
								   "externalCCDownHierTeamURL":credentialsConfig.get("externalCCDownHierTeamURL"),
								   "externalCCAboveHierTeamURL":credentialsConfig.get("externalCCAboveHierTeamURL")
		}

		self.linksResetPassword = {"resetPasswordURL":credentialsConfig.get("resetPasswordURL"),
								   "interimPassword":credentialsConfig.get("interimPassword")
								   }
		self.linksHideMainOrg = {"hideMainOrgAdminTeamURL":credentialsConfig.get("hideMainOrgAdminTeamURL"),
								   "hideMainOrgNONAdminTeamURL":credentialsConfig.get("hideMainOrgNONAdminTeamURL"),
								   "hideMainOrgAdminUSER":credentialsConfig.get("hideMainOrgAdminUSER"),
								   "hideMainOrgNONAdminUSER":credentialsConfig.get("hideMainOrgNONAdminUSER")
								   }
		self.linksStartGoogleHangout = {"startGoogleHangoutONTEAMSProfileURL":credentialsConfig.get("startGoogleHangoutONTEAMSProfileURL"),
								   "startGoogleHangoutONTEAMSURL":credentialsConfig.get("startGoogleHangoutONTEAMSURL"),
								   "startGoogleHangoutONPEOPLEURL":credentialsConfig.get("startGoogleHangoutONPEOPLEURL"),
								   "startGoogleHangoutOFFTEAMSProfileURL":credentialsConfig.get("startGoogleHangoutOFFTEAMSProfileURL"),
								   "startGoogleHangoutOFFTEAMSURL":credentialsConfig.get("startGoogleHangoutOFFTEAMSURL"),
								   "startGoogleHangoutOFFPEOPLEURL":credentialsConfig.get("startGoogleHangoutOFFPEOPLEURL"),
								   "startGoogleHangoutONUSER":credentialsConfig.get("startGoogleHangoutONUSER"),
								   "startGoogleHangoutOFFUSER":credentialsConfig.get("startGoogleHangoutOFFUSER")
								   }

		self.linksSharedArticleLink = {"sharedArticleLinkURL":credentialsConfig.get("sharedArticleLinkURL"),
								   "sharedArticleLinkSharedUSER":credentialsConfig.get("sharedArticleLinkSharedUSER"),
								   "sharedArticleLinkNOTSharedUSER":credentialsConfig.get("sharedArticleLinkNOTSharedUSER")
								   }

		self.linksForumLinks = {"forumNews02LinksURL":credentialsConfig.get("forumNews02LinksURL"),
								"forumNews05LinksURL":credentialsConfig.get("forumNews05LinksURL"),
								"forumNews06LinksURL":credentialsConfig.get("forumNews06LinksURL"),
								"forumLibraryLinksURL":credentialsConfig.get("forumLibraryLinksURL"),
								"forumVisitForumLinksURL":credentialsConfig.get("forumVisitForumLinksURL"),
								"forumMoreLinksURL":credentialsConfig.get("forumMoreLinksURL"),
								"forumAdminAccountInfoForumLinksURL":credentialsConfig.get("forumAdminAccountInfoForumLinksURL"),
								   "forumLinkUser":credentialsConfig.get("forumLinkUser")
		}
		return self


if __name__ == "__main__":
	unittest.main()