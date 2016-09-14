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
import zipfile
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
total = 5                                   #total number of tests
res = {"P" : 0}		                        #initializing pass/fail counters
log_path,shot_path = path_est(date)
# buildPath = build_path()
down_folder =  downloadLocation_path()#folder for dumping files downloaded during test
#------------------------------------------------
class adminExtractTEAMstructureToVisio(unittest.TestCase):

	def setUp(self):

		profile = webdriver.firefox.firefox_profile.FirefoxProfile()    #setting Firefox preferences
		profile.set_preference('browser.helperApps.neverAsk.saveToDisk','application/zip')# automatically saves downloads
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
		self.driver.save_screenshot(shot_path+os.sep+"adminExtractTEAMstructureToVisio_"+now+"_001.png")
		try:
			usernameInput =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
			usernameInput.clear()                          #finding the login fields
			usernameInput.send_keys("jasonjones_usqa@mailinator.com")
			password =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
			password.clear()
			password.send_keys("Ship1Stop2")
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractTEAMstructureToVisio_"+now+"_002.png")
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
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractTEAMstructureToVisio_"+now+"_003.png")
			adminGear.click()
			output = writer("INFO:\tClick Admin Gear",output)
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tQA:RichClient:btnAdmin\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractTEAMstructureToVisio_"+now+"_003.png")
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
			exportRelationshipsToVisio = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:exportRelationshipsToVisio")))
			output = writer("VERIFY:\tExport TEAM structure to Visio\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractTEAMstructureToVisio_"+now+"_004.png")
			exportRelationshipsToVisio.click()
			output = writer("INFO:\tClicked Export TEAM structure to Visio",output)
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tQA:exportRelationshipsToVisio\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractTEAMstructureToVisio_004_"+now+"_004.png")
		#---------------------------
		#UTF Encoding
		try:
			utf8Checkbox = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"utf8Encoding")))
			output = writer("VERIFY:\tUTF Encoding\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			utf8Checkbox.click()
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractTEAMstructureToVisio_"+now+"_005.png")
			output = writer("INFO:\tClicked UTF Encoding",output)
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tutf8Encoding\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractTEAMstructureToVisio_"+now+"_005.png")

		#----------------------------
		#Export TEAM structure To Visio Button
		try:
			downloadFile = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME,"downloadFile")))
			output = writer("VERIFY:\tDownload  Button\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractTEAMstructureToVisio_"+now+"_006.png")
			downloadFile.click()
			output = writer("INFO:\tClicked Download Button",output)
			stamp = True
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tDownload Button\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminExtractTEAMstructureToVisio_"+now+"_006.png")
			stamp = False
		#--------------------------
		if stamp:
			while True:
				try:
					new_download = get_newfile(down_folder,start)
					z = zipfile.ZipFile( new_download )
					output = writer("INFO:\tFile located",output)
					output = writer("INFO:\tFile name: "+new_download,output)
					hasJpg = False
					hasTxt = False
					for f in z.infolist():
						output = writer("INFO:\tFile in Zip:\t"+f.filename,output)
						if not hasJpg and  ".jpg" in f.filename:
							hasJpg = True
						if not hasTxt and ".txt" in f.filename:
							hasTxt = True
						if hasJpg and hasTxt:
							output = writer("VERIFY:\tZip file contain all expected content types\tPASS",output)
							res["P"] += 1   #add 1 to pass counter
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