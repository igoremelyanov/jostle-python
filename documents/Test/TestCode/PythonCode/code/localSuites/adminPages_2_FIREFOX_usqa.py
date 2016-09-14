## python AdminPages2 testsuite
# this testsuite operates on the assumption that there already exists contributor data

import unittest
from adminCreateNewsAdmins_usqa import adminCreateNewsAdmins as test001
from adminCreateTeamsAdmins_usqa import adminCreateTeamsAdmins as test002
from adminCreateSystemAdmins_usqa import adminCreateSystemAdmins as test003
from adminExtractShouts_usqa import adminExtractShouts as test004
from adminExtractTEAMstructureToVisio_usqa import adminExtractTEAMstructureToVisio as test005
from adminExtractOverallLogins_usqa import adminExtractOverallLogins as test006
from adminExtractContributorsNotLoggedIn_usqa import adminExtractContributorsNotLoggedIn as test007
from adminExtractContributorsInvitedButNeverLoggedIn_usqa import adminExtractContributorsInvitedButNeverLoggedIn as test008
from adminVerifyAccountUsageStatistics_usqa import adminVerifyAccountUsageStatistics as test009
from adminLoginSamlUser_usqa import adminLoginSamlUser as test010
from adminLoginGoogleUser_usqa import adminLoginGoogleUser as test011
	
if __name__ == "__main__":
	unittest.main()
	