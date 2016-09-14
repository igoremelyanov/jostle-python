# Create a Teams admin and verify capability as well as email sent

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
from mailinatorApi import mailinatorApi	#for email checking

#necessary globals
prog = os.path.basename(__file__).split(".")[0]      #gets the name of the currently running program
now,date = get_datetime() 	            #get date and time string
output = []                             #empty list to append Test Outputs
res = {"P" : 0}	                        #initializing pass/fail counters
log_path,shot_path = path_est(date)
#------------------------------------------------
class adminCreateTeamsAdmins(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(15)
		self.driver.maximize_window()
		self.password = "Ship1Stop2"
		self.initializer = "jasonjones_usqa@mailinator.com"
		self.logins = ["jimhalpert_usqa@mailinator.com","michaelgaryscott_usqa@mailinator.com"]
		self.namesTeams = ["Jim Halpert","Michael Scott"]
		self.total = 15*len(self.logins)
		self.driver.set_page_load_timeout(60)

	def test_create_teams_admins(self):
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
			usernameInput =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
			usernameInput.clear()                          #finding the login fields
			usernameInput.send_keys(self.initializer)
			password =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
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
		# Log Back in and start making Teams Admins
		for name,login in zip(self.namesTeams,self.logins):
			for j in range(5):
				try:
					self.driver.get(url)    #navigate to login with URL
					usernameInput =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
					usernameInput.clear()                          #finding the login fields
					usernameInput.send_keys(self.initializer)
					password =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
					password.clear()
					password.send_keys(self.password)
					WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME,"saveAndSubmit"))).click()
					try:
						WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,"error-message")))
						continue
					except TimeoutException:
						pass
					output = writer("INFO:\tJostle Launched",output)
					output = writer("INFO:\tlogin submitted as "+self.initializer,output)
					#-------------------------
					#get around the welcome screen
					get_around_welcome_screen(self.driver)
					break
				except TimeoutException:
					pass
			#Admin Gear Test
			try:
				adminGear = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))
				output = writer("Verify:\tQA:RichClient:btnAdmin\tPASS",output)
				res["P"] += 1   #add  1 to pass counter
				adminGear.click()
				output = writer("INFO:\tClicked Admin Gear",output)
			except (NoSuchElementException, TimeoutException):
				output = writer("VERIFY:\tQA:RichClient:btnAdmin\tFAIL",output)
			#Frame switch
			try:
				WebDriverWait(self.driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"QA:AdminFrame")))
				output = writer("INFO:\tSuccessfully switched to iframe",output)
			except TimeoutException:
				output = writer("INFO:\tCouldn't switch to iframe",output)
			#Manage Teams Admin
			try:
				manageTeamsAdmin = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:manageRelationshipAdmin")))
				output = writer("VERIFY:\tQA:manageRelationshipAdmin\tPASS",output)
				res["P"] += 1   #add  1 to pass counter
				manageTeamsAdmin.click()
				output = writer("INFO:\tClicked manageRelationshipAdmin",output)
			except (NoSuchElementException, TimeoutException):
				output = writer("VERIFY:\tQA:manageRelationshipAdmin\tFAIL",output)
			#------------------------
			#Adding an admin, logging in to verify, back in as admin to delete
			try:
				searchText = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"searchText")))
				searchText.clear()
				output = writer("VERIFY:\tsearchText\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
				searchText.send_keys(str(name))
				searchButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"searchButton")))
				searchButton.click()
				output = writer("VERIFY:\tSearchButton\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
			except (NoSuchElementException, TimeoutException):
				output = writer("VERIFY:\tSearch Box/Button\tFAIL",output)
			try:
				greenButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"img[alt=\"Add\"]")))
				output = writer("VERIFY:\tGreen Add Button\tPASS",output)
				greenButton.click()
				output = writer("INFO:\tAdded "+name+" as a Teams Admin",output)
				res["P"] += 1   #add 1 to pass counter
			except (NoSuchElementException, TimeoutException):
				output = writer("VERIFY:\tGreen Add Button\tFAIL",output)
				output = writer("INFO:\t Tried to click the green button 5 times. SUPER FAIL",output)
			#----------------------------
			#log in to verify privileges
			for j in range(5):
				try:
   					self.driver.get(url)    #navigate to login with URL
					output = writer("INFO:\tJostle Launched",output)
					usernameInput = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
					usernameInput.clear()	#finding the login fields
					usernameInput.send_keys(login)
					password = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
					password.clear()
					password.send_keys(self.password)
					WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME,"saveAndSubmit"))).click()
					try:
						WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,"error-message")))
						continue
					except TimeoutException:
						pass
					output = writer("INFO:\tLogged in as "+name,output)
					#-------------------------
					#get around the welcome screen
					get_around_welcome_screen(self.driver)
					break
				except TimeoutException:
					pass
			else:
				output = writer("INFO:\tCouldn't Login as "+name,output)
			#-------------------------------
			#Going to Teams View
			for i in range(5):
				try:
					teamsButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnTeams")))
					output = writer("VERIFY:\tQA:RichClient:btnTeams\tPASS",output)
					teamsButton.click()
					output = writer("INFO:\tClicked TEAMS view button",output)
					res["P"] += 1   #add 1 to pass counter
				except (NoSuchElementException, TimeoutException):
					output = writer("VERIFY:\tQA:RichClient:btnTeams\tFAIL",output)
				try:
					WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:CentricView:emailTeamButton")))
					break
				except TimeoutException:
					output = writer("INFO: Page does not appear to be fully load",output)
			#-------------------------------
			#verifying Teams Admin Rights
			try:
				cardDecorator = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:CentricView:primarySupCG")))
				output = writer("VERIFY:\tTop Card Present\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
				cardDecorator.click()
				output = writer("INFO:\tTop Card Click\tPASS",output)
				try:
					time.sleep(2)#Wait card selection effect to complete
					WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:CentricView:editButton")))
					output = writer("VERIFY:\tQA:CentricView:editButton\tPASS",output)
					output = writer("INFO:\tVerified that "+name+" is a Teams Admin",output)
					res["P"] += 1   #add 1 to pass counter
				except (NoSuchElementException, TimeoutException):
					output = writer("VERIFY:\tQA:CentricView:editButton\tFAIL",output)
					output = writer("INFO:\t"+name+" did NOT gain Teams Admin privileges",output)
			except (NoSuchElementException, TimeoutException):
				output = writer("VERIFY:\tTop Card Present\tFAIL",output)
				output = writer("INFO:\tCrazy Team View ERROR",output)

			#--------------------------
			# deleting person as Teams admin
			for j in range(5):
				try:
					self.driver.get(url)    #navigate to login with URL
					usernameInput =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
					usernameInput.clear()                          #finding the login fields
					usernameInput.send_keys(self.initializer)
					password =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
					password.clear()
					password.send_keys(self.password)
					WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME,"saveAndSubmit"))).click()
					try:
						WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,"error-message")))
						continue
					except TimeoutException:
						pass
					output = writer("INFO:\tJostle Launched",output)
					output = writer("INFO:\tJason Jones Logged in",output)
					#-------------------------
					#get around the welcome screen
					get_around_welcome_screen(self.driver)
					break
				except TimeoutException:
					pass
			else:
				output = writer("INFO:\tjasonjones Login Failed",output)

			try:
				adminGear = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))
				output = writer("VERIFY:\tAdmin Gear found\tPASS",output)
				adminGear.click()
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
			#Manage Teams Admin
			try:
				manageTeamsAdmin = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:manageRelationshipAdmin")))
				output = writer("VERIFY:\tQA:manageRelationshipAdmin is present\tPASS",output)
				manageTeamsAdmin.click()
				output = writer("INFO:\tClicked manageRelationshipAdmin",output)
				res["P"] += 1   #add 1 to pass counter
			except TimeoutException:
				output = writer("INFO:\tQA:manageRelationshipAdmin didn't work",output)
			#-------------------------
			#finding the little red "x for the person i just added
			try:
				allX = WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located((By.ID,"incomplete-links"))) #list of webelements
				allXtext = [element.text for element in allX][1:]   #list of text for the webelements
				# email = login.replace("@mailinator.com","@qa-email.jostletest.com")
				# email = login.replace("@mailinator.com","@jostletest1.mailgun.org")
				email = login
				for text in allXtext:
					if email == text:
						loc = allXtext.index(text)
						X = WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"delete-item")))
						output = writer("VERIFY\tLittle Red 'x' for "+name+"\tPASS",output)
						correct_x = X[loc]
						correct_x.click()
						output = writer("INFO\tClicked Little Red 'x' for "+name,output)
						#----------------------------
						#verify if page was loaded
						try:
							WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located((By.ID,"loading")))
						except TimeoutException:
							output = writer("INFO:\tPage did not load at all.",output)
						time.sleep(1)#Wait extra time to ensure page load.
						output = writer("INFO:\tPage loaded after user added as TEAMS Admin",output)
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
   					self.driver.get(url)    #navigate to login with URL
					output = writer("INFO:\tJostle Launched",output)
					usernameInput =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
					usernameInput.clear()                          #finding the login fields
					usernameInput.send_keys(login)
					password =  WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
					password.clear()
					password.send_keys(self.password)
					WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME,"saveAndSubmit"))).click()
					try:
						WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,"error-message")))
						continue
					except TimeoutException:
						pass
					output = writer("INFO:\tLogged in as "+name+" again",output)
					#-------------------------
					#get around the welcome screen
					get_around_welcome_screen(self.driver)
					break
				except (NoSuchElementException, TimeoutException):
					pass
			else:
				output = writer("INFO:\tCouldn't Login as "+name,output)
			#------------------------------
			#Going to Teams View
			for i in range(5):
				try:
					teamsButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnTeams")))
					output = writer("VERIFY:\tQA:RichClient:btnTeams\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
					teamsButton.click()
					output = writer("INFO:\tClicked TEAMS view button",output)
				except (NoSuchElementException, TimeoutException):
					output = writer("VERIFY:\tQA:RichClient:btnTeams\tFAIL",output)
				try:				
					WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:CentricView:emailTeamButton")))
					break
				except TimeoutException:
					output = writer("INFO: Page does not appear to be fully load",output)
					res["P"] -= 1   #remove 1 to pass counter
			#-------------------------------
			#verifying Teams Admin Rights are absent
			try:
				cardDecorator = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:CentricView:primarySupCG")))
				output = writer("VERIFY:\tTop Card Present\tPASS",output)
				cardDecorator.click()
				output = writer("INFO:\tTop Card Click\tPASS",output)
				res["P"] += 1   #add 1 to pass counter
				try:
					output = writer("INFO:\tLooking for Teams Admin stuff",output)
					time.sleep(2)#Wait card selection effect to complete
					editButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:CentricView:editButton")))
					if editButton.is_displayed() != True:
						output = writer("VERIFY:\tQA:CentricView:editButton Absent\tPASS",output)
						output = writer("INFO:\t"+name+" is no longer a Teams Admin",output)
						res["P"] += 1   #add 1 to pass counter
					else:
						output = writer("VERIFY:\tQA:CentricView:editButton Absent\tFAIL",output)
						output = writer("INFO:\t"+name+" is STILL a Teams Admin",output)
				except (NoSuchElementException, TimeoutException):
					output = writer("VERIFY:\tQA:CentricView:editButton Absent\tPASS",output)
					res["P"] += 1   #add 1 to pass counter
					output = writer("INFO:\t"+name+" has lost Teams Admin privileges",output)
			except (NoSuchElementException, TimeoutException):
				output = writer("VERIFY:\tTop Card Present\tFAIL",output)
				output = writer("INFO:\tCrazy Team View ERROR",output)

			#-------------------------------
			#checking emails were sent
			subject = name.split(" ")[0] + ", you have just been made a TEAMS Administrator in ApplesRus"
			checkEmails  = mailinatorApi()
			checkEmails.emailVerification(login, subject, end=now, emailSent=True)
			for log in checkEmails.output:
				output.append(log)
			res["P"] += checkEmails.counter
			#go back to the top of the loop and make another admin

		#---------------------------------------------------------------	
		end = time.time()
		elapsed = end - start
		output = writer("INFO:\ttestResultCount:\t"+str(res["P"])+"\t/\t"+str(self.total),output)
		output = writer("INFO:\tTEST\tRESULT\tTIME\tBUILD",output)

	def tearDown(self):
		global output
		if res["P"] == self.total:
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
