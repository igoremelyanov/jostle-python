import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import TimeoutException	    #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.
from get_buildno import get_buildno
from pathToPythonCode import pathToPythonCode
from writer import writer               #function to handle outputs
import time



def check_contributor_profile_info(driver, output,  numberOfFields, exp_fieldValues, xpathArray):
	
	prog = os.path.basename(__file__).split(".")[0]      	#gets the name of the currently running program	
	result = "pass"		                        	

	#Go to Info
	try:
		infoButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:ContribProfile:infoButton")))		
		output = writer("VERIFY:\tQA:ContribProfile:infoButton\tPASS",output)
		infoButton.click()
		output = writer("INFO:\tQA:ContribProfile:infoButton clicked",output)		
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:ContribProfile:infoButton\tFAIL",output)
		result = "fail"

		
	#------------------------------------------

	#Verify contributor_name info 
	
	for i in range(0,numberOfFields):			
		try:
			receivedElement = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,xpathArray[i])))			
			nameOf_receivedElement = receivedElement.get_attribute("innerHTML") #Retrieve contents of inside the mailinator mail entry line.
			output = writer("INFO:\tName of element received by xpath is - "+nameOf_receivedElement+" ",output)

			if (exp_fieldValues[i] in nameOf_receivedElement):				
				output = writer("VERIFY:\tThe field value of received element is correct\tPASS",output)					
			else:
				output = writer("VERIFY:\tThe field value of received element is wrong\tFAIL",output)
				result = "fail"					
		except (NoSuchElementException, TimeoutException):
			output = writer("INFO:\tNoSuchElementException",output)
			result= "fail"
	
	return result