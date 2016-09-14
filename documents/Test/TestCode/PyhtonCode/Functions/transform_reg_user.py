#function to get the build number from the Jostle platform
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.]
from writer import writer               #function to handle outputs
from get_around_welcome_screen import get_around_welcome_screen #function to bypass startup popup
import time,os

def transform_reg_user(driver=None,jostlegun=False,loginToTest=None,name=None,output=None):
	"""
	   this is a function is used to verify if user is regular user, MUST BE called after loginToTest with administrator and dismissal of the the welcome popup.
		@param driver: instance of the selenium webdriver being used by the test that called this function.
		@param jostlegun: true | false for use of jostlegun
		@param loginToTest: e-mail of the user that should be regular user.
		@param name: name of the user that should be regular user.
		@param output: variable for the log buffer used by the test.
	"""
	output = writer("-"*50,output)
	output = writer("INFO: Checking and transforming in regular user ",output)
	try:
		adminGear = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))
		output = writer("VERIFY:\tAdmin Gear present",output)
		adminGear.click()
		output = writer("INFO:\tClicked Admin Gear",output)
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:RichClient:btnAdmin",output)
	#-------------------------
	#Frame switch
	try:
		WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"QA:AdminFrame")))
		output = writer("INFO:\tSuccessfully switched to iframe",output)
	except TimeoutException:
		output = writer("INFO:\tCouldn't switch to iframe",output)
	#-------------------------
	#Manage News Admin
	try:
		manageSystemAdmin = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:manageSystemAdmin")))
		output = writer("VERIFY:\tQA:manageSystemAdmin present",output)
		manageSystemAdmin.click()
		output = writer("INFO:\tClicked manageSystemAdmin",output)
	except (NoSuchElementException, TimeoutException):
		output = writer("INFO:\tQA:manageSystemAdmin didn't work",output)
	#finding the little red "x for the person i just added
	try:
		allX = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID,"incomplete-links"))) #list of webelements
		allXtext = [element.text for element in allX]   #list of text for the webelements
		email = loginToTest
		if jostlegun == True:
			email = loginToTest.replace("@mailinator.com","@jostletest1.mailgun.org")
		for text in allXtext:
			if email == text:
				loc = allXtext.index(text)
				X = driver.find_elements_by_css_selector("span.delete-item")
				correct_x = X[loc]
				correct_x.click()
				output = writer("VERIFY\tLittle Red 'x' for "+name,output)
				output = writer("INFO\tClicked Little Red 'x' for "+name,output)
				time.sleep(1)
				break
			else: pass
		else:
			output = writer("VERIFY\tLittle Red 'x' for "+name,output)
			output = writer("INFO:\tNo X Present for "+name,output)
	except (NoSuchElementException, TimeoutException):
		output = writer("INFO\tCouldn't find any Little Red x's ",output)

	#-------------------------
	driver.switch_to.default_content()
	#-------------------------
	try:
		adminGearButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))
		output = writer("Verify:\tQA:RichClient:btnAdmin\tOK",output)
		adminGearButton.click()
		output = writer("INFO:\tClicked Admin Gear",output)
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:RichClient:btnAdmin\tSKIPPED",output)
	#-------------------------
	#Frame switch
	try:
		WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"QA:AdminFrame")))
		output = writer("INFO:\tSuccessfully switched to iframe",output)
	except TimeoutException:
		output = writer("INFO:\tCouldn't switch to iframe",output)
	#-------------------------
	#Manage News Admin
	try:
		manageNewsAddminButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:manageNewsAdmin")))
		output = writer("Verify:\tQA:manageNewsAdmin\tOK",output)
		manageNewsAddminButton.click()
		output = writer("INFO:\tClicked manageNewsAdmin",output)
	except (NoSuchElementException, TimeoutException):
		output = writer("INFO:\tQA:manageNewsAdmin didn't work",output)
	#-------------------------
	#verify if page was loaded
	try:
		WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.ID,"loading")))
	except TimeoutException:
		output = writer("INFO:\tPage may not be fully load.",output)
	#-------------------------
	#finding the little red "x for the person i just added
	try:
		allX = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID,"incomplete-links"))) #list of webelements
		allXtext = [element.text for element in allX]   #list of text for the webelements
		email  = loginToTest.replace("@mailinator.com","@jostletest1.mailgun.org")
		for text in allXtext:
			if email == text:
				loc = allXtext.index(text)
				X = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"span.delete-item"))) 
				correct_x = X[loc]
				correct_x.click()
				output = writer("VERIFY\tLittle Red 'x' for "+name+"\tOK",output)
				output = writer("INFO\tClicked Little Red 'x' for "+name,output)
				time.sleep(2)
	
				break
			else: pass
		else:
			output = writer("VERIFY\tLittle Red 'x' for "+name+"\tSKIPPED",output)
			output = writer("INFO:\tNo X Present for "+name,output)
	except (NoSuchElementException, TimeoutException):
		output = writer("INFO\tCouldn't find any Little Red x's ",output)

	#-------------------------
	driver.switch_to.default_content()
	#-------------------------
	try:
		adminGear = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnAdmin")))
		output = writer("VERIFY:\tAdmin Gear found\tOK",output)
		adminGear.click()
		output = writer("INFO:\tClicked Admin Gear",output)
	except TimeoutException:
		output = writer("VERIFY:\tQA:RichClient:btnAdmin\tSKIPPED",output)
	#-------------------------
	#Frame switch
	try:
		WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"QA:AdminFrame")))
		output = writer("INFO:\tSuccessfully switched to iframe",output)
	except TimeoutException:
		output = writer("INFO:\tCouldn't switch to iframe",output)
	#-------------------------
	#Manage Teams Admin
	try:
		manageTeamsAdmin = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:manageRelationshipAdmin")))
		output = writer("VERIFY:\tVerified manageRelationshipAdmin\tOK",output)
		manageTeamsAdmin.click()
		output = writer("INFO:\tClicked manageRelationshipAdmin",output)
	except TimeoutException:
		output = writer("INFO:\tQA:manageRelationshipAdmin didn't work",output)
	#-------------------------
	#verify if page was loaded
	try:
		WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.ID,"loading")))
	except TimeoutException:
		output = writer("INFO:\tPage may not be fully load.",output)
	#-------------------------
	#finding the little red "x for the person i just added
	try:
		allX = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID,"incomplete-links"))) #list of webelements
		allXtext = [element.text for element in allX][1:]   #list of text for the webelements
		# email = loginToTest.replace("@mailinator.com","@qa-email.jostletest.com")
		email = loginToTest.replace("@mailinator.com","@jostletest1.mailgun.org")
		for text in allXtext:
			if email == text:
				loc = allXtext.index(text)
				X = driver.find_elements_by_class_name("delete-item")
				correct_x = X[loc]
				correct_x.click()
				output = writer("VERIFY\tLittle Red 'x' for "+name+"\tOK",output)
				output = writer("INFO\tClicked Little Red 'x' for "+name,output)
				#-------------------------
				#verify if page was loaded
				try:
					WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.ID,"loading")))
				except TimeoutException:
					output = writer("INFO:\tTEAMS page did not fully load.",output)
				time.sleep(1)#Wait extra time to ensure page load.
	
				break
			else: pass
		else:
			output = writer("VERIFY\tLittle Red 'x' for "+name+"\tSKIPPED",output)
			output = writer("INFO:\tNo X Present for "+name,output)
	except (NoSuchElementException, TimeoutException):
		output = writer("INFO\tCouldn't find any Little Red x's ",output)
	#-------------------------
	driver.switch_to.default_content()
	#-------------------------

if __name__ == "__main__":
	testdriver = webdriver.Firefox()
	output = []
	output = writer("-"*50,output)
	output = writer("transform_reg_user",output)
	url = "https://usqa.jostle.us/jostle-prod/login.html"
	output = writer("URL:\t"+url,output)
	testdriver.get(url)    #navigate to login with URL
	regUser = "janlevenson_usqa@mailinator.com"
	output = writer("INFO:\tJostle Launched",output)
	try:
		usernameInput = WebDriverWait(testdriver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
		usernameInput.clear()                          #finding the login fields
		usernameInput.send_keys("jasonjones_usqa@mailinator.com")
		password = WebDriverWait(testdriver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
		password.clear()
		password.send_keys("Ship1Stop2")
		WebDriverWait(testdriver, 15).until(EC.element_to_be_clickable((By.NAME,"saveAndSubmit"))).click()
		output = writer("INFO:\tlogin submitted as Jason Jones",output)
	except TimeoutException:
		output = writer("INFO:\tlogin failed for Jason Jones",output)

	#-------------------------
	#get around the welcome screen
	get_around_welcome_screen(testdriver)
	#-------------------------
	transform_reg_user(testdriver,False,regUser,"Jan Levenson",output)
	testdriver.close()