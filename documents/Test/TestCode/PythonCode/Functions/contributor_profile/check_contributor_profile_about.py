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



def check_contributor_profile_about(driver, output, arrayPromotedTags, arrayBlockedTags):
	
	prog = os.path.basename(__file__).split(".")[0]      	#gets the name of the currently running program
	result = "pass" 	
	
	
	output = writer("INFO:\tVerify promote tags appears in words Cloud  ------------",output)
	wordsCloudArray=[]	
	#time.sleep(5)
	#totalElements = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME,"profileTagCloud"))) - do not work because explicit wait gets a sigle element, not a list			 
	#KIMAR NOTE: This has the same effect of a sleep of 5 seconds, just to load enough page for us to proceed. Not the full page.
	#If some magic happens and we load page really fast, we will wait less than 5 secs.
	try:
		WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID,"viewBuildTracker3")))
	except (NoSuchElementException, TimeoutException):
		output = writer("INFO:\tPage load incomplete",output)
	try:
		totalElements =  driver.find_elements_by_class_name("profileTagCloud")
		for x in range(0,len(totalElements)):
			try:
				xpathString = "//div[@class='profileTagCloud']["+str(x+1)+"]/div"
				# output = writer("INFO:\tXPATH:\t"+xpathString,output)				#for debug					
				receivedElement = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,xpathString)))	
				valueOf_receivedElement = receivedElement.get_attribute("innerHTML") #Retrieve contents of inside the mailinator mail entry line.											  
				wordsCloudArray.append(valueOf_receivedElement)
			except (NoSuchElementException, TimeoutException):
				output = writer("INFO:\tUnable to find element in tags",output)							  
		
		for promotedTag in arrayPromotedTags: 							
			if promotedTag in wordsCloudArray:			
				output = writer("VERIFY:\t"+promotedTag+"- The promote tag is in Words Cloud\tPASS",output)							  
			else:
				output = writer("VERIFY:\t"+promotedTag+"- The promote tag is NOT in Words Cloud\tFAIL",output) 
				result = "fail"	
		#---------------------------------------------								   
			
		
		output = writer("INFO:\tVerify blocked tags DON'T appear in words Cloud  -------------",output)	
		
		for blockedTag in arrayBlockedTags:  							 
			if blockedTag in wordsCloudArray: 
				output = writer("VERIFY:\t"+blockedTag+"- The blocked tag is visible in Words Cloud\tFAIL",output)
				result = "fail"	 							 
			else:			
				output = writer("VERIFY:\t"+blockedTag+"- The blocked tag is NOT in Words Cloud\tPASS",output) 
		#------------------------------------------------
	except (NoSuchElementException, TimeoutException):
		output = writer("INFO:\tCloud tag not found",output)							  
	

	return result