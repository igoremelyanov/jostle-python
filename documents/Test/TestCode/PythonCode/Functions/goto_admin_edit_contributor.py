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

def goto_admin_edit_contributor(contributor,driver = None,intervalWaitForPage = None,output = None):
	"""
	   this is a function that is used to go to the Admin Edit/Delete contributor page.
	   @param driver: instance of selenium webdriver being used by class that called this function.
	   @param contributor: instance for name/email to find the contributor
	   @param intervalWaitForPage: interval that webdriver will wait for page to load before abort, set to 1 min if empty.
	   @param output: variable for the log buffer used by the test.
	   ++ All arguments needed, but it is possible to set intervalWaitForPage, password, screenshotPath, now, and screenshotPos to None.
	"""
	global start, log_path
	pageLoadWaitInterval = intervalWaitForPage if intervalWaitForPage != None else 5
	if (driver == None or output == None):
		print "ERROR in goto_admin_edit_contributor(): Please send webdriver, and output as arguments."
	else:
		driver.set_page_load_timeout(pageLoadWaitInterval)
		try:
			start = time.time()
			#Edit/Delete individual Contributor
			try:
				editDeleteContributors = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:editDeleteContributors")))
				editDeleteContributors.click()
				output = writer("INFO:\tClicked editDeleteContributors",output)
			except TimeoutException:
				output = writer("INFO:\tQA:editDeleteContributors\tFAIL did NOT load",output)
			#---------------------------
			#Search Text Box
			try:
				searchText = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"searchText")))
				searchText.send_keys(contributor)
				output = writer("INFO:\tSubmitted: "+contributor,output)
			except TimeoutException:
				output = writer("INFO:\tsearchText\tFAIL",output)
				driver.save_screenshot(shot_path+"links2_CheckIndividalDownHierRights_"+now+"_005.png")
			#---------------------------
			#Search Button
			try:
				searchButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"searchButton")))
				searchButton.click()
				output = writer("INFO:\tsearchButton click",output)
			except TimeoutException:
				output = writer("VERIFY:\tsearchButton\tFAIL",output)
			#---------------------------
			#Find the Correct Contributor
			try:
				editContributor = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.LINK_TEXT,"EDIT")))
				editContributor.click()
				output = writer("INFO:\tClicked EDIT button",output)
			except TimeoutException:
				output = writer("INFO:\tNO EDIT button",output)
			#---------------------------
		except TimeoutException:
			output = writer("INFO:\tGo to Admin Edit/Delete Contributor FAILED for: "+contributor,output)
	return start


if __name__ == "__main__":
	testdriver = webdriver.Firefox()
	prog = "goto_admin_edit_contributor"
	global output
	output = []                                 #empty list to append Test Outputs
	output = writer("-"*50,output)
	output = writer(prog,output)  
	goto_admin_edit_contributor("tom.merrit@mailinator.com",testdriver,60,output)
	testdriver.close()