import os
from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException	    #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select                #for selecting from dropdown menus
from get_datetime import get_datetime   #date\time funtion that we use for file names
from get_buildno import get_buildno
from path_est import path_est 
from pathToPythonCode import pathToPythonCode
from writer import writer               #function to handle outputs
import time



def delete_contributor(driver, output, contributorName ):
	
	prog = os.path.basename(__file__).split(".")[0]      	#gets the name of the currently running program	
	result = "pass"		
	
	#Admin Gear Test
	try:		
		btnAdmin = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))		
		output = writer("VERIFY:\tQA:RichClient:btnAdmin\tPASS",output)			
		btnAdmin.click()
		output = writer("INFO:\tQA:RichClient:btnAdmin clicked",output)
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:RichClient:btnAdmin\tFAIL",output)
		result = "fail"	
	#-------------------------	
	
	#verify if link page was loaded
	try:
		WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.ID,"loading")))
	except TimeoutException:
		output = writer("INFO:\tPage may have failed during loading",output)
	
	#Frame switch
	try:
		driver.switch_to_frame("QA:AdminFrame")
		output = writer("INFO:\tSuccessfully switched to QA:AdminFrame",output)
	except NoSuchFrameException:
		output = writer("INFO:\tCouldn't switch to QA:AdminFrame",output)
		result = "fail"
	#-------------------------
	
	#Edit/Delete individual Contributor
	try:		
		editDeleteContributors = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:editDeleteContributors")))
		output = writer("VERIFY:\tQA:editDeleteContributors\tPASS",output)		
		editDeleteContributors.click()
		output = writer("INFO:\tQA:editDeleteContributors clicked",output)
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:editDeleteContributors\tFAIL",output)
		result = "fail"
	#---------------------------

	#Search Text Box
	try:
		searchText = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"searchText")))		
		output = writer("VERIFY:\tsearchText\tPASS",output)		
		searchText.send_keys(contributorName)		
		output = writer("INFO:\tSubmitted name",output)
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tsearchText\tFAIL",output)
		result = "fail"
	#---------------------------

	#Search Button
	try:
		searchButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"searchButton")))		
		output = writer("VERIFY:\tsearchButton\tPASS",output)			
		searchButton.click()
		output = writer("INFO:\tsearchButton clicked",output)
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tsearchButton\tFAIL",output)
		result = "fail"
	#---------------------------

	#Find and Delete the Correct Contributor
	try:
		deleteItem = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME,"delete-item")))		
		output = writer("VERIFY:\tredDeleteButton\tPASS",output)		
		deleteItem.click()
		output = writer("INFO:\tClicked red delete button",output)
		alert = driver.switch_to_alert()
		alert.accept()
		stamp = True
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tredDeleteButton\tFAIL",output)
		stamp = False
		result = "fail"
	#-------------------------

	#Success?
	if stamp:
		output = writer("INFO:\tlooking for success",output)
		while True:
			try:
				driver.find_element_by_class_name("success-result")
				output = writer("VERIFY:\tSuccess Result\tPASS",output)              #the rest of this block is run only if the element is found				
				output = writer("INFO:\tDeletion Successful",output)				
				break
			except (NoSuchElementException, TimeoutException): pass
			try:
				driver.find_element_by_class_name("form-error-message")
				output = writer("VERIFY:\tSuccess Result\tFAIL",output)              #the rest of this block is run only if the element is found
				output = writer("INFO:\tDeletion Fail. Cannot Delete self",output)
				break
			except (NoSuchElementException, TimeoutException):  pass
	else:
		output = writer("VERIFY:\tsuccess-result\tFAIL",output)
		result = "fail"
	
	#----------------------------------------------------------------------------
		
	return result