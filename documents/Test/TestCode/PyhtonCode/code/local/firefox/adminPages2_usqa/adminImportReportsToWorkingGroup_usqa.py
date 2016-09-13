# Import Reports To Structure

from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import NoSuchElementException   #exception for missing element
from selenium.common.exceptions import NoSuchFrameException     #exception for missing iframe
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.
from selenium.webdriver.support.ui import Select                #for selecting from dropdown menus
from selenium.webdriver.common.keys import Keys
import unittest, os, time
#custom functions
from get_datetime import get_datetime   #date\time funtion that we use for file names
from get_buildno import get_buildno     #function to get build number
from get_around_welcome_screen import get_around_welcome_screen #function to bypass startup popup
from path_est import path_est           #function to open date folders for dumps
from build_path import build_path
from get_newfile import get_newfile     #function to get most recently created file in a folder
from writer import writer               #function to handle outputs
from execute_login import execute_login #function to perform login

#necessary globals
prog = os.path.basename(__file__).split(".")[0]      	#gets the name of the currently running program
now,date = get_datetime() 	                #get date and time string
output = []                                 #empty list to append Test Outputs
total = 11                                   #total number of tests
res = {"P" : 0}		                        #initializing pass/fail counters
log_path,shot_path = path_est(date)
buildPath = build_path()
#------------------------------------------------
class adminImportReportsToWorkingGroup_usqa(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(20)         	#sets a general time to wait for an element to be found.
		self.driver.maximize_window()
		self.driver.set_page_load_timeout(60)

	def test_import_reports_toWorkingGroup(self):
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
		start = execute_login(self.driver,None,url,"jasonjones_usqa@mailinator.com",None,"adminImportReportsToWorkingGroup",shot_path,now,None,output)
		#-------------------------
		global Build
		Build = get_buildno(self.driver)      #must pass self.driver to get_buildno()
		output = writer("BUILD:\t"+ Build,output)
		#-------------------------
		#get around the welcome screen
		get_around_welcome_screen(self.driver)
		#-------------------------
		#Admin Gear test

		try:
			adminGearButton = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))
			output = writer("VERIFY:\tQA:RichClient:btnAdmin\tPASS",output)
			res["P"] += 1   #add  1 to pass counter
			self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_003.png")
			adminGearButton.click()
			output = writer("INFO:\tClicked Admin Gear",output)
		except 	TimeoutException:
			output = writer("VERIFY:\tQA:RichClient:btnAdmin\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_003.png")
		#-------------------------
		#Switch iframe
		try:
			WebDriverWait(self.driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"QA:AdminFrame")))
			output = writer("INFO:\tSuccessfully switched to iframe",output)
		except TimeoutException:
			output = writer("INFO:\tCouldn't switch to iframe",output)
		#-------------------------
		# Import Reports To
		try:
			importReportsTo = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID,"QA:importReportsTo")))
			output = writer("VERIFY:\timportReportsTo\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_004.png")
			importReportsTo.click()
			output = writer("INFO:\tImportReports Clicked",output)
		except TimeoutException:
			output = writer("VERIFY:\tQA:importReportsTo\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_004.png")
		#---------------------------
		# Select Category
		try:

			categorySelection = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID,"category")))
			output = writer("VERIFY:\tSelect category dropbox\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			categorySelection.send_keys("WORKING GROUPS")
			output = writer("INFO:\tSelect category sent 'WORKING GROUPS'",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_005.png")
			time.sleep(3)
			self.driver.execute_script("updateSpaceList()")
		except TimeoutException:
			output = writer("VERIFY:\tSelect category dropbox\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_005.png")
		#---------------------------
		# UTF Encoding
		# try:
		# 	utf8Encoding = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID,"utf8Encoding")))
		# 	output = writer("VERIFY:\tutf8Encoding\tPASS",output)
		# 	res["P"] += 1   #add 1 to pass counter
		# 	utf8Encoding.click()
		# 	output = writer("INFO:\tutf8Encoding Click",output)
		# 	self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_005.png")
		# except (NoSuchElementException, TimeoutException):
		# 	output = writer("VERIFY:\tutf8Encoding\tFAIL",output)
		# 	self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_005.png")
		#----------------------------
		# CSV Input
		# Select Chart
		try:

			chartSelection = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID,"chart")))
			output = writer("VERIFY:\tSelect chart dropbox\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			time.sleep(3)
			chartSelection.send_keys("AUT REG - WORKING GROUP TEAM")
			output = writer("INFO:\tSelect chart sent 'AUT REG - WORKING GROUP TEAM'",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_006.png")
			# time.sleep(1)
			#self.driver.execute_script("updateSpaceList()")
		except TimeoutException:
			output = writer("VERIFY:\tSelect chart dropbox\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_006.png")

		try:
			csvInput = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.NAME,"csv")))
			output = writer("VERIFY:\tfileInput\tPASS",output)
			csvInput.send_keys(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../testfiles/jasonJonesOrg_usqa/jasonJonesOrgImportWorkingGroup1_usqa.csv")))
			self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_007.png")
			output = writer("INFO:\t.csv Submitted",output)
			res["P"] += 1   #add 1 to pass counter
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tfileInput\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_007.png")
		#--------------------------
		# Upload Button
		try:
			uploadButton = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[value=\'Upload\']")))
			output = writer("VERIFY:\tuploadButton\tPASS",output)
			uploadButton.click()
			output = writer("INFO:\tuploadButton click",output)
			res["P"] += 1   #add 1 to pass counter
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tuploadButton\tFAIL",output)
		#--------------------------
		# Accept alert box
		try:
			alert = WebDriverWait(self.driver, 30).until(EC.alert_is_present())
			# self.driver.switch_to_alert()
			alert.accept()
			stamp = True
		except (NoSuchElementException, TimeoutException):
			stamp = False
		#---------------------------
		#Select Drop down fields
		try:
			usernameField = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID,"usernameField")))
			output = writer("VERIFY:\tusernameField\tPASS",output)
			Select(usernameField).select_by_visible_text("Username")
			res["P"] += 1   #add 1 to pass counter
			output = writer("INFO:\tusernameField Entered",output)
			primarySupervisorUsernameField = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID,"supervisorUsernameField")))
			output = writer("VERIFY:\tprimarySupervisorUsernameField\tPASS",output)
			Select(primarySupervisorUsernameField).select_by_visible_text("Supervisor")
			res["P"] += 1   #add 1 to pass counter
			output = writer("INFO:\tprimarySupervisorUsernameField Entered",output)
			primaryRoleNameField = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID,"roleNameField")))
			output = writer("VERIFY:\tprimaryRoleNameField\tPASS",output)
			Select(primaryRoleNameField).select_by_visible_text("JobCategory")
			res["P"] += 1   #add 1 to pass counter
			output = writer("INFO:\tprimaryRoleNameField Entered",output)
			primaryTeamNameField = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID,"teamNameField")))
			output = writer("VERIFY:\tprimaryTeamNameField\tPASS",output)
			Select(primaryTeamNameField).select_by_visible_text("WorkMobilePhone")
			res["P"] += 1   #add 1 to pass counter
			output = writer("INFO:\tprimaryTeamNameField Entered",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_008.png")
			addButton = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.NAME,"add")))
			output = writer("VERIFY:\timportButton\tPASS",output)
			res["P"] += 1   #add 1 to pass counter
			addButton.click()
			output = writer("INFO:\timportButton Clicked",output)
		except (NoSuchElementException, TimeoutException):
			output = writer("VERIFY:\tImport Contributor Fields\tFAIL",output)
			self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_008.png")

		if stamp:
			output = writer("INFO:\tLooking for Success Result",output)
			while True:
				try:
					WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME,"success-result")))
					output = writer("VERIFY:\tSuccess Result\tPASS",output)              #the rest of this block is run only if the element is found
					output = writer("INFO:\t.csv Upload Successful",output)
					res["P"] += 1   #add 1 to pass counter
					self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_009.png")
					break
				except (NoSuchElementException, TimeoutException):
					pass
				try:
					WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME,"failure-result")))
					output = writer("VERIFY:\tSuccess Result\tFAIL",output)      #the rest of this block is run only if the element is not found
					output = writer("INFO:\t.csv Upload Unsuccessful",output)
					self.driver.save_screenshot(shot_path+os.sep+"adminImportReportsToWorkingGroup_"+now+"_009.png")
					break
				except (NoSuchElementException, TimeoutException):
					pass
			else:
				output = writer("VERIFY:\tLooking for Success Result\tFAIL",output)

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