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
res = {"P" : 0}	  
def create_library_user(self, output, res):

	url = self.googleInfo['googleMailUrl']
	output = writer("URL:\t"+url,output)
	self.driver.get(url)    #navigate to login with URL
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
	
	#-------------------------
	url = "https://admin.google.com/AdminHome#UserList"
	output = writer("URL:\t"+url,output)
	self.driver.get(url)    #navigate to login with URL

	#-------------------------
	
if __name__ == "__main__":
	
	class A:
		# Init.
		def __init__(self, value):
			self.__value = value
	A.driver = webdriver.Firefox()
	server_credentials(A,"usqa")
	create_library_user(A, output, res)