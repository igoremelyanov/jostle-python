import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
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


def check_information_in_bio(driver, output, stringBiography, arraySkills, arrayQualifications, arrayLabelsForLinks, stringInterests, arrayPathesToPhotos):
	
	prog = os.path.basename(__file__).split(".")[0]      	#gets the name of the currently running program
	now,date = get_datetime()
	log_path,shot_path = path_est(date) 
	result = "pass"		                        	
	j=1
	
	
	
	#Go to Bio
	try:
		bioButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:ContribProfile:bioButton")))				
		output = writer("VERIFY:\tQA:ContribProfile:bioButton\tPASS",output)
		bioButton.click()
		output = writer("INFO:\tQA:ContribProfile:bioButton clicked",output)		
		driver.save_screenshot(shot_path+"check_information_in_bio"+now+"_"+str(j)+".png")				   
	except (NoSuchElementException, TimeoutException):
		result = "fail"
		output = writer("VERIFY:\tQA:ContribProfile:bioButton\tFAIL",output)
		driver.save_screenshot(shot_path+"check_information_in_bio"+now+"_"+str(j)+".png")
	#------------------------------------------ 

	
	#Verify text appears in Biography
	output = writer("INFO:\tBiography verification -----------------",output)
	try:
		receivedElement = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='gwt-HTML bioTabText']")))				
		valueOf_receivedElement = receivedElement.get_attribute("innerHTML") #Retrieve contents of inside the mailinator mail entry line.
		j+=1		
		driver.save_screenshot(shot_path+"check_information_in_bio"+now+"_"+str(j)+".png")
		if stringBiography in valueOf_receivedElement:
			output = writer("VERIFY:\tstringBiography\tPASS",output)
		else:
			result = "fail"
			output = writer("VERIFY:\tstringBiography\tFAIL",output)
	except (NoSuchElementException, TimeoutException):
		result = "fail"
		output = writer("VERIFY:\tstringBiography\tFAIL",output)
		driver.save_screenshot(shot_path+"check_information_in_bio"+now+"_"+str(j)+".png")
	#-------------------------------------------
	

	#Verify Skills
	output = writer("INFO:\tSkills verification -----------------",output)	
	count = 0
	for skill in arraySkills:
		try:
			receivedElement = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='gwt-HTML bioTabText']/../../../div[3]/div[2]/div/div["+str(count+1)+"]/div")))
			valueOf_receivedElement = receivedElement.get_attribute("innerHTML") #Retrieve contents of inside the mailinator mail entry line.		
			count+=1
			if skill in valueOf_receivedElement:					    
				output = writer("VERIFY:\t"+valueOf_receivedElement+" skill is in Skills \tPASS",output) 							  
			else:
				result = "fail"
				output = writer("VERIFY:\t"+valueOf_receivedElement+" skill is in Skills \tFAIL",output) 
		except (NoSuchElementException, TimeoutException):
			result = "fail"
			output = writer("VERIFY:\tSkills verification\tFAIL",output)
	#-------------------------------


	#Verify Qualifications
	output = writer("INFO:\tQualifications verification -----------------",output)	
	count = 0
	for qualification in arrayQualifications:
		try:
			receivedElement = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='gwt-HTML bioTabText']/../../../div[5]/div[2]/div/div["+str(count+1)+"]/div")))
			valueOf_receivedElement = receivedElement.get_attribute("innerHTML") #Retrieve contents of inside the mailinator mail entry line.			
			count+=1
			if qualification in valueOf_receivedElement:					    
				output = writer("VERIFY:\t"+valueOf_receivedElement+" qualification is in Qualifications \tPASS",output) 							  
			else:
				result = "fail"
				output = writer("VERIFY:\t"+valueOf_receivedElement+" qualification is in Qualifications \tFAIL",output) 
		except (NoSuchElementException, TimeoutException):
			result = "fail"
			output = writer("VERIFY:\tQualifications verification\tFAIL",output)
	#-------------------------------


	#Verify Links
	output = writer("INFO:\tLinks verification -----------------",output)	
	count = 0
	for link in arrayLabelsForLinks:
		try:
			receivedElement = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='gwt-HTML bioTabText']/../../../div[7]/div[2]/div["+str(count+1)+"]/div")))			
			valueOf_receivedElement = receivedElement.get_attribute("innerHTML") #Retrieve contents of inside the mailinator mail entry line.				
			count+=1
			if link in valueOf_receivedElement:					    
				output = writer("VERIFY:\t"+valueOf_receivedElement+" link is in Links \tPASS",output) 							  
			else:
				result = "fail"
				output = writer("VERIFY:\t"+valueOf_receivedElement+" link is in Links \tFAIL",output) 
		except (NoSuchElementException, TimeoutException):
			result = "fail"
			output = writer("VERIFY:\tLinks verification\tFAIL",output)			 
	#-------------------------------


	#Verify Interests
	output = writer("INFO:\tInterests verification -----------------",output)	
	try:
		receivedElement = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='gwt-HTML bioTabText']/../../../div[9]/div[2]/div")))		
		valueOf_receivedElement = receivedElement.get_attribute("innerHTML") #Retrieve contents of inside the mailinator mail entry line.
		output = writer("INFO:\tverify Interests",output)
		print "Value of Interests string", stringInterests	
		if stringInterests in valueOf_receivedElement:
			output = writer("VERIFY:\tstringInterests\tPASS",output)
		else:
			result = "fail"
			output = writer("VERIFY:\tstringInterests\tFAIL",output)
	except (NoSuchElementException, TimeoutException):
		result = "fail"
		output = writer("VERIFY:\tstringInterests\tFAIL",output)
	
	
			
	return result