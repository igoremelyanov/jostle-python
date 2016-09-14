#function to get the build number from the Jostle platform
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.]
from get_datetime import get_datetime   #date\time funtion that we use for file names
from path_est import path_est   
from writer import writer               #function to handle outputs
import time,os

def execute_login(driver = None,intervalWaitForPage = None,url = None,username = None,password = None,testString = None,screenshotPath = None,now = None,screenshotPos =None,output = None):
	"""
	   this is a function that is used to close any existing popup screens when user logs in.
	   @param driver: instance of selenium webdriver being used by class that called this function.
	   @param intervalWaitForPage: interval that webdriver will wait for page to load before abort, set to 1 min if empty.
	   @param url: URL of the server to logon to. (e.g "https://usqa.jostle.us/jostle-prod/login.html")
	   @param username: username for the login procedure (e.g. Leo.Laporte@mailinator.com).
	   @param password: password used for the login procedure, set to 'Ship1Stop2' if empty.
	   @param testString: name of the test to be used in the save_screenshot
	   @param screenshotPath: path for the screenshot dir
	   @param screenshotPos: number of the first screenshot to be taken (e.g. 1, 2 , 3 ...)
	   @param output: variable for the log buffer used by the test.
	   ++ All arguments needed, but it is possible to set intervalWaitForPage, password, screenshotPath, now, and screenshotPos to None.
	"""
	global start,log_path
	pageLoadWaitInterval = intervalWaitForPage if intervalWaitForPage != None else 60
	if password == None:
		password = "Ship1Stop2"
	if screenshotPos == None:
		screenshotPos = 1
	if now == None:
		now,date = get_datetime() 	            #get date and time string
	if screenshotPath == None:
		log_path,screenshotPath = path_est(date)
	if (driver == None or url == None or username == None or testString == None or output == None):
		print "ERROR in execute_login(): Please sent webdriver, URL, username, testString and output as arguments."
	else:
		driver.set_page_load_timeout(pageLoadWaitInterval)
		#-------------------------
		#verify if link page was loaded
		try:
			driver.get(url)    #navigate to login with URL
			start = time.time()
			output = writer("INFO:\tJostle Launched",output)
			#driver.save_screenshot(screenshotPath+os.sep+testString+"_"+now+"_"+str(screenshotPos).zfill(3)+".png")
			screenshotPos +=1
			time.sleep(1) # added for Ap.jostle.us timing issue.
			usernameInput = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"username")))
			usernameInput.clear()                          #finding the login fields
			usernameInput.send_keys(username)
			passwordInput = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"password")))
			passwordInput.clear()
			passwordInput.send_keys(password)
			driver.save_screenshot(screenshotPath+os.sep+testString+"_"+now+"_"+str(screenshotPos).zfill(3)+".png")
			WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.NAME,"saveAndSubmit"))).click()
			output = writer("INFO:\tlogin submitted as "+username,output)
		except TimeoutException:
			output = writer("INFO:\tlogin failed for "+username,output)
		
	return start


if __name__ == "__main__":
	testdriver = webdriver.Firefox()
	url = "https://usqa.jostle.us/jostle-prod/login.html"
	usernameEntry = "jasonjones_usqa@mailinator.com"
	passEntry = "Ship1Stop2"
	prog = "execute_login"
	global output
	output = []                                 #empty list to append Test Outputs
	output = writer("-"*50,output)
	output = writer(prog,output)  
	execute_login(testdriver,None,url,usernameEntry,None,prog,None,None,None,output)
	testdriver.close()