from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.
import unittest, os, time
from writer import writer               #function to handle outputs


def googleAppInstall(self, output, res):
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
	#Frame switch to Google Apps Marketplace iframe
	marketPlaceURL = "https://chrome.google.com/webstore/detail/jostle-usqa-app/mfebknhodmheplhmdicpdmpeagjmodok"
	self.driver.get(marketPlaceURL)    #navigate to Google marketplace URL
	output = writer("INFO:\tNavigated to Google Marketplace URL", output)
	
	#-------------------------
	# Try switch to the 'INSTALL APP' iframe for 5 times
	for i in range(5):
		try:
			WebDriverWait(self.driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//div[@id='___additnow_0']/iframe")))
			output = writer("INFO:\tSwitch to iframe",output)
		except TimeoutException:
			output = writer("INFO:\tCouldn't switch to iframe",output)
		output = writer("Try "+str(i+1), output)
		try:
			installAppButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, "aincontent")))	# INSTALL APP button
			output = writer("VERIFY:\tFound INSTALL APP button\tPASS", output)
			res["P"] += 1	#add 1 to pass counter
			installAppButton.click()
			output = writer("INFO:\tClicked on INSTALL APP button.", output)
			break
		except TimeoutException:
			output = writer("VERIFY:\tFound INSTALL APP button\tFAIL", output)					
	else:
		self.fail("FATAL:\tProblems in Google Marketplace: unable to install APP")

	#-------------------------
	# Accepting Google's Term of Service
	try:
		#-------------------------
		# Get window handles and swith to child window
		handles = self.driver.window_handles # handles[0]: parent - handles[1]: child
		
		# Ensures that the two windows are loaded by Selenium
		while len(handles) < 2:
			handles = self.driver.window_handles # handles[0]: parent - handles[1]: child

		self.driver.switch_to_window(handles[1]) # switching to child window - Terms of service confirmation screen
		output = writer("INFO:\tDisplayed the Terms of service confirmation screen", output)
		#-------------------------
		# Accept Term of Serivce
		serviceAggrCheckbox = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//div[@role='checkbox']"))) # only checkbox in the screen
		output = writer("VERIFY:\tTerms of service checkbox found\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		serviceAggrCheckbox.click()
		output = writer("INFO:\tClicked on Agree with Google's Term of Service", output)
		acceptButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".goog-buttonset-action.buttonRight"))) # Accept button CSS selector
		output = writer("VERIFY:\tAccept button found\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		acceptButton.click()
		output = writer("INFO:\tAccept button clicked", output)
	except TimeoutException:
		output = writer("VERIFY:\tTerms of service found\tFAIL", output)
	#-------------------------
	# Switching iFrame for the Jostle App Configuration procedure
	try:
		#-------------------------
		# Get window handles and swith to remaining window as initial popup closes
		handles = self.driver.window_handles # handles[0]: parent - handles[1]: child

		#-------------------------
		# Ensures that the inital popup closed
		while len(handles) > 1:
			handles = self.driver.window_handles # handles[0]: parent - handles[1]: child

		self.driver.switch_to_window(handles[0]) # switching to remaining window - Jostle App Configuration procedure
		WebDriverWait(self.driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//div[@id='glass-content']/iframe")))
		output = writer("INFO:\tSwitch to iframe for Configuring Jostle App",output)
	except TimeoutException:
		output = writer("INFO:\tCouldn't switch to iframe for Configuring Jostle App",output)

	#-------------------------
	# Configure 1 of 3: Notify your users
	try:
		notifyUsersSwitch = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//div[text()='on']")))
		output = writer("VERIFY:\tNotify users switch found\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		notifyUsersSwitch.click()
		output = writer("INFO:\tNotify users switch clicked", output)
		nextButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//div[text()='Next']")))
		output = writer("VERIFY:\tNext button found\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		nextButton.click()
		output = writer("INFO:\tNext button clicked", output)
	except TimeoutException:
		output = writer("VERIFY:\tUnable to configure 'Notify users'\tFAIL", output)

	#-------------------------
	# Configure 2 of 3: Where to find Jostle USQA
	try:
		nextButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//div[text()='Next']")))
		output = writer("VERIFY:\tNext button found\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		nextButton.click()
		output = writer("INFO:\tNext button clicked", output)
	except TimeoutException:
		output = writer("VERIFY:\tUnable to progress in '2 of 3: Where to find Jostle USQA'\tFAIL", output)
	

if __name__ == "__main__":
	
	class A:
		# Init.
		def __init__(self, value):
			self.__value = value

	googleAppInstall(A, output, res)