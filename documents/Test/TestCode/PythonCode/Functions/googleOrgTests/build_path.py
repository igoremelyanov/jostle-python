import os
from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.

from get_buildno import get_buildno
from pathToPythonCode import pathToPythonCode


def build_path(self,servername,is_started):
	# @self: variable with local variables for the test
	# @servername: name of the server (e.g. usqa, caqa)
	# @is_started: true if the already logged to server and only needs a build number to put in the path, otherwise start a new session

	# If Jostle session is not started, open a new session and get the buildNo.
	if is_started == False:
		driver = webdriver.Firefox()
		driver.implicitly_wait(0) #Using explicit wait, no need for implicit wait
		driver.get(self.serverInfo["loginUrl"])    #navigate to login with URL
		username = WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.ID,"username")))
		username.clear()                          #finding the login fields
		username.send_keys(self.serverInfo["initializer"])
		password = WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.ID,"password")))
		password.clear()
		password.send_keys(self.serverInfo["initializerPass"])
		WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.NAME,"saveAndSubmit"))).click()
		self.Build = get_buildno(driver)
		driver.quit()
	else:
		self.Build = get_buildno(self.driver) #only get buildNo from existing Jostle session

	path = pathToPythonCode()
	self.build_path = path+"logFiles"+os.sep+"googleAppsTest_"+servername+os.sep+"buildData"+os.sep+self.Build+os.sep
	if not os.path.exists(self.build_path):
		os.makedirs(self.build_path)

	return self.build_path

if __name__ == "__main__":

	class context:
		# Init.
		def __init__(self, value):
			self.__value = value
			
	context.serverInfo = {"initializer":"jasonjones_usqa@mailinator.com",
	"loginUrlloginloginllogi":"https://usqa.jostle.us/jostle-prod/login.html",
	"initializerPass":"Ship1Stop2"}

	#Test for session not initiated.
	build_path(context,"usqa",False)
	print context.build_path

	#Test for session initiated.
	context.driver = webdriver.Firefox()
	context.driver.implicitly_wait(0) #Using explicit wait, no need for implicit wait
	context.driver.get("https://caqa.jostle.us/jostle-prod/login.html")    #navigate to login with URL
	username = WebDriverWait(context.driver,15).until(EC.element_to_be_clickable((By.ID,"username")))
	username.clear()                          #finding the login fields
	username.send_keys("jasonjones@mailinator.com")
	password = WebDriverWait(context.driver,15).until(EC.element_to_be_clickable((By.ID,"password")))
	password.clear()
	password.send_keys(context.serverInfo["initializerPass"])
	WebDriverWait(context.driver,15).until(EC.element_to_be_clickable((By.NAME,"saveAndSubmit"))).click()

	#Call buildPath builder
	build_path(context,"caqa",True)
	print context.build_path

	context.driver.quit()



