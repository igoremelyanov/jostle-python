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
total = 7                                   #total number of tests
res = {"P" : 0}		                        #initializing pass/fail counters
log_path,shot_path = path_est(date)
down_folder =  downloadLocation_path()#folder for dumping files downloaded during test
#------------------------------------------------
class adminExtractShouts(unittest.TestCase):

	def setUp(self):

		profile = webdriver.firefox.firefox_profile.FirefoxProfile()    #setting Firefox preferences
		profile.set_preference('browser.helperApps.neverAsk.saveToDisk','text/csv')# automatically saves downloads
		profile.set_preference("browser.download.folderList", 2)
		profile.set_preference('browser.download.dir', down_folder)
		self.driver = webdriver.Firefox(firefox_profile=profile)
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
		url = "https://usqa.jostle.us/jostle-prod/login.html"
		output = writer("URL:\t"+url,output)
		self.driver.get(url)    #navigate to login with URL
		start = time.time()
		output = writer("INFO:\tJostle Launched",output)
		self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_001.png")
		try:
			usernameInput =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
			usernameInput.clear()                          #finding the login fields
			usernameInput.send_keys("jasonjones_usqa@mailinator.com")
			password =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
			password.clear()
			password.send_keys("Ship1Stop2")
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_002.png")
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
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_003.png")
			adminGear.click()
			output = writer("INFO:\tClick Admin Gear",output)
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tQA:RichClient:btnAdmin\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_003.png")
		#-------------------------
		#Switch iframe
		try:
			WebDriverWait(self.driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"QA:AdminFrame")))
			output = writer("INFO:\tSuccessfully switched to iframe",output)
		except TimeoutException:
			output = writer("INFO:\tCouldn't switch to iframe",output)
		#-------------------------
		#Find Extract Manage Contributor Data
		try:
			exportShoutOuts = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:exportShoutOuts")))
			output = writer("VERIFY:\tExport Shout-Outs\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_004.png")
			exportShoutOuts.click()
			output = writer("INFO:\tClicked Export Shout-Outs",output)
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tQA:exportShoutOuts\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_004_"+now+"_004.png")
		#---------------------------
		#uUTF Encoding
		try:
			utf8Checkbox = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"utf8Encoding")))
			output = writer("VERIFY:\tUTF Encoding\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			utf8Checkbox.click()
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_005.png")
			output = writer("INFO:\tClicked UTF Encoding",output)
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tutf8Encoding\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_005.png")
		#----------------------------
		#Set date range - Starting Date
		try:
			sinceDate = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME,"sinceDate")))
			output = writer("VERIFY:\tFound Starting Date input\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_006.png")
			sinceDate.clear()
			sinceDate.send_keys("01/01/2015")
			output = writer("INFO:\tInsert the Starting Date in input",output)
			stamp = True
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tFound Starting Date input\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_006.png")
			stamp = False
		#----------------------------
		#Set date range - Ending Date
		try:
			untilDate = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME,"untilDate")))
			output = writer("VERIFY:\tFound Ending Date input\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_007.png")
			untilDate.clear()
			untilDate.send_keys("05/14/2015")
			output = writer("INFO:\tInsert the Ending Date in input",output)
			stamp = True
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tFound Ending Date input\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_007.png")
			stamp = False
		#----------------------------
		#Export Shout-Outs Button
		try:
			download = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME,"download")))
			output = writer("VERIFY:\tExport Shout-Outs Button\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_008.png")
			download.click()
			output = writer("INFO:\tClicked Export Shout-Outs Button",output)
			stamp = True
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tExport Shout-Outs Button\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractShouts_"+now+"_008.png")
			stamp = False
		#--------------------------
		if stamp:
			while True:
				try:
					new_download = get_newfile(down_folder,start)
					g = open(new_download,"r")
					header = g.readline()
					shoutOut = g.readline().split(",")[7]
					output = writer("INFO:\tFile located",output)
					output = writer("INFO:\tFile name: "+new_download,output)
					output = writer("INFO:\tContent to match:\t"+shoutOut,output)
		
					if shoutOut == "@Towlie TheTowel rocks":
						output = writer("VERIFY:\tFile Download and Read\tPASS",output)
						res["P"] += 1   #add 1 to pass counter
					else:
						output = writer("VERIFY:\tFile Download and Read\tFAIL",output)
					break
				except:pass
		else:pass
		end = time.time()
		elapsed = end - start
		output = writer("INFO:\ttestResultCount:\t"+str(res["P"])+"\t/\t"+str(total),output)
		output = writer("INFO:\tTEST\tRESULT\tTIME\tBUILD",output)
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