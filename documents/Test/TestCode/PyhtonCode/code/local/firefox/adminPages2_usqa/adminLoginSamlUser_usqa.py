#Extract and Manage all Contributor Data

from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
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
from downloadLocation_path import downloadLocation_path

#necessary globals
prog = os.path.basename(__file__).split(".")[0]     	#gets the name of the currently running program
now,date = get_datetime() 	                #get date and time string
output = []                                 #empty list to append Test Outputs
total = 7                                   #total number of tests
res = {"P" : 0}		                        #initializing pass/fail counters
log_path,shot_path = path_est(date)

#------------------------------------------------
#test credentials
# username = "admin@saml.jostle.us"
# password  = "a#w1^Nkmnni5@IS"

#------------------------------------------------
class adminLoginSamlUser(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(20)         	#sets a general time to wait for an element to be found.
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
		#Login
		url = "https://usqa.jostle.us/jostle-prod/login.html"
		output = writer("URL:\t"+url,output)
		self.driver.get(url)    #navigate to login with URL
		start = time.time()
		output = writer("INFO:\tJostle Launched",output)
		self.driver.save_screenshot(shot_path+os.sep+"adminLoginSamlUser_"+now+"_001.png")
		try:
			usernameInput =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
			usernameInput.clear()                          #finding the login fields
			usernameInput.send_keys("admin.saml2@jostle.us")
			password =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
			password.clear()
			password.send_keys("a#w1^Nkmnni5@IS")
			self.driver.save_screenshot(shot_path+os.sep+"adminLoginSamlUser_"+now+"_002.png")
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME,"saveAndSubmit"))).click()
			output = writer("INFO:\tlogin submitted as SAML user",output)
		except TimeoutException:
			output = writer("INFO:\tlogin failed for SAML user",output)
			elapsed = time.time() - start
			self.fail("Unable to login, aborting test")
		#-------------------------
		#Login to saml 
		# If URL https://saml2.jostle.us/adfs/ls/?SAMLRequest=fZFfb4IwFMXf9ymavkOxirJGMG7GzMRlRHAPe6tQsQZa7S1mH38IsrkX3%2Frn3N89OWc6%2B65KdBEGpFYhHrgeRkJlOpeqCPE2XToBnkVPU%2BBVSU9sXtuD2ohzLcCiOYAwtpl71QrqSphEmIvMxHazDvHB2hMwQmo4c%2FeowZbCrYF0J%2Bf6Sq5MkiQfhJeS91%2BNCKNFg5eK29ZTT2ot3KF4vgdSAsFoqU0mWmsh3vMSBEarRYi573N6CIK8yMdF4Y%2Fo6CgmdLcPJs8iyK8iiDmAvIi%2FMYBarBRYrmyIqTfwHW%2FsDGjqDRn1GR26lPpfGMVGW53p8kWqLqnaKKY5SGCKVwKYzVgyf18z6nps14mAvaVp7MQfSYrRZ584vSbedKCAdRk%2FZp1ui3HUVcJax%2Bae8BjA%2B9Jw9BvllNyzotv1f9vRDw%3D%3D&SigAlg=http%3A%2F%2Fwww.w3.org%2F2000%2F09%2Fxmldsig%23rsa-sha1&Signature=kSA8%2F5TOUUpzyRe4fDJ1CKSwjEIc7aWBk5x2p%2FqVs%2BGD0ga%2FXndle3OAV2b6neZL9BqM0A0XTuOicMZip7ZcvOJKPDR5wFNGYXsVqbXlJBxiPibsxNATLPFcwCMlbaADrWOZNT6n%2B%2FkquOva2mLkU%2BodRgh282RtUj3ir1nRg31W9KOrfMKLGHOKncMgYFRFAu3U%2B%2FygQnlrbeZyY4cWDPdWgjGWbg1u56MVvSowT3r6s4tPO%2Bn6mfbbK99d7R%2Brx6h%2Bni3NGq2vV9nZxdqPa2DgHzcH0A%2F%2F%2Bx0ZPk2BLxtnpqAfdIYU5UAX3v4%2FSZW5uZJBTPM6slWCJiR0GR519g%3D%3D
		output = writer("INFO:\tSAML credentials request page.",output)
		self.driver.save_screenshot(shot_path+os.sep+"adminLoginSamlUser_"+now+"_003.png")
		try:
			usernameInput =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"ctl00_ContentPlaceHolder1_UsernameTextBox")))
			usernameInput.clear()                          #finding the login fields
			usernameInput.send_keys("Administrator")
			passwordInput =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"ctl00_ContentPlaceHolder1_PasswordTextBox")))
			passwordInput.clear()
			passwordInput.send_keys("a#w1^Nkmnni5@IS")
			self.driver.save_screenshot(shot_path+os.sep+"adminLoginSamlUser_"+now+"_004.png")
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"ctl00_ContentPlaceHolder1_SubmitButton"))).click()
			output = writer("INFO:\tSAML login submitted",output)
		except TimeoutException:
			output = writer("INFO:\tSAML login failed",output)
		#-------------------------
		global Build
		Build = get_buildno(self.driver)      #must pass self.driver to get_buildno()
		output = writer("BUILD:\t"+ Build,output)
		global buildPath
		buildPath = build_path_admin2_usqa(Build)
		#-------------------------
		#get around the welcome screen
		get_around_welcome_screen(self.driver)
		#--------------------------
		#Check page elements
		self.driver.save_screenshot(shot_path+os.sep+"adminLoginSamlUser_"+now+"_005.png")
		# Verify if NEWS menu option is available.
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:newsBtn")))
			output = writer("VERIFY:\tNEWS menu button is available.\tPASS",output)
			res["P"] += 1   #add  1 to pass counter"
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tNEWS menu button is available.\tFAIL",output)
		# Verify if TEAMS menu option is available.
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnTeams")))
			output = writer("VERIFY:\tTEAMS menu button is available.\tPASS",output)
			res["P"] += 1   #add  1 to pass counter"
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tTEAMS menu button is available.\tFAIL",output)
		# Verify if PEOPLE menu option is available.
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnPeople")))
			output = writer("VERIFY:\tPEOPLE menu button is available.\tPASS",output)
			res["P"] += 1   #add  1 to pass counter"
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tPEOPLE menu button is available.\tFAIL",output)
		# Verify if DISCUSSIONS menu option is available.
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnDiscussions")))
			output = writer("VERIFY:\tDISCUSSIIONS menu button is available.\tPASS",output)
			res["P"] += 1   #add  1 to pass counter"
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tDISCUSSIIONS menu button is available.\tFAIL",output)
		# Verify if LIBRARY menu option is available.
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:libraryBtn")))
			output = writer("VERIFY:\tLIBRARY menu button is available.\tPASS",output)
			res["P"] += 1   #add  1 to pass counter"
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tLIBRARY menu button is available.\tFAIL",output)
		# Verify if MORE menu option is available.
		try:
			WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:moreBtn")))
			output = writer("VERIFY:\tMORE menu button is available.\tPASS",output)
			res["P"] += 1   #add  1 to pass counter"
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tMORE menu button is available.\tFAIL",output)
		#-------------------------
		#Admin Gear test
		try:
			adminGearIcon = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))
			output = writer("VERIFY:\tAdmin Gear\tPASS",output)
			res["P"] += 1   #add  1 to pass counter
			self.driver.save_screenshot(shot_path+os.sep+"adminLoginSamlUser_"+now+"_006.png")
			adminGearIcon.click()
			output = writer("INFO:\tClick Admin Gear",output)
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tQA:RichClient:btnAdmin\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminLoginSamlUser_"+now+"_006.png")
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