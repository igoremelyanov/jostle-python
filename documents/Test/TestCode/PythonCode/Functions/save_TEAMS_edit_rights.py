#function to get the build number from the Jostle platform
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.]
from get_datetime import get_datetime   #date\time funtion that we use for file names
from path_est import path_est   
from writer import writer               #function to handle outputs
import time,os

def save_TEAMS_edit_rights(driver = None,intervalWaitForPage = None,output = None):
	"""
	   this is a function that is used to go to the Admin Edit/Delete contributor page.
	   @param driver: instance of selenium webdriver being used by class that called this function.
	   @param contributor: instance for name/email to find the contributor
	   @param intervalWaitForPage: interval that webdriver will wait for page to load before abort, set to 1 min if empty.
	   @param output: variable for the log buffer used by the test.
	   ++ All arguments needed, but it is possible to set intervalWaitForPage, password, screenshotPath, now, and screenshotPos to None.
	"""
	global start, log_path
	start = time.time()
	pageLoadWaitInterval = intervalWaitForPage if intervalWaitForPage != None else 5
	if (driver == None or output == None):
		print "ERROR in save_TEAMS_edit_rights(): Please send webdriver, and output as arguments."
	else:
		#Click the Save Button
		try:
			saveSettings = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.NAME,"saveSettings")))
			saveSettings.click()
			output = writer("INFO:\tClicked Save Button",output)
			stamp = True
		except TimeoutException:
			output = writer("VERIFY:\tsaveSettings\tFAIL",output)
   			stamp = False
     	#-----------------------------
		if stamp:
			output = writer("INFO:\tlooking for success result",output)
			while True:
				try:
					WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME,"success-result")))
					output = writer("INFO:\tSuccess Result\tfound",output)
					success = True
					break
				except TimeoutException:
					pass
				try:
					WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME,"form-error-message")))
					output = writer("INFO:\tSuccess Result\tFAIL",output)
					success = False
					break
				except TimeoutException:
					pass
        #----------------------
		try:
			xpathString = "//a[contains(text(), 'TEAMS view')]"
			backToAdminLink= WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,xpathString)))
			backToAdminLink.click()
			output = writer("INFO:\tClicked TEAMS view link to return to main Admin page",output)
		except TimeoutException:
			output = writer("INFO:\tClicked TEAMS view link to return to main Admin page\tFAIL",output)
	return start


if __name__ == "__main__":
	testdriver = webdriver.Firefox()
	prog = "save_TEAMS_edit_rights"
	global output
	output = []                                 #empty list to append Test Outputs
	output = writer("-"*50,output)
	output = writer(prog,output)  
	save_TEAMS_edit_rights(testdriver,60,output)
	testdriver.close()