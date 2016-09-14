	#Extract and Manage all Contributor Data

from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException   #exception for missing element
from selenium.common.exceptions import NoSuchFrameException     #exception for missing iframe
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.
import unittest, os, time
#custom functions
from get_datetime import get_datetime   #date\time funtion that we use for file names
from get_buildno import get_buildno     #function to get build number
from get_around_welcome_screen import get_around_welcome_screen #function to bypass startup popup
from path_est import path_est           #function to open date folders for dumps
from build_path_admin2_usqa import build_path_admin2_usqa
from get_newfile import get_newfile     #function to get most recently created file in a folder
from writer import writer               #function to handle outputs

# Special imports to OS specific actions
import os
import platform

#necessary globals
prog = os.path.basename(__file__).split(".")[0]     	#gets the name of the currently running program
now,date = get_datetime() 	                #get date and time string
output = []                                 #empty list to append Test Outputs
total = 48                                   #total number of tests
res = {"P" : 0}		                        #initializing pass/fail counters
log_path,shot_path = path_est(date)
#------------------------------------------------
class adminVerifyAccountUsageStatistics(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(10)         	#sets a general time to wait for an element to be found.
		self.driver.maximize_window()
		self.driver.set_page_load_timeout(60)

	def test_extract_contributors(self):
		global output
		global elapsed
		elapsed = 0
		output = writer("-"*50,output)
		output = writer(prog,output)
		output = writer("-"*50,output)
		output = writer("DATE:\t"+date,output)
		output = writer("OS PLATFORM:\t\t"+self.driver.capabilities["platform"],output)
		output = writer("BROWSER VERSION:\t"+self.driver.capabilities["browserName"]+" "+self.driver.capabilities["version"],output)
		output = writer("SELENIUM VERSION:\t"+ str(webdriver.__version__),output)
		#-------------------------
		url = "https://usqa.jostle.us/jostle-prod/login.html"
		output = writer("URL:\t"+url,output)
		self.driver.get(url)    #navigate to login with URL
		start = time.time()
		output = writer("INFO:\tJostle Launched",output)
		self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_001.png")
		try:
			usernameInput = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
			usernameInput.clear()                          #finding the login fields
			usernameInput.send_keys("jasonjones_usqa@mailinator.com")
			password = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
			password.clear()
			password.send_keys("Ship1Stop2")
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_002.png")
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME,"saveAndSubmit"))).click()
			output = writer("INFO:\tlogin submitted as Jason Jones",output)
		except TimeoutException:
			output = writer("INFO:\tlogin failed for Jason Jones",output)
			elapsed = time.time() - start
			self.fail("Unable to login, aborting test")
		#-------------------------
		global Build
		Build = get_buildno(self.driver)      #must pass self.driver to get_buildno()
		output = writer("BUILD:\t"+ Build,output)
		global buildPath
		buildPath = build_path_admin2_usqa(Build)
		#-------------------------
		#get around the welcome screen
		get_around_welcome_screen(self.driver)
		#-------------------------
		#Admin Gear test
		try:
			adminGear = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))
			output = writer("VERIFY:\tAdmin Gear\tPASS",output)
			res["P"] += 1   #add  1 to pass counter
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_003.png")
			adminGear.click()
			output = writer("INFO:\tClick Admin Gear",output)
		except TimeoutException:
			output = writer("VERIFY:\tQA:RichClient:btnAdmin\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_003.png")
		#-------------------------
		#Switch iframe
		try:
			WebDriverWait(self.driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"QA:AdminFrame")))
			output = writer("INFO:\tSuccessfully switched to iframe",output)
		except TimeoutException:
			output = writer("INFO:\tCouldn't switch to iframe",output)
		#-------------------------
		#Find Account information
		try:
			accountUsage = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:accountUsage")))
			output = writer("VERIFY:\tAccount information view\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_004.png")
			accountUsage.click()
			output = writer("INFO:\tClicked Account information ",output)
		except TimeoutException:
			output = writer("VERIFY:\tQA:accountUsage\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_004.png")
		#-------------------------
		#Verify page title
		try:
			pageTitle = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME,"title"))).text
			output = writer("INFO:\tPage title:\t"+pageTitle,output)
			if(pageTitle == "Account information"):
				output = writer("VERIFY:\tAccount information page loaded\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tAccount information page loaded.\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_005.png")
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\t Page not loaded.\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_005.png")

		#-------------------------
		#Verify Learn more link

		# Indentifies OS to assign a Tab switch key to be used by the test script.
		osName = platform.system();
		# Test running in Mac OS X.
		if(osName == "Darwin"):
			newTabKey = Keys.COMMAND
			tabSwitchKey = Keys.COMMAND
			output = writer("INFO:\tTesting running on MAC OS X.", output)
		# Test running in Linux.
		elif(osName == "Linux"):
			newTabKey = Keys.CONTROL
			tabSwitchKey = Keys.ALT
			output = writer("INFO:\tTesting running on Linux.", output)
		# Default case assumes it run on Windows.
		else:
			newTabKey = Keys.CONTROL
			tabSwitchKey = Keys.CONTROL
			output = writer("INFO:\tTesting running on Windows.", output)

		try:
			learnLink = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//span[@id='new-standard-links']/em/a")))
			learnLinkUrl = learnLink.get_attribute("href") #Workaround for JOS-5448
		except TimeoutException:
			output = writer("INFO:\tUnable to locate 'Learn more' link.", output)

		# Save the window opener (current window, do not mistaken with tab... not the same)
		main_window = self.driver.current_window_handle

		#open new tab
		learnLink.send_keys(newTabKey + Keys.RETURN)
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.TAG_NAME,"body"))).send_keys(tabSwitchKey + '2')
			self.driver.switch_to_window(main_window) #switch Selenium context to search elements in the new tab.
			#Workaround for JOS-5448 START
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.TAG_NAME,"body")))
			self.driver.get(learnLinkUrl)
			#Workaround for JOS-5448 END

			pageTitle = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.TAG_NAME,"h1"))).text
			if("Account Information" in pageTitle):
				output = writer("VERIFY:\tLearn more links open the correct page.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tLearn more links open the correct page.\tFAIL",output)
		except TimeoutException:
			output = writer("INFO:\tUnable to open 'Learn more' link page.", output)

		#-------------------------
		#Switch iframe
		try:
			#-------------------------
			#close new tab
			#return to old tab
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.TAG_NAME,"body"))).send_keys(tabSwitchKey + '1')
			self.driver.switch_to_window(main_window) #switch Selenium context to search elements in the new tab.
			#-------------------------
			WebDriverWait(self.driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"QA:AdminFrame")))
			output = writer("INFO:\tSuccessfully switched to iframe",output)
		except TimeoutException:
			output = writer("INFO:\tCouldn't switch to iframe",output)

		#-------------------------
		#Verify Subscription data and its format
		try:
			subSectionEl = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME,"subtitle")))
			try:
				if(subSectionEl.text == "Subscription"):
					output = writer("VERIFY:\tSubscription subsection label is present.\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
				else:
					output = writer("VERIFY:\tSubscription subsection label is present.\tFAIL",output)
					res["P"] += 1   #add 1 to pass counter
				accountSummary = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:origStartDate"))).text
				if( "Original start date:" in accountSummary):
					output = writer("VERIFY:\tOriginal date is present.\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
					substrgStartIndex = accountSummary.find("Original start date:")# Find the start index of the original start date string.
					origStartDate = accountSummary[substrgStartIndex:substrgStartIndex+33] # Limit string to check only values for original start date
					if("01/28/2014" in origStartDate):
						output = writer("VERIFY:\tOriginal date matches expected date.\t01/28/2014.\tPASS",output)
						res["P"] += 1   #add 1 to pass counter
					else:
						output = writer("VERIFY:\tOriginal date matches expected date.\t01/28/2014.\tFAIL",output)
				else:
					output = writer("VERIFY:\tOriginal date is present.\tFAIL",output)
				accountSummary = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:termStartDate"))).text
				if( "Current term start date:" in accountSummary):
					output = writer("VERIFY:\tCurrent term start date is present.\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
				else:
					output = writer("VERIFY:\tCurrent term start date is present.\tFAIL",output)
				accountSummary = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:termExpiryDate"))).text
				if( "Current term expiry date:" in accountSummary):
					output = writer("VERIFY:\tCurrent term expiry date is present.\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
				else:
					output = writer("VERIFY:\tCurrent term expiry date is present.\tFAIL",output)
				self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_006.png")
			except TimeoutException:
				output = writer("VERIFY:\t Account summary is missing. No Subscription data available.\tFAIL",output)
				self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_006.png")

			#---------------------------
			#Verify Users(Contributors) data and its format
		 	try:
				subSectionEl = WebDriverWait(subSectionEl, 15).until(EC.element_to_be_clickable((By.XPATH,".//../following-sibling::span")))
		 		if(subSectionEl.text == "Users (Contributors)"):
					output = writer("VERIFY:\tUsers (Contributors) subsection label is present.\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
				else:
					output = writer("VERIFY:\tUsers (Contributors) subsection label is present.\tFAIL",output)
					res["P"] += 1   #add 1 to pass counter
				accountSummary = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:purchased"))).text
				if( "Purchased:" in accountSummary):
					output = writer("VERIFY:\tNumber of users purchased is present.\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
					substrgStartIndex = accountSummary.find("Purchased:")# Find the start index of the purchased string.
					numPurchased = accountSummary[substrgStartIndex:substrgStartIndex+16] # Limit string to check only values for purchased accounts..
					if("50" in numPurchased):
						output = writer("VERIFY:\tPurchased matches expected value.\t50\tPASS",output)
						res["P"] += 1   #add 1 to pass counter
					else:
						output = writer("VERIFY:\tPurchased matches expected value.\t50\tFAIL",output)
				else:
					output = writer("VERIFY:\tNumber of users purchased is present.\tFAIL",output)

				accountSummary = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:created"))).text
				if( "Created:" in accountSummary):
					output = writer("VERIFY:\tNumber of users created is present.\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
				else:
					output = writer("VERIFY:\tNumber of users created is present.\tFAIL",output)

				accountSummary = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:remaining"))).text
				if( "Remaining:" in accountSummary):
					output = writer("VERIFY:\tNumber of users remaining term is present.\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
				else:
					output = writer("VERIFY:\tNumber of users remaining term is present.\tFAIL",output)
				self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
			except TimeoutException:
				output = writer("VERIFY:\t Account summary is missing. No Users(Contributors) data available.\tFAIL",output)
				self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
			#---------------------------
			#Verify Data Storage data and its format
			try:
				subSectionEl = WebDriverWait(subSectionEl, 15).until(EC.element_to_be_clickable((By.XPATH,".//../following-sibling::span")))
		 		if(subSectionEl.text == "Data Storage"):
					output = writer("VERIFY:\tData Storage subsection label is present.\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
				else:
					output = writer("VERIFY:\tData Storage subsection label is present.\tFAIL",output)
					res["P"] += 1   #add 1 to pass counter
				accountSummary = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:totalUsed"))).text
				if( "Total used:" in accountSummary):
					output = writer("VERIFY:\tTotal used storage is present.\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
				else:
					output = writer("VERIFY:\tTotal used storage is present.\tFAIL",output)
				accountSummary = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:allocation"))).text
				if( "Allocation:" in accountSummary):
					output = writer("VERIFY:\tAllocation is present.\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
					substrgStartIndex = accountSummary.find("Allocation:")# Find the start index of the purchased string.
					numPurchased = accountSummary[substrgStartIndex:substrgStartIndex+21] # Limit string to check only values for purchased accounts..
					if("20 GB" in numPurchased):
						output = writer("VERIFY:\tAllocated storage matches expected value.\t20 GB\tPASS",output)
						res["P"] += 1   #add 1 to pass counter
					else:
						output = writer("VERIFY:\tAllocated storage matches expected value.\t20 GB\tFAIL",output)
				else:
					output = writer("VERIFY:\tAllocation is present.\tFAIL",output)

			except TimeoutException:
				output = writer("VERIFY:\t Account summary is missing. No Data Storage data available.\tFAIL",output)
				self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
		except TimeoutException:
			output = writer("VERIFY:\t All except subsections is present.\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
		#---------------------------
		#Verify Contributor  data and its format
		try:
			contributorData = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:CONTRIBUTOR"))).text
			if( "CONTRIBUTOR" in contributorData):
				output = writer("VERIFY:\tCONTRIBUTOR label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tCONTRIBUTOR label is present.\tFAIL",output)
			contributorData = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:PROFILE_DATA']/td[@class='account-detail']"))).text
			if( "Profile data" in contributorData):
				output = writer("VERIFY:\tProfile data is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tProfile data is present.\tFAIL",output)
			contributorData = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:PROFILE_DATA']/td[@class='centered']"))).text
			if( "USA" in contributorData):
				output = writer("VERIFY:\tProfile data location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tProfile data location is USA.\tFAIL",output)
			contributorData = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:PROFILE_PHOTOS']/td[@class='account-detail']"))).text
			if( "Profile photos" in contributorData):
				output = writer("VERIFY:\tProfile photos is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tProfile photos is present.\tFAIL",output)
			contributorData = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:PROFILE_PHOTOS']/td[@class='centered']"))).text
			if( "USA" in contributorData):
				output = writer("VERIFY:\tProfile photos location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tProfile photos location is USA.\tFAIL",output)
			contributorData = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:PROFILE_ATTACHMENTS']/td[@class='account-detail']"))).text
			if( "Profile attachments" in contributorData):
				output = writer("VERIFY:\tProfile attachments is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tProfile attachments is present.\tFAIL",output)
			contributorData = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:PROFILE_ATTACHMENTS']/td[@class='centered']"))).text
			if( "USA" in contributorData):
				output = writer("VERIFY:\tProfile attachments location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tProfile attachments location is USA.\tFAIL",output)

			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tAll CONTRIBUTOR details available.\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
		#---------------------------
		#Verify TEAMS data and its format
		try:
			contributorData = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:TEAMS']/td")))
			contributorProperty = contributorData.text
			if( "TEAMS" in contributorProperty):
				output = writer("VERIFY:\tTEAMS label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tTEAMS label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:TEAMS_ORG_STRUCTURE']/td[@class='account-detail']"))).text
			if( "Organizational structure" in contributorProperty):
				output = writer("VERIFY:\tOrganizational structure label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tOrganizational structure label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:TEAMS_ORG_STRUCTURE']/td[@class='centered']"))).text
			if( "USA" in contributorProperty):
				output = writer("VERIFY:\tOrganizational structure location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tOrganizational structure location is USA.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:TEAMS_PROFILE_DATA']/td[@class='account-detail']"))).text
			if( "Profile data" in contributorProperty):
				output = writer("VERIFY:\tProfile data  label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tProfile data  label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:TEAMS_PROFILE_DATA']/td[@class='centered']"))).text
			if( "USA" in contributorProperty):
				output = writer("VERIFY:\tProfile data location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tProfile data location is USA.\tFAIL",output)

			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
		except TimeoutException:
			output = writer("VERIFY:\tAll TEAMS details available.\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
		#---------------------------
		#Verify DISCUSSIONS data and its format
		try:
			contributorData = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:DISCUSSIONS']/td")))
			contributorProperty =  contributorData.text
			if( "DISCUSSIONS" in contributorProperty):
				output = writer("VERIFY:\tDISCUSSIONS label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tDISCUSSIONS label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:DISCUSSIONS_TEXT']/td[@class='account-detail']"))).text
			if( "Text" in contributorProperty):
				output = writer("VERIFY:\tText label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tText label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,".//tr[@id='QA:DISCUSSIONS_TEXT']/td[@class='centered']"))).text
			if( "USA" in contributorProperty):
				output = writer("VERIFY:\tDiscussion Text location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tDiscussion Text location is USA.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:DISCUSSIONS_ATTACHMENTS']/td[@class='account-detail']"))).text
			if( "Attachments" in contributorProperty):
				output = writer("VERIFY:\tDiscussion attachments label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tDiscussion attachments label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,".//tr[@id='QA:DISCUSSIONS_ATTACHMENTS']/td[@class='centered']"))).text
			if( "USA" in contributorProperty):
				output = writer("VERIFY:\tDiscussion attachments location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tDiscussion attachments location is USA.\tFAIL",output)

			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
		except TimeoutException:
			output = writer("VERIFY:\tAll DISCUSSIONS details available.\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
		#---------------------------
		#Verify NEWS (Articles, Events, Classifieds) data and its format
		try:
			contributorData = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:ARTICLES']/td")))
			contributorProperty =  contributorData.text
			if( "NEWS, EVENTS, CLASSIFIEDS" in contributorProperty):
				output = writer("VERIFY:\tNEWS, EVENTS, CLASSIFIEDS label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tNEWS, EVENTS, CLASSIFIEDS label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:NEWS_ITEMS']/td[@class='account-detail']"))).text
			if( "Items" in contributorProperty):
				output = writer("VERIFY:\tNews Items label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tNews Items label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:NEWS_ITEMS']/td[@class='centered']"))).text
			if( "USA" in contributorProperty):
				output = writer("VERIFY:\tNews Items location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tNews Items location is USA.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:NEWS_IMAGES']/td[@class='account-detail']"))).text
			if( "Images" in contributorProperty):
				output = writer("VERIFY:\tImages label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tImages label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:NEWS_IMAGES']/td[@class='centered']"))).text
			if( "USA" in contributorProperty):
				output = writer("VERIFY:\tImages location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tImages location is USA.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:NEWS_ATTACHMENTS']/td[@class='account-detail']"))).text
			if( "Attachments" in contributorProperty):
				output = writer("VERIFY:\tAttachments label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tAttachments label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:NEWS_ATTACHMENTS']/td[@class='centered']"))).text
			if( "USA" in contributorProperty):
				output = writer("VERIFY:\tAttachments location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tAttachments location is USA.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:NEWS_FEED']/td[@class='account-detail']"))).text
			if( "Activity feed" in contributorProperty):
				output = writer("VERIFY:\tActivity feed label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tActivity feed label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:NEWS_FEED']/td[@class='centered']"))).text
			if( "USA" in contributorProperty):
				output = writer("VERIFY:\tActivity feed location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tActivity feed location is USA.\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
		except TimeoutException:
			output = writer("VERIFY:\tAll NEWS (Articles, Events, Classifieds) details available.\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
		#---------------------------
		#Verify LIBRARY data and its format
		try:
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:LIBRARY']/td"))).text
			if( "LIBRARY" in contributorProperty):
				output = writer("VERIFY:\tLIBRARY label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tLIBRARY label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:LIBRARY']/td[@class='centered']"))).text
			if( "USA" in contributorProperty):
				output = writer("VERIFY:\tLIBRARY data location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tLIBRARY data location is USA.\tFAIL",output)
		except TimeoutException:
			output = writer("VERIFY:\tAll LIBRARY details available.\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")
		#---------------------------
		#Verify MOBILE (login information) data and its format
		try:
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:MOBILE']/td"))).text
			if( "MOBILE (login information)" in contributorProperty):
				output = writer("VERIFY:\tMOBILE (login information) label is present.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tMOBILE (login information) label is present.\tFAIL",output)
			contributorProperty = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@id='QA:MOBILE']/td[@class='centered']"))).text
			if( "USA" in contributorProperty):
				output = writer("VERIFY:\tMobile login data location is USA.\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			else:
				output = writer("VERIFY:\tMobile login data location is USA.\tFAIL",output)
		except TimeoutException:
			output = writer("VERIFY:\tAll MOBILE (login information) details available.\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminVerifyAccountUsageStatistics_"+now+"_007.png")

		#---------------------------
		#Test summary
		end = time.time()
		elapsed = end - start
		output = writer("INFO:\ttestResultCount:\t"+str(res["P"])+"\t/\t"+str(total),output)
		#---------------------------

	def tearDown(self):
		global output
		if res["P"] == total:
			f = open(log_path+os.sep+prog+"_"+now+"_PASS.log",'w')
			g = open(buildPath+os.sep+prog+"_PASS.log",'w')
			output = writer("RESULTS:\t"+prog+"\tPASS\t"+str(elapsed)[0:-8]+"\t"+Build,output)
			f.writelines(output)
			g.writelines(output)
		else:
			f = open(log_path+os.sep+prog+"_"+now+"_FAIL.log",'w')
			g = open(buildPath+os.sep+prog+"_FAIL.log",'w')
			output = writer("RESULTS:\t"+prog+"\tFAIL\t"+str(elapsed)[0:-8]+"\t"+Build,output)
			f.writelines(output)
			g.writelines(output)
		f.close()
		g.close()
		self.driver.quit()                      #closes the webdriver


if __name__ == "__main__":
	 unittest.main()