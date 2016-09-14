import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select                #for selecting from dropdown menus
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import TimeoutException	    #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.
from get_datetime import get_datetime   #date\time funtion that we use for file names
from get_buildno import get_buildno
from path_est import path_est 
from pathToPythonCode import pathToPythonCode
from writer import writer               #function to handle outputs
import time


def add_tags_to_words_cloud(driver, output, arrayPromotedTags, arrayBlockedTags):
	
	prog = os.path.basename(__file__).split(".")[0]      	#gets the name of the currently running program
	now,date = get_datetime()
	log_path,shot_path = path_est(date) 
	result = "pass"		                        	
	j=1	
	

	#Go to Tags tab
	try:		
		tagTabButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:ContribProfile:aboutButton")))
		output = writer("VERIFY:\tQA:ContribProfile:aboutButton\tPASS",output)
		j+=1
		driver.save_screenshot(shot_path+"add_tags_to_words_cloud"+now+"_"+str(j)+".png")		
		tagTabButton.click()		
		output = writer("INFO:\tQA:ContribProfile:aboutButton clicked",output)
		j+=1
		driver.save_screenshot(shot_path+"add_tags_to_words_cloud"+now+"_"+str(j)+".png")		   
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:ContribProfile:aboutButton\tFAIL",output)
		result = "fail"
		j+=1
		driver.save_screenshot(shot_path+"add_tags_to_words_cloud"+now+"_"+str(j)+".png")
	#------------------------------------------	


	#Push edit button
	try:		
		editButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:ContribProfile:about:editButton")))
		output = writer("VERIFY:\tQA:ContribProfile:about:editButton\tPASS",output)
		editButton.click()
		output = writer("INFO:\tQA:ContribProfile:about:editButton clicked",output)
		j+=1
		driver.save_screenshot(shot_path+"add_tags_to_words_cloud"+now+"_"+str(j)+".png")		   
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:ContribProfile:about:editButton\tFAIL",output)
		result = "fail"
		j+=1
		driver.save_screenshot(shot_path+"add_tags_to_words_cloud"+now+"_"+str(j)+".png")
	#------------------------------------------	


	#Add promote tags to Words Cloud	
	for tag in arrayPromotedTags:		
		try:
			cloudPanel = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME,"profileCloudEditPanel")))	
			output = writer("VERIFY:\tprofileCloudEditPanel\tPASS",output)		
			cloudPanel.click()						
			output = writer("INFO:\tprofileCloudEditPanel clicked",output)		   
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tprofileCloudEditPanel\tFAIL",output)
			result = "fail"
		

		output = writer("INFO:\tAdding promote tag1",output)
		try:
			cloudPanel = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME,"profileCloudEditPanel")))					
			cloudPanel.find_element_by_xpath(".//input").send_keys(tag)		
			output = writer("VERIFY:\tprofileCloudEditPanel:input\tPASS",output)				   
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tprofileCloudEditPanel:input\tFAIL",output)
			result = "fail"

		
		try:			
			addItemButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:EditableListBox:addItemButton")))				   
			output = writer("VERIFY:\tQA:EditableListBox:addItemButton\tPASS",output)
			addItemButton.click()
			output = writer("INFO:\tQA:EditableListBox:addItemButton clicked",output)		   
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tQA:EditableListBox:addItemButton\tFAIL",output)
			result = "fail"
	
	#------------------------------------------	


	#Add blocked tags to Words Cloud	
	
	for blocked_tag in arrayBlockedTags:				
		try:
			cloudPanel = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME,"profileCloudEditPanel")))									
			output = writer("VERIFY:\tprofileCloudEditPanel\tPASS",output)
			cloudPanel.find_element_by_id("QA:about:blockedTags").click()	
			output = writer("INFO:\tprofileCloudEditPanel clicked\tPASS",output)
			cloudPanel.find_element_by_id("QA:about:blockedTags").send_keys(blocked_tag)	
			output = writer("VERIFY:\tprofileCloudEditPanel:input\tPASS",output)				   
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tprofileCloudEditPanel:input\tFAIL",output)
			result = "fail"		

		
		try:			
			addItemButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='QA:about:blockedTags']/.././/button")))			   
			output = writer("VERIFY:\tQA:EditableListBox:addItemButton\tPASS",output)
			addItemButton.click()
			output = writer("INFO:\tQA:EditableListBox:addItemButton clicked\tPASS",output)		   
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tQA:EditableListBox:addItemButton\tFAIL",output)
			result = "fail"	

	#------------------------------------------
	

	#save configuration for promote and blocked tags
	try:
		saveButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:ContribProfile:about:saveButton")))
		output = writer("VERIFY:\tQA:ContribProfile:saveButton\tPASS",output)
		saveButton.click()
		output = writer("INFO:\tQA:ContribProfile:saveButton clicked\tPASS",output)
		j+=1
		driver.save_screenshot(shot_path+"add_tags_to_words_cloud"+now+"_"+str(j)+".png")		   
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:ContribProfile:saveButton\tFAIL",output)
		result = "fail"
		j+=1
		driver.save_screenshot(shot_path+"add_tags_to_words_cloud"+now+"_"+str(j)+".png")
	#-------------------------------------------
	
			
	return result