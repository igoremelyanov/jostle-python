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
from get_around_welcome_screen import get_around_welcome_screen #function to bypass startup popup		#get around the welcome screen
from path_est import path_est           #function to open date folders for dumps
from build_path_admin2_usqa import build_path_admin2_usqa
from get_newfile import get_newfile     #function to get most recently created file in a folder
from writer import writer               #function to handle outputs
from downloadLocation_path import downloadLocation_path

#necessary globals
prog = os.path.basename(__file__).split(".")[0]     	#gets the name of the currently running program
now,date = get_datetime() 	                #get date and time string
output = []                                 #empty list to append Test Outputs
total = 8                                   #total number of tests
res = {"P" : 0}		                        #initializing pass/fail counters
log_path,shot_path = path_est(date)

#------------------------------------------------
#test credentials
# username = "admin@saml.jostle.us"
# password  = "a#w1^Nkmnni5@IS"

#------------------------------------------------
class adminLoginGoogleUser(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(20)         	#sets a general time to wait for an element to be found.
		self.driver.maximize_window()
		self.driver.set_page_load_timeout(60)

	def test_extract_contributors(self):
		global elapsed
		elapsed = 0
		global output
		output = writer("-"*50,output)
		output = writer(prog,output)
		output = writer("-"*50,output)
		output = writer("DATE:\t"+date,output)
		output = writer("OS PLATFORM:\t\t"+self.driver.capabilities["platform"],output)
		output = writer("BROWSER VERSION:\t"+self.driver.capabilities["browserName"]+" "+self.driver.capabilities["version"],output)
		output = writer("SELENIUM VERSION:\t"+ str(webdriver.__version__),output)
		#-------------------------
		#Login
		url = "https://usqa.jostle.us/jostle-prod/login.html"
		output = writer("URL:\t"+url,output)
		self.driver.get(url)    #navigate to login with URL
		start = time.time()
		output = writer("INFO:\tJostle Launched",output)
		self.driver.save_screenshot(shot_path+os.sep+"adminLoginGoogleUser_"+now+"_001.png")
		try:
			username = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
			username.clear()                          #finding the login fields
			username.send_keys("dwight@jostle.in")
			password = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
			password.clear()
			password.send_keys("Ship1Stop2")
			self.driver.save_screenshot(shot_path+os.sep+"adminLoginGoogleUser_"+now+"_002.png")
			submitButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME,"saveAndSubmit")))
			submitButton.click()
			output = writer("INFO:\tlogin submitted",output)
		except TimeoutException:
			nextButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"next")))
			nextButton.click()
		try:
			#-------------------------
			#Login to Google

			output = writer("INFO:\tGoogle credentials request page.",output)
			emailInput =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"Email")))
			output = writer("VERIFY:\tE-mail input\tPASS",output)
			emailInput.clear()                          #finding the login fields
			emailInput.send_keys("dwight@jostle.in")
			self.driver.save_screenshot(shot_path+os.sep+"adminLoginGoogleUser_"+now+"_003.png")
			emailInput.send_keys(Keys.ENTER)

			output = writer("INFO:\tE-mail credentials inserted",output)
			res["P"] += 1   #add  1 to pass counter"
		except TimeoutException:
			output = writer("INFO:\tGoogle login submit\tFAIL",output)
		#-------------------------
		#First try login and passwor in same screen
		try:
			passwordInput = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"Passwd")))
			passwordInput.clear()
			passwordInput.send_keys("Ship1Stop2")
			self.driver.save_screenshot(shot_path+os.sep+"adminLoginGoogleUser_"+now+"_004.png")
			signIn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"signIn")))
			signIn.click()
			output = writer("INFO:\tGoogle login submitted",output)
		except TimeoutException:
			nextButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"next")))
			nextButton.click()
			output = writer("INFO:\tInserted login id and clicked next",output)
			passwordInput = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"Passwd")))
			passwordInput.clear()
			passwordInput.send_keys("Ship1Stop2")
			self.driver.save_screenshot(shot_path+os.sep+"adminLoginGoogleUser_"+now+"_004.png")
			signIn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"signIn")))
			signIn.click()
			output = writer("INFO:\tGoogle login submitted",output)
		
		#-------------------------
		#get around the welcome screen
		get_around_welcome_screen(self.driver)
		#-------------------------
		global Build
		Build = get_buildno(self.driver)      #must pass self.driver to get_buildno()
		output = writer("BUILD:\t"+ Build,output)
		global buildPath
		buildPath = build_path_admin2_usqa(Build)
		#--------------------------
		#Check page elements
		self.driver.save_screenshot(shot_path+os.sep+"adminLoginGoogleUser_"+now+"_005.png")
		# Verify if NEWS menu option is available.
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:newsBtn")))
			output = writer("VERIFY:\tNEWS menu button is available.\tPASS",output)
			res["P"] += 1   #add  1 to pass counter"
		except TimeoutException:
			output = writer("VERIFY:\tNEWS menu button is available.\tFAIL",output)
		# Verify if TEAMS menu option is available.
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnTeams")))
			output = writer("VERIFY:\tTEAMS menu button is available.\tPASS",output)
			res["P"] += 1   #add  1 to pass counter"
		except TimeoutException:
			output = writer("VERIFY:\tTEAMS menu button is available.\tFAIL",output)
		# Verify if PEOPLE menu option is available.
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnPeople")))
			output = writer("VERIFY:\tPEOPLE menu button is available.\tPASS",output)
			res["P"] += 1   #add  1 to pass counter"
		except TimeoutException:
			output = writer("VERIFY:\tPEOPLE menu button is available.\tFAIL",output)
		# Verify if DISCUSSIONS menu option is available.
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnDiscussions")))
			output = writer("VERIFY:\tDISCUSSIIONS menu button is available.\tPASS",output)
			res["P"] += 1   #add  1 to pass counter"
		except TimeoutException:
			output = writer("VERIFY:\tDISCUSSIIONS menu button is available.\tFAIL",output)
		# Verify if LIBRARY menu option is available.
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:libraryBtn")))
			output = writer("VERIFY:\tLIBRARY menu button is available.\tPASS",output)
			res["P"] += 1   #add  1 to pass counter"
		except TimeoutException:
			output = writer("VERIFY:\tLIBRARY menu button is available.\tFAIL",output)
		# Verify if MORE menu option is available.
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:moreBtn")))
			output = writer("VERIFY:\tMORE menu button is available.\tPASS",output)
			res["P"] += 1   #add  1 to pass counter"
		except TimeoutException:
			output = writer("VERIFY:\tMORE menu button is available.\tFAIL",output)
		#-------------------------
		#Admin Gear test
		try:
			adminGearIcon = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))
			output = writer("VERIFY:\tAdmin Gear\tPASS",output)
			res["P"] += 1   #add  1 to pass counter
			self.driver.save_screenshot(shot_path+os.sep+"adminLoginGoogleUser_"+now+"_006.png")
			adminGearIcon.click()
			output = writer("INFO:\tClick Admin Gear",output)
		except TimeoutException:
			output = writer("VERIFY:\tQA:RichClient:btnAdmin\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminLoginGoogleUser_"+now+"_006.png")
		#---------------------------
		#Test wrap up
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