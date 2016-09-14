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

def goto_admin_iframe(driver = None,intervalWaitForPage = None,output = None):
	"""
	   this is a function that is used to switch to the Admin page iframe.
	   @param driver: instance of selenium webdriver being used by class that called this function.
	   @param intervalWaitForPage: interval that webdriver will wait for page to load before abort, set to 1 min if empty.
	   @param output: variable for the log buffer used by the test.
	   ++ All arguments needed, but it is possible to set intervalWaitForPage, password, screenshotPath, now, and screenshotPos to None.
	"""
	global start, log_path
	pageLoadWaitInterval = intervalWaitForPage if intervalWaitForPage != None else 5
	if (driver == None or output == None):
		print "ERROR in goto_admin_iframe(): Please send webdriver, and output as arguments."
	else:
		driver.set_page_load_timeout(pageLoadWaitInterval)
		try:
			start = time.time()
			#Admin Gear test
			try:
				adminGearButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))
				output = writer("VERIFY:\tQA:RichClient:btnAdmin\tPASS",output)
				adminGearButton.click()
				output = writer("INFO:\tclicked Admin Gear",output)
			except TimeoutException:
				output = writer("VERIFY:\tQA:RichClient:btnAdmin\tFAIL",output)
			#-------------------------
			#Switch iframes
			try:
				WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"QA:AdminFrame")))
				output = writer("INFO:\tsuccessfully switched to iframe",output)
			except TimeoutException:
				output = writer("INFO:\tcouldn't switch to iframe",output)
			#----------------------------	
		except TimeoutException:
			output = writer("INFO:\tgo to Admin iframe failed",output)	
	return start


if __name__ == "__main__":
	testdriver = webdriver.Firefox()
	prog = "goto_admin_iframe"
	global output
	output = []                                 #empty list to append Test Outputs
	output = writer("-"*50,output)
	output = writer(prog,output)  
	goto_admin_iframe(testdriver,60,output)
	testdriver.close()