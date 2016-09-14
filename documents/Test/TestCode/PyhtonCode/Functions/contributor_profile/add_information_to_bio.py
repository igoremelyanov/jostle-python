import os
from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.
from selenium.webdriver.support.ui import Select                #for selecting from dropdown menus
from get_datetime import get_datetime   #date\time funtion that we use for file names
from get_buildno import get_buildno
from path_est import path_est 
from pathToPythonCode import pathToPythonCode
from writer import writer               #function to handle outputs
import time


def add_information_to_bio(driver, output,stringBiography, arraySkills, arrayQualifications, arrayLabelsForLinks, arrayLinks, stringInterests, arrayPathesToPhotos):
	
	prog = os.path.basename(__file__).split(".")[0]      	#gets the name of the currently running program
	now,date = get_datetime()
	log_path,shot_path = path_est(date) 
	result = "pass"		                        	
	j=1	

	#Go to Bio
	try:
		bioButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:ContribProfile:bioButton")))
		bioButton.click()
		output = writer("VERIFY:\tQA:ContribProfile:bioButton\tPASS",output)		
		driver.save_screenshot(shot_path+"add_information_to_bio"+now+"_"+str(j)+".png")		   
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:ContribProfile:bioButton\tFAIL",output)
		result = "fail"
		j+=1
		driver.save_screenshot(shot_path+"add_information_to_bio"+now+"_"+str(j)+".png")
	#------------------------------------------		

	#Push edit button
	try:
		bioEditButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:ContribProfile:bio:editButton")))		
		output = writer("VERIFY:\tQA:ContribProfile:bio:editButton\tPASS",output)
		bioEditButton.click()
		output = writer("INFO:\tQA:ContribProfile:bio:editButton clicked",output)		
		j+=1
		driver.save_screenshot(shot_path+"add_information_to_bio"+now+"_"+str(j)+".png")		   
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:ContribProfile:bio:editButton\tFAIL",output)
		result = "fail"
		j+=1
		driver.save_screenshot(shot_path+"add_information_to_bio"+now+"_"+str(j)+".png")
	#------------------------------------------	

	
	#Add information to Biography
	try:		
		bioTextarea = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@placeholder,'Type your story here')]")))		
		output = writer("VERIFY:\tBiography textarea\tPASS",output)
		bioTextarea.click()	
		output = writer("INFO:\tBiography textarea clicked",output)	   
		time.sleep(1)
		bioTextarea.send_keys(stringBiography)
		output = writer("VERIFY:\tBiography textarea input\tPASS",output)					   
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tBiography textarea\tFAIL",output)
		result = "fail"
	#------------------------------------------

	#Adding Skills
	for skill in arraySkills:
		try:
			addSkills = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@placeholder,'Add your skills')]")))			
			output = writer("VERIFY:\tSkills field\tPASS",output)			
			addSkills.send_keys(skill)
			output = writer("INFO:\tAdd text to skills textfield",output)			
			driver.find_element_by_xpath("//*[contains(@placeholder,'Add your skills')]/../button").click()
			output = writer("INFO:\tQA:JellybeansList:addButton clicked",output)			
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tSkills field\tFAIL",output)
			result = "fail"
	#------------------------------------------	


	#Adding Qualifications
	for qualification in arrayQualifications:
		try:
			addQualifications = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@placeholder,'Add Your Qualifications')]")))			
			output = writer("VERIFY:\tQualifications textfield\tPASS",output)			
			addQualifications.send_keys(qualification)
			output = writer("INFO:\tAdd text to Qualifications textfield",output)			
			driver.find_element_by_xpath("//*[contains(@placeholder,'Add Your Qualifications')]/../button").click()
			output = writer("INFO:\tQA:JellybeansList:addButton clicked",output)			
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tQualifications textfield\tFAIL",output)
			result = "fail"
	#------------------------------------------



	#Add label for link
	i=1
	for link in arrayLinks:		
		try:
			linkLabel = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@placeholder,'Add a label')]/../../div["+str(i)+"]/.//*[contains(@placeholder,'Add a label')]")))		
			output = writer("VERIFY:\tLabel for link textfield\tPASS",output)
			linkLabel.send_keys(arrayLabelsForLinks[i-1])
			output = writer("INFO:\tLabel for link textfield input\tPASS",output)				
			j+=1
			driver.save_screenshot(shot_path+"add_information_to_bio"+now+"_"+str(j)+".png")					   
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tLabel for link textfield\tFAIL",output)
			result = "fail"
			j+=1
			driver.save_screenshot(shot_path+"add_information_to_bio"+now+"_"+str(j)+".png")

		#------------------------------------------


		#Add link
		try:
			addLink = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@placeholder,'Add web link')]/../../div["+str(i)+"]/.//*[contains(@placeholder,'Add web link')]")))		
			output = writer("VERIFY:\tLink textfield\tPASS",output)
			addLink.click()	
			output = writer("INFO:\tLink textfield clicked",output)		
			
			addLink.send_keys(arrayLinks[i-1])
			output = writer("INFO:\tLink textfield input",output)
			j+=1
			driver.save_screenshot(shot_path+"add_information_to_bio"+now+"_"+str(j)+".png")
			driver.find_element_by_xpath("//*[contains(@placeholder,'Add web link')]/../../div["+str(i)+"]/.//*[contains(@placeholder,'Add web link')]/../img[2]").click()										
			output = writer("VERIFY:\tclick on gwt-Image cursorPointer\tPASS",output)			
			j+=1
			driver.save_screenshot(shot_path+"add_information_to_bio"+now+"_"+str(j)+".png")		   
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tLink textfield\tFAIL",output)
			result = "fail"
			j+=1
			driver.save_screenshot(shot_path+"add_information_to_bio"+now+"_"+str(j)+".png")
		i+=1
		#------------------------------------------

	
	#Add information to Interests
	try:	
		interestsTextfield = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(@placeholder,'Add your interests')]")))	
		output = writer("VERIFY:\tInterests textarea\tPASS",output)		   
		interestsTextfield.send_keys(stringInterests)
		output = writer("INFO:\tInterests textarea input\tPASS",output)					   
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tInterests textarea\tFAIL",output)
		result = "fail"
	#------------------------------------------	

	
	#save configuration 
	try:
		saveButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:ContribProfile:bio:saveButton")))		
		output = writer("VERIFY:\tQA:ContribProfile:bio:saveButton\tPASS",output)
		saveButton.click()
		output = writer("INFO:\tQA:ContribProfile:bio:saveButton clicked",output)
		j+=1
		driver.save_screenshot(shot_path+"add_information_to_bio"+now+"_"+str(j)+".png")		   
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:ContribProfile:bio:saveButton\tFAIL",output)
		result = "fail"
		j+=1
		driver.save_screenshot(shot_path+"add_information_to_bio"+now+"_"+str(j)+".png")
	#-------------------------------------------

			
	return result