import os
from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException	    #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.
from selenium.webdriver.support.ui import Select                #for selecting from dropdown menus
from get_datetime import get_datetime   #date\time funtion that we use for file names
from get_buildno import get_buildno
from path_est import path_est 
from pathToPythonCode import pathToPythonCode
from writer import writer               #function to handle outputs
import time




def create_new_contributor(driver, output, name, family_name, office_phone_number, mobile_phone_number,job_category, department,  location , hire_date, birthDate):
	
	prog = os.path.basename(__file__).split(".")[0]      	#gets the name of the currently running program
	now,date = get_datetime()
	log_path,shot_path = path_est(date) 
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

	#Create a new individual Contributor
	j=1
	try:
		createContributor = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:createContributor")))		
		output = writer("VERIFY:\tQA:createContributor\tPASS",output)		
		createContributor.click()
		output = writer("INFO:\tClicked createContributor",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:createContributor\tFAIL",output)
		result = "fail"		
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	#---------------------------
	
	#First Name	
	j+=1	
	try:
		firstName = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"firstName")))		
		output = writer("VERIFY:\tfirstName\tPASS",output)			
		firstName.send_keys(name)
		output = writer("INFO:\tSubmitted first name",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tfirstName\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------

	#Last Name     constFirstName = "FirstName_Build_"+Build+"_Time:"+now
	j+=1
	try:
		lastName = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"lastName")))		
		output = writer("VERIFY:\tlastName\tPASS",output)		
		lastName.send_keys(family_name)
		output = writer("INFO:\tSubmitted last name",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tlastName\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------

	#Work Email
	j+=1
	millis = str(round(time.time()))	
	
	constEmail = name+family_name+"_"+millis+"@mailinator.com"		
	try:
		workEmail = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"workEmail")))		
		output = writer("VERIFY:\tworkEmail\tPASS",output)		
		workEmail.send_keys(constEmail)
		output = writer("INFO:\tSubmitted work email",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tworkEmail\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------
	
	#Work Office Phone
	j+=1
	try:
		workOfficePhone = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"workOfficePhone")))		
		output = writer("VERIFY:\tworkOfficePhone\tPASS",output)		
		workOfficePhone.send_keys(office_phone_number)
		output = writer("INFO:\tSubmitted work office phone",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tworkOfficePhone\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------
	
	#Work Mobile Phone
	j+=1
	try:
		workMobilePhone = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"workMobilePhone")))		
		output = writer("VERIFY:\tworkMobilePhone\tPASS",output)		
		workMobilePhone.send_keys(mobile_phone_number)
		output = writer("INFO:\tSubmitted work mobile phone",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tworkMobilePhone\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------

	#External Id
	j+=1
	constID = now
	try:
		externalId = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"externalId")))		
		output = writer("VERIFY:\temployeeId\tPASS",output)		
		externalId.send_keys(constID)
		output = writer("INFO:\tSubmitted employee Id",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\texternalId\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------

	#Job Category
	j+=1
	try:
		title = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"title")))		
		output = writer("VERIFY:\tjobCategory\tPASS",output)		
		title.send_keys(job_category)
		output = writer("INFO:\tSubmitted job category",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\ttitle\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------
	
	#Department
	"""Requires [Department: Jedi] to exist """
	j+=1
	try:
		departmentDropdown = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"departmentDropdown")))		
		output = writer("VERIFY:\tdepartmentDropdown\tPASS",output)			
		Select(departmentDropdown).select_by_visible_text(department)
		output = writer("INFO:\tSubmitted department Dropdown",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tdepartmentDropdown\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------

	#Location
	"""requires [Location: Las Vegas] to exist"""
	j+=1
	try:
		locationDropdown = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"locationDropdown")))		
		output = writer("VERIFY:\tlocationDropdown\tPASS",output)
		Select(locationDropdown).select_by_visible_text(location)
		output = writer("INFO:\tSubmitted location Dropdown",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tlocationDropdown\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------
	
	#Hire Date
	j+=1
	try:
		hireDateInput = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"hireDateInput")))		
		output = writer("VERIFY:\thireDate\tPASS",output)
		hireDateInput.send_keys(hire_date)
		output = writer("INFO:\tSubmitted hire date",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\thireDateInput\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------

	#Birth Date
	j+=1
	try:
		birthDateInput = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"birthDateInput")))		
		output = writer("VERIFY:\tbirthDate\tPASS",output)		
		birthDateInput.send_keys(birthDate)
		output = writer("INFO:\tSubmitted birth date",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tbirthDateInput\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------

	#Work Messaging Label
	j+=1
	workMessagingLebel = name+family_name+"_"+job_category
	try:
		messagingTypeInput = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"messagingTypeInput")))		
		output = writer("VERIFY:\tmessagingTypeInput\tPASS",output)		
		messagingTypeInput.send_keys(workMessagingLebel)
		output = writer("INFO:\tSubmitted work Messaging Label",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tmessagingTypeInput\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------

	#Work Messaging ID
	j+=1
	millis = str(round(time.time()))	
	workMessagingID = millis
	try:
		messagingIdInput = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"messagingIdInput")))		
		output = writer("VERIFY:\tmessagingIdInput\tPASS",output)		
		messagingIdInput.send_keys(workMessagingID)
		output = writer("INFO:\tSubmitted work Messaging Id",output)		
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tworkmessagingIdInput\tFAIL",output)
		result = "fail"		
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	#---------------------------
	
	
	#Publishing and Editing Rights
	j+=1
	allow = False
	try:
		allowEditReportsToBelow = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"allowEditReportsToBelow")))		
		output = writer("VERIFY:\tallowEditReportsToBelow\tPASS",output)		   
		if not allow:			
			allowEditReportsToBelow.click()
			output = writer("INFO:\tSubmitted allow editing rights",output)
		else: 
			output = writer("INFO:\tSubmitted DISallow editing rights",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tallowEditReportsToBelow\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
	#---------------------------

	#Submit Create Contributor
	j+=1
	try:
		createAndInviteButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name=\"Create & Invite\"]")))		
		output = writer("VERIFY:\tcreateAndInviteButton\tPASS",output)
		createAndInviteButton.click()		   
		output = writer("INFO:\tcreateAndInviteButton clicked",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		stamp = True
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tcreateAndInviteButton\tFAIL",output)
		driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
		result = "fail"
		stamp = False
	#-----------------------------

	if stamp:
		output = writer("INFO:\tlooking for success",output)
		while True:
			try:
				WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME,"success-result")))				
				output = writer("VERIFY:\tSuccess Result\tPASS",output)              #the rest of this block is run only if the element is found				 
				output = writer("INFO:\tCreation Successful",output)
				j+=1
				driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
				break
			except (NoSuchElementException, TimeoutException):
				pass
			try:
				WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID,"contributor.errors")))				
				output = writer("VERIFY:\tSuccess Result\tFAIL",output)
				result = "fail"
				output = writer("INFO:\tContributor exists",output)
				j+=1
				driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
				break
			except (NoSuchElementException, TimeoutException):
				pass
			try:
				WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME,"form-error-message")))				
				output = writer("VERIFY:\tSuccess Result\tFAIL",output)
				result = "fail"
				output = writer("INFO:\tField Input Failure",output)
				j+=1
				driver.save_screenshot(shot_path+"create_new_contributor"+now+"_"+str(j)+".png")
				break
			except (NoSuchElementException, TimeoutException):
				pass
	else:
		output = writer("INFO:\tLooking for Success Result\tFAIL",output)
		result = "fail"

	#-----------------------------
		
	return result