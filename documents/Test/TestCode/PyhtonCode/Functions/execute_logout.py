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

def execute_logout(driver = None,intervalWaitForPage = None,output = None):
	"""
	   this is a function that is used to log out before the script tries a  new login.
	   @param driver: instance of selenium webdriver being used by class that called this function.
	   @param intervalWaitForPage: interval that webdriver will wait for page to load before abort, set to 1 min if empty.
	   @param output: variable for the log buffer used by the test.
	   ++ All arguments needed, but it is possible to set intervalWaitForPage, password, screenshotPath, now, and screenshotPos to None.
	"""
	global start, log_path
	pageLoadWaitInterval = intervalWaitForPage if intervalWaitForPage != None else 5
	if (driver == None or output == None):
		print "ERROR in execute_logout(): Please send webdriver, and output as arguments."
	else:
		driver.set_page_load_timeout(pageLoadWaitInterval)
		#-------------------------
		# execute the logout
		try:
			start = time.time()
			output = writer("INFO:\tLooking for Logout button",output)
			logOutButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnLogout")))
			logOutButton.click()  
			output = writer("INFO:\tLogout button clicked",output) 
			logOutOKConfirmation = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"QA:JostleDialogs:okButton")))                      
			logOutOKConfirmation.click()
			output = writer("INFO:\tLogout confirmation OK button clicked",output) 
			
		except TimeoutException:
			output = writer("INFO:\tlogout failed",output)
		
	return start


if __name__ == "__main__":
	testdriver = webdriver.Firefox()
	prog = "execute_logout"
	global output
	output = []                                 #empty list to append Test Outputs
	output = writer("-"*50,output)
	output = writer(prog,output)  
	execute_logout(testdriver,None,output)
	testdriver.close()