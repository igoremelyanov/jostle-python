#function to get the build number from the Jostle platform
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.]


def get_around_welcome_screen(driver = None, timeout = None):
	"""
	   this is a function that is used to close any existing popup screens when user logs in.
	"""
	driver.implicitly_wait(0) #reset implicity wait. It is not need in here as there is only explicit wait.
	spinnerWait=30
	#timeoutValue = timeout if timeout != None else 1
	timeoutValue=1
	timeoutPopUp = 1
	if driver == None:
		print "ERROR in get_around_welcome_screen(): Please sent webdriver as argument. Timeout value is optional."
	else:
		#-------------------------
		#verify if link page was loaded
		try:
			WebDriverWait(driver, spinnerWait).until(EC.invisibility_of_element_located((By.ID,"loading")))
		except TimeoutException:
			print "FATAL:\tPage did not load at all."
			sys.exit("taking too long to load page")
		#-------------------------
		for x in range(0,3):
			#get around the welcome screen
			try:
				print "INFO:\tTrying to close Welcome popup"
				welcomePopupClose = WebDriverWait(driver,timeoutPopUp).until(EC.element_to_be_clickable((By.ID,"welcomePopupCloseButton")))
				welcomePopupClose.click()
				#driver.implicitly_wait(8)
				return None #abort function as pop is already closed.
			except TimeoutException:
				pass
			try:
				print "INFO:\tTrying to close New feature popup"
				newFeatPopupClose = WebDriverWait(driver,timeoutPopUp).until(EC.element_to_be_clickable((By.ID,"newFeaturePopupCloseButton")))
				newFeatPopupClose.click()
				#driver.implicitly_wait(8)
				return None #abort function as pop is already closed.
			except TimeoutException:
				pass
			try:
				print "INFO:\tTrying to close startJostlingNow"
				startJostlingPopupClose = WebDriverWait(driver,timeoutPopUp).until(EC.element_to_be_clickable((By.ID,"QA:startJostlingNow")))
				startJostlingPopupClose.click()
				#driver.implicitly_wait(5)
				return None #abort function as pop is already closed.
			except TimeoutException:
				pass
	return None