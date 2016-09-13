# Create a News admin and verify capability as well as email sent

from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import NoSuchElementException   #exception for missing element
from selenium.common.exceptions import NoSuchFrameException     #exception for missing iframe
from selenium.common.exceptions import ElementNotVisibleException	#exception for elements in page not active
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.
from selenium.webdriver.common.action_chains import ActionChains
import unittest, os, time
#custom functions
from get_datetime import get_datetime   #date\time funtion that we use for file names
from get_buildno import get_buildno     #function to get build number
from get_around_welcome_screen import get_around_welcome_screen #function to bypass startup popup
from path_est import path_est           #function to open date folders for dumps
from build_path_admin2_usqa import build_path_admin2_usqa
from get_newfile import get_newfile     #function to get most recently created file in a folder
from writer import writer               #function to handle outputs
from execute_login import execute_login #function to perform login
from mailinatorApi import mailinatorApi	#for email checking

#necessary globals
prog = os.path.basename(__file__).split(".")[0]       #gets the name of the currently running program
now,date = get_datetime() 	            #get date and time string
output = []                             #empty list to append Test Outputs
res = {"P" : 0}	                        #initializing pass/fail counters
log_path,shot_path = path_est(date)
#------------------------------------------------
class adminCreateNewsAdmins(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(10)
		self.driver.maximize_window()
		self.password = "Ship1Stop2"
		self.initializer = "jasonjones_usqa@mailinator.com"
		self.logins = ["jimhalpert_usqa@mailinator.com","tobyflenderson_usqa@mailinator.com","ryanhoward_usqa@mailinator.com"]
		self.namesNews = ["Jim Halpert","Toby Flenderson","Ryan Howard"]
		self.total = 12*len(self.logins)
		self.driver.set_page_load_timeout(60)

	def test_create_news_admins(self):
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
	    #navigate to login with URL
		url = "https://usqa.jostle.us/jostle-prod/login.html"
		output = writer("URL:\t"+url,output)
		self.driver.get(url)    #navigate to login with URL
		start = time.time()
		output = writer("INFO:\tJostle Launched",output)
		try:
			username = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
			username.clear()                          #finding the login fields
			username.send_keys(self.initializer)
			password = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
			password.clear()
			password.send_keys(self.password)
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
		#---------------------------------------
		# Log Back in and start making News Admins
		for name,login in zip(self.namesNews,self.logins):
			for j in range(5):
				try:
					self.driver.get(url)    #navigate to login with URL
					output = writer("INFO:\tJostle Launched",output)
					username = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
					username.clear()                          #finding the login fields
					username.send_keys(self.initializer)
					password = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
					password.clear()
					password.send_keys(self.password)
					WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME,"saveAndSubmit"))).click()
					try:
						WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,"error-message")))
						continue
					except TimeoutException:
						pass
					output = writer("INFO:\tlogin submitted as "+name,output)
					#-------------------------
					#get around the welcome screen
					get_around_welcome_screen(self.driver)
					break
				except (NoSuchElementException, TimeoutException):
					pass
			#Admin Gear selection
			try:
				adminGearButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))
				output = writer("Verify:\tQA:RichClient:btnAdmin\tPASS",output)
				res["P"] += 1   #add  1 to pass counter
				adminGearButton.click()
				output = writer("INFO:\tClicked Admin Gear",output)
			except (NoSuchElementException, TimeoutException):
				output = writer("VERIFY:\tQA:RichClient:btnAdmin\tFAIL",output)
			#Frame switch
			try:
				WebDriverWait(self.driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"QA:AdminFrame")))
			except TimeoutException:
				output = writer("INFO:\tCouldn't switch to iframe",output)
			#Manage News Admin
			try:
				manageNewsAdmin = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:manageNewsAdmin")))
				output = writer("VERIFY:\tQA:manageNewsAdmin\tPASS",output)
				res["P"] += 1   #add  1 to pass counter
				manageNewsAdmin.click()
				output = writer("INFO:\tClicked manageNewsAdmin",output)
			except (NoSuchElementException, TimeoutException):
				output = writer("VERIFY:\tQA:manageNewsAdmin\tFAIL",output)
			#------------------------
			#Adding an admin, logging in to verify, back in as admin to delete
			try:
				searchText = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"searchText")))
				output = writer("VERIFY:\tsearchText\tPASS",output)
				searchText.clear()
				res["P"] += 1   #add 1 to pass counter
				searchText.send_keys(str(name))
				output = writer("INFO:\tsearchText inserted -\t"+str(name),output)
				searchButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"searchButton")))
				output = writer("VERIFY:\tSearchButton\tPASS",output)
				searchButton.click()
				output = writer("INFO:\tSearchButton clicked",output)
				res["P"] += 1   #add 1 to pass counter
			except (NoSuchElementException, TimeoutException):
				output = writer("VERIFY:\tSearch Box/Button\tFAIL",output)
			try:
				# self.driver.find_element_by_css_selector("img[alt=\"Add\"]").click()\
				contribCheckbox = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//input[contains(@id,'contributor')]")))
				output = writer("VERIFY:\tContributor checkbox\tPASS",output)
				contribCheckbox.click()
				res["P"] += 1   #add 1 to pass counter
				output = writer("INFO:\tContributor checkbox clicked",output)
				addAdminEditorButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"addAdminsButton")))
				output = writer("VERIFY:\t'Add as Editors' Button\tPASS",output)
				addAdminEditorButton.click()
				time.sleep(4)
				#-------------------------
				#verify if page was loaded
				try:
					WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located((By.ID,"loading")))
				except TimeoutException:
					output = writer("INFO:\tPage did not fully load.",output)
				output = writer("INFO:\tAdded "+name+" as a News Admin",output)
				res["P"] += 1   #add 1 to pass counter
			except (NoSuchElementException, TimeoutException):
				output = writer("VERIFY:\t'Add as Editors' Button\tFAIL",output)
				output = writer("INFO:\t Tried to click the 'Add as Editors'  button 5 times. SUPER FAIL")
			#----------------------------
			#log in to verify privileges
			for j in range(5):
				try:
					execute_login(self.driver,None,url,login,self.password,"none",shot_path,now,None,[])
					get_around_welcome_screen(self.driver)
					break
				except (NoSuchElementException, TimeoutException):
					pass
			else:
				output = writer("INFO:\tCouldn't Login as "+name,output)

			#-------------------------------
			#verifying News Admin Rights
			try:
				storiesButton =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:News:addNewStories")))
				output = writer("VERIFY:\tQA:News:newArticle\tPASS",output)
				ActionChains(self.driver).context_click(storiesButton).perform()
				WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:News:newArticle")))
				output = writer("INFO:\tVerified that "+name+" is a News Admin",output)
				res["P"] += 1   #add 1 to pass counter
			except (NoSuchElementException, TimeoutException):
				output = writer("VERIFY:\tQA:News:addNewStories\tFAIL",output)
				output = writer("INFO:\t"+name+" did NOT gain News Admin privileges",output)
			#--------------------------
			# deleting person as news admin
			for j in range(5):
				try:
					#time.sleep(1)
					execute_login(self.driver,None,url,self.initializer,self.password,"none",shot_path,now,None,[])
					get_around_welcome_screen(self.driver)
					break
				except (NoSuchElementException, TimeoutException):
					pass
			else:
				output = writer("INFO:\t"+self.initializer+" Login Failed",output)

			try:
				adminGearButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))
				output = writer("Verify:\tQA:RichClient:btnAdmin\tPASS",output)
				adminGearButton.click()
				output = writer("INFO:\tClicked Admin Gear",output)
				res["P"] += 1   #add 1 to pass counter
			except (NoSuchElementException, TimeoutException):
				output = writer("VERIFY:\tQA:RichClient:btnAdmin\tFAIL",output)
			#-------------------------
			#Frame switch
			try:
				WebDriverWait(self.driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"QA:AdminFrame")))
				output = writer("INFO:\tSuccessfully switched to iframe",output)
			except TimeoutException:
				output = writer("INFO:\tCouldn't switch to iframe",output)
			#-------------------------
			#Manage News Admin
			try:
				manageNewsAddminButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:manageNewsAdmin")))
				output = writer("Verify:\tQA:manageNewsAdmin\tPASS",output)
				manageNewsAddminButton.click()
				output = writer("INFO:\tClicked manageNewsAdmin",output)
				res["P"] += 1   #add 1 to pass counter
			except (NoSuchElementException, TimeoutException):
				output = writer("INFO:\tQA:manageNewsAdmin didn't work",output)
			#-------------------------
			#finding the little red "x for the person i just added
			try:
				allX = WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located((By.ID,"incomplete-links"))) #list of webelements
				allXtext = [element.text for element in allX]   #list of text for the webelements
				email  = login
				for text in allXtext:
					if email == text:
						loc = allXtext.index(text)
						X = WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"span.delete-item")))
						output = writer("VERIFY\tLittle Red 'x' for "+name+"\tPASS",output)
						correct_x = X[loc]
						correct_x.click()
						output = writer("INFO\tClicked Little Red 'x' for "+name,output)
						#-------------------------------
						#verify if page was loaded
						try:
							WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located((By.ID,"loading")))
						except TimeoutException:
							output = wrirter("FATAL:\tPage did not fully load.",output)
						res["P"] += 1   #add 1 to pass counter
						break
					else: pass
				else:
					output = writer("VERIFY\tLittle Red 'x' for "+name+"\tFAIL",output)
					output = writer("INFO:\tNo X Present for "+name,output)
			except (NoSuchElementException, TimeoutException):
				output = writer("INFO\tCouldn't find any Little Red x's ",output)
    		#----------------------------
			#log in to verify privileges have been removed
			for j in range(5):
				try:
					execute_login(self.driver,None,url,login,self.password,"none",shot_path,now,None,[])
					get_around_welcome_screen(self.driver)
					break
				except (NoSuchElementException, TimeoutException):
					pass
			else:
				output = writer("INFO:\tCouldn't Login as "+name,output)

			#-------------------------------
			#verifying News Admin Rights are absent
			try:
				output = writer("INFO:\tLooking for News Admin stuff",output)
				storiesButton = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,"QA:News:addNewStories")))
				ActionChains(self.driver).context_click(storiesButton).perform()
				WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID,"QA:News:newArticle")))
				output = writer("VERIFY:\tQA:News:addNewStories Absent\tFAIL",output)
				output = writer("INFO:\t"+name+" is STILL a News Admin",output)
			except (NoSuchElementException,ElementNotVisibleException,TimeoutException):
				output = writer("VERIFY:\tQA:News:addNewStories Absent\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
				output = writer("INFO:\t"+name+" has lost News Admin privileges",output)
			#-------------------------------
			#checking emails were sent
			subject = name.split(" ")[0] + ", you have just been made a NEWS Editor in ApplesRus"
			checkEmails  = mailinatorApi()
			checkEmails.emailVerification(login, subject, end=now, emailSent=True)
			for log in checkEmails.output:
				output.append(log)
			res["P"] += checkEmails.counter
			#go back to the top of the loop and make another admin

		#---------------------------------------------------------------
		end = time.time()
		elapsed = end - start
		output = writer("start:\t"+str(start)+"\tend\t"+str(end)+"\telapsed\t"+str(elapsed),output)

		output = writer("INFO:\ttestResultCount:\t"+str(res["P"])+"\t/\t"+str(self.total),output)
		output = writer("INFO:\tTEST\tRESULT\tTIME\tBUILD",output)

	def tearDown(self):
		global output
		if res["P"] == self.total:
			f = open(log_path+os.sep+prog+"_"+now+"_PASS.log",'w')
			g = open(buildPath+os.sep+prog+"_PASS.log",'w')
			output = writer("RESULTS:\t"+prog+"\tPASS\t"+str(elapsed)[0:-8],output)
			f.writelines(output)
			g.writelines(output)
		else:
			f = open(log_path+os.sep+prog+"_"+now+"_FAIL.log",'w')
			g = open(buildPath+os.sep+prog+"_FAIL.log",'w')
			output = writer("RESULTS:\t"+prog+"\tFAIL\t"+str(elapsed)[0:-8],output)
			f.writelines(output)
			g.writelines(output)
		f.close()
		g.close()
		self.driver.quit()                      #closes the webdriver


if __name__ == "__main__":
	 unittest.main()