#function to get the build number from the Jostle platform
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.]
from get_datetime import get_datetime   #date\time funtion that we use for file names
from path_est import path_est   
from writer import writer               #function to handle outputs
import time,os

def check_TEAMS_exit_edit_mode_Button(driver = None,intervalWaitForPage = None,output = None):
	"""
	   this is a function that is used to verify if the Exit edit mode button is displayed in TEAMS.
	   @param driver: instance of selenium webdriver being used by class that called this function.
	   @param intervalWaitForPage: interval that webdriver will wait for page to load before abort, set to 1 min if empty.
	   @param output: variable for the log buffer used by the test.
	   ++ All arguments needed, but it is possible to set intervalWaitForPage, to None.
	"""
	global verify, log_path
	pageLoadWaitInterval = intervalWaitForPage if intervalWaitForPage != None else 5
	if (driver == None or output == None):
		print "ERROR in check_TEAMS_exit_edit_mode_Button(): Please send webdriver, and output as arguments."
	else:
		driver.set_page_load_timeout(pageLoadWaitInterval)
		try:
			verify = 0
			#Admin Gear test
			try:
				editButton = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID,"QA:CentricView:exitEditButton")))
				if editButton.is_displayed() == False:
					output = writer("VERIFY:\texitEditButton Absent\tFAIL",output)
				elif editButton.is_displayed() == True:
					output = writer("VERIFY:\texitEditButton Present\tPASS",output)
					verify = 1
			except TimeoutException:
				output = writer("INFO:\tCatastrophic DOM Error",output)
			#-------------------------
		except TimeoutException:
			output = writer("INFO:\tgo to Admin iframe failed",output)	
	return verify

def check_cannot_edit_team_alert(driver = None,intervalWaitForPage = None,output = None):
	"""
	   this is a function that is used to check if the Cannot edit team aleart is displayed.
	   @param driver: instance of selenium webdriver being used by class that called this function.
	   @param intervalWaitForPage: interval that webdriver will wait for page to load before abort, set to 1 min if empty.
	   @param output: variable for the log buffer used by the test.
	   ++ All arguments needed, but it is possible to set intervalWaitForPage to None.
	"""
	global verify, log_path
	#pageLoadWaitInterval = intervalWaitForPage if intervalWaitForPage != None else 5
	#driver.set_page_load_timeout(pageLoadWaitInterval)
	verify=0
	if (driver == None or output == None):
		print "ERROR in check_TEAMS_exit_edit_mode_Button(): Please send webdriver, and output as arguments."
	else:
		try:
			WebDriverWait(driver, intervalWaitForPage).until(EC.alert_is_present())
			cannotEditTeamAlert = driver.switch_to_alert().dismiss()
			output = writer("VERIFY:\tDismissed the alert.\tPASS",output)
			verify = 1
		except (TimeoutException, NoAlertPresentException):
			output = writer("VERIFY:\tDid NOT find and dismiss Alert: You do not have permissions for this team.\tFAIL", output)
			#-------------------------
	return verify


if __name__ == "__main__":
	testdriver = webdriver.Firefox()
	prog = "check_TEAMS_exit_edit_mode_Button"
	global output
	output = []                                 #empty list to append Test Outputs
	output = writer("-"*50,output)
	output = writer(prog,output)  
	check_TEAMS_exit_edit_mode_Button(testdriver,60,output)
	testdriver.close()