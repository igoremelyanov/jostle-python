from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.
import unittest, os, time
from writer import writer               #function to handle outputs

def googleAppsManage(self, output, res):
	#-------------------------
	# Configure 3 of 3: Additional setup
	try:
		launchButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Manage app']/..")))
		output = writer("VERIFY:\tManage app link found\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		launchButton.click()
		output = writer("INFO:\tManage app link clicked", output)
	except TimeoutException:
		output = writer("VERIFY:\tUnable to launch manage app\tFAIL", output)
	
	#-------------------------
	# Switching window for the Jostle App Settings in Google Marketplace
	try:
		#-------------------------
		# Get window handles and swith to remaining window as initial popup closes
		handles = self.driver.window_handles # handles[0]: parent - handles[1]: child

		#-------------------------
		# Ensures that the inital popup closed
		while len(handles) < 2:
			handles = self.driver.window_handles # handles[0]: parent - handles[1]: child
			print str(len(handles))

		self.driver.switch_to_window(handles[1]) # switching to Google Marketplace window
		WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH,"//div[@text()='Marketplace apps']")))
		output = writer("INFO:\tSwitch to Google Marketplace window",output)
	except TimeoutException:
		output = writer("INFO:\tCouldn't switch to Google Marketplace window",output)
	#-------------------------
	# Click on Settings
	try:
		settingsDiv = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//div[text()='Settings']/..")))
		output = writer("VERIFY:\tSettings div found\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		settingsDiv.click()
		output = writer("INFO:\tSettings div clicked", output)
	except TimeoutException:
		output = writer("VERIFY:\tSettings div found\tFAIL", output)

	#-------------------------
	# Go to Jostle USQA for setup
	try:
		setupLink = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//a[text()='Go to Jostle USQA for setup']/..")))
		output = writer("VERIFY:\tJostle Setup link found\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		setupLink.click()
		output = writer("INFO:\tJostle Setup link clicked", output)
	except TimeoutException:
		output = writer("VERIFY:\tJostle Setup link found\tFAIL", output)

	#-------------------------
	# Configuring server instance
	try:
		#-------------------------
		# Get  new window handles and switch to it
		handles = self.driver.window_handles # handles[0]: parent - handles[1]: child window

		# Ensures that the two windows are loaded by Selenium
		while len(handles) < 3:
			handles = self.driver.window_handles # handles[0]: parent - handles[1]: child
			print str(len(handles))+" handles "

		self.driver.switch_to_window(handles[2]) # switching to new window - Instance Configuration
		output = writer("INFO:\tSwitch to Server Instance Configuration window",output)

		hostOption = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//label[@for='"+self.servername.upper()+"']")))
		output = writer("VERIFY:\tOption "+ self.servername.upper()+" server instance\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		hostOption.click()
		output = writer("INFO:\tOption "+ self.servername.upper()+" server instance clicked", output)
		continueButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue']")))
		output = writer("VERIFY:\tContinue button\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		continueButton.click()
		output = writer("INFO:\tContinue button clicked", output)
	except TimeoutException:
		output = writer("VERIFY:\tCouldn't Configuring Jostle Server instance\tFAIL",output)
	
	#-------------------------
	# Keeping the master account
	try:
		continueButton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue']")))
		output = writer("VERIFY:\tContinue button for Master Account confirmation\tPASS", output)
		res["P"] += 1	#add 1 to pass counter
		continueButton.click()
		output = writer("INFO:\tContinue button clicked", output)
	except TimeoutException:
		output = writer("VERIFY:\tContinue button for Master Account confirmation\tFAIL", output)

	#-------------------------
	#Wait spinner for preparing server infrastructure
	try:
		WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located((By.ID, "spinner")))
		res["P"] += 1	#add 1 to pass counter
		output = writer("VERIFY:\tJostle server setup complete\tPASS", output)
	except TimeoutException:
		output = writer("VERIFY:\tJostle server setup complete\tFAIL", output)

	#-------------------------
	#Skip setup logo
	try:
		skipUploadLink = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='standard-links']/a")))
		output = writer("VERIFY:\tSkip logo upload link\tPASS",output)
		res["P"] += 1	#add 1 to pass counter
		skipUploadLink.click()
		output = writer("INFO:\tSkip logo upload link clicked",output)
	except TimeoutException:
		output = writer("VERIFY:\tSkip logo upload link\tFAIL",output)

	#-------------------------
	#Enable API access confirmation
	try:
		enablingDoneLink = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, "linkDiv")))
		output = writer("VERIFY:\tEnable API access done link\tPASS",output)
		res["P"] += 1	#add 1 to pass counter
		enablingDoneLink.click()
		output = writer("INFO:\tEnable API access done link clicked",output)
	except TimeoutException:
		output = writer("VERIFY:\tEnable API access done link\tFAIL",output)
	

if __name__ == "__main__":
	
	class A:
		# Init.
		def __init__(self, value):
			self.__value = value

	googleAppInstall(A, )