from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.
import unittest, os, time
from writer import writer               #function to handle outputs

#custom functions
from googleOrgTests.server_credentials import server_credentials	#function to load server specific properties

output = []                             #empty list to append Test Outputs
res = {"P" : 0, "LP" : 0}	                        #initializing pass/fail counters
def googleAppRemove(self, output, res):
	#-------------------------
	# Authentication to Google
	try:
		emailInput = WebDriverWait(self.driver,15).until(EC.element_to_be_clickable((By.ID,"Email")))
		output = writer("VERIFY:\tEmail input found.\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		emailInput.clear()
		output = writer("INFO:\tEmail input cleared.", output)
		emailInput.send_keys(self.googleInfo['user'])
		output = writer("INFO:\tInserted "+self.googleInfo['user']+" as E-mail to be used.", output)
		nextButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, "next")))
		output = writer("VERIFY:\tNext button is Present.\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		nextButton.click()
		output = writer("INFO:\tNext button clicked.", output)
	except TimeoutException:
		output = writer("Verify:\tE-mail input or next button found.\tFAIL", output)
		output = writer("ERROR:\tCheck your Internet connection.\tABORTING!", output)
		self.fail("ABORT:\tUnable to start test procedure")

	try:
		passwordInput = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID,"Passwd")))
		output = writer("VERIFY:\tPassword Input box found.\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		passwordInput.clear()
		output = writer("INFO:\tPassword input cleared.", output)
		passwordInput.send_keys(self.googleInfo['password'])
		output = writer("INFO:\tInserted password in password input field.", output)
		signInButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, "signIn")))
		output = writer("VERIFY:\t'Sign in' button found.\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		signInButton.click()
		output = writer("INFO:\t'Sign in' button clicked.", output)
	except TimeoutException:
		output = writer("VERIFY:\tPassword Input box found or 'Sign in' button found.\tFAIL", output)
	
	#-------------------------
	# Verify if Google user mais is fully load
	try: 
		# If all major Google mail  left-panel options are clickable, login to e-mail was successful.
		WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(@title,'Inbox')]")))
		#WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(@title,'Important')]")))
		WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(@title,'Sent Mail')]")))
		output = writer("VERIFY:\t'Google mail was loaded successfully.\tPASS",output)
		res["P"] += 1	#add 1 to pass counter
	except TimeoutException:
		output = writer("VERIFY:\t'Google mail was loaded successfully.\tFAIL",output)
	
	res["LP"] = 0	#reset loop pass counter
	#-------------------------
	# Try switch to the 'Remove APP' iframe for 5 times
	for i in range(5):
		res["P"] -= res["LP"]	#add 1 to pass counter
		#-------------------------
		#Go to Google Apps Manage iframe
		adminConsoleURL = "https://admin.google.com/AdminHome"
		self.driver.get(adminConsoleURL)    #navigate to Google marketplace URL
		output = writer("INFO:\tNavigated to Google Admin Console URL", output)

		#-------------------------
		#Clicked on Apps
		try:
			WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, "//*[text()='Loading...']")))
			appsButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Apps']/..")))
			output = writer("VERIFY:\tFound APPs menu\tPASS", output)
			res["P"] += 1	#add 1 to pass counter
			res["LP"] += 1	#add 1 to loop pass counter
			appsButton.click()
			output = writer("INFO:\tFound APPs menu clicked", output)
		except TimeoutException:
			output = writer("VERIFY:\tFound APPs menu\tFAIL", output)
			continue
			
		#-------------------------
		#Clicked on MarkPlace Apps
		try:
			WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, "//*[text()='Loading...']")))
			appsButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Marketplace apps']")))
			output = writer("VERIFY:\tFound Marketplace APPs menu\tPASS", output)
			res["P"] += 1	#add 1 to pass counter
			res["LP"] += 1	#add 1 to loop pass counter
			appsButton.click()
			output = writer("INFO:\tFound Marketplace APPs menu clicked", output)
		except TimeoutException:
			output = writer("VERIFY:\tFound Marketplace APPs menu\tFAIL", output)	
			continue

		#-------------------------
		# Click on Jostle USQA
		try:
			WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, "//*[text()='Loading...']")))
			settingsDiv = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//a[text()='Jostle USQA']")))
			output = writer("VERIFY:\tJostle USQA div found\tPASS", output)
			res["P"] += 1	#add 1 to pass counter
			res["LP"] += 1	#add 1 to loop pass counter
			settingsDiv.click()
			output = writer("INFO:\tJostle USQA div clicked", output)
		except TimeoutException:
			output = writer("VERIFY:\tJostle USQA div found\tFAIL", output)

		#-------------------------
		# Click on trash icon
		try:
			WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, "//*[text()='Loading...']")))
			trashIcon = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='Remove App']")))
			output = writer("VERIFY:\tTrash icon found\tPASS", output)
			res["P"] += 1	#add 1 to pass counter
			res["LP"] += 1	#add 1 to loop pass counter
			trashIcon.click()
			output = writer("INFO:\tTrash icon clicked", output)		
		except TimeoutException:
			output = writer("VERIFY:\tTrash icon found\tFAIL", output)
			continue

		#-------------------------
		# Confirm removal Popup
		try:
			WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, "//*[text()='Loading...']")))
			removeAppButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//div[text()='Remove App']")))
			output = writer("VERIFY:\tPopup confirmation button found\tPASS", output)
			res["P"] += 1	#add 1 to pass counter
			res["LP"] += 1	#add 1 to loop pass counter
			removeAppButton.click()
			output = writer("INFO:\tPopup confirmation button clicked", output)		
		except TimeoutException:
			output = writer("VERIFY:\tPopup confirmation button found\tFAIL", output)
			continue
		break

		#-------------------------
		# Confirm removal
		try:
			WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, "//*[text()='Loading...']")))
			removeAppButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//div[text()='No services have been installed.']")))
			output = writer("VERIFY:\tConfirmation message found\tPASS", output)
			res["P"] += 1	#add 1 to pass counter
			res["LP"] += 1	#add 1 to loop pass counter
		except TimeoutException:
			output = writer("VERIFY:\tConfirmation message found\tFAIL", output)
			continue
		break
	else:
		self.fail("FATAL:\tProblems in Google Marketplace: unable to install APP")
	

if __name__ == "__main__":
	
	class A:
		# Init.
		def __init__(self, value):
			self.__value = value
	A.driver = webdriver.Firefox()
	# Entering google mail as Google User - must be user0
	A.servername = "usqa"
	server_credentials(A, A.servername)
	url = A.googleInfo['googleMailUrl']
	output = writer("URL:\t"+url,output)
	A.driver.get(url)    #navigate to login with URL
	googleAppRemove(A, output, res)