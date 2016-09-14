#function to get the build number from the Jostle platform
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException     #exception for timeout
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By #Necessary for Explicit Wait test
from selenium.webdriver.support.ui import WebDriverWait #Explicit Wait
from selenium.webdriver.support import expected_conditions as EC #handles the expected conditions for Explicit Waits.]
from writer import writer               #function to handle outputs
from get_around_welcome_screen import get_around_welcome_screen #function to bypass startup popup
import time,os

def ensure_not_team_member(driver=None,privateTeam=None,name=None,output=None):
	"""
	   this is a function is used to verify if user is regular user, MUST BE called after loginToTest with administrator and dismissal of the the welcome popup.
		@param driver: instance of the selenium webdriver being used by the test that called this function.
		@param privateTeam: private team name to verify if user is not a member
		@param name: name of the user that should be regular user. Can be fullname or part of name that is unique enough.
		@param output: variable for the log buffer used by the test.
	"""
	print privateTeam
	print name
	print output
	output = writer("-"*50,output)
	output = writer("INFO: Checking and transforming in regular user ",output)
	try:
		teamsButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:RichClient:btnTeams")))
		output = writer("VERIFY:\tTEAMS menu option present",output)
		teamsButton.click()
		output = writer("INFO:\tClicked TEAMS on menu",output)
	except (NoSuchElementException, TimeoutException):
		output = writer("VERIFY:\tQA:RichClient:btnTEAMS",output)
	#-------------------------
	#get around the welcome screen
	get_around_welcome_screen(driver)
	#-------------------------
	#Open search drawer
	try:
		searchButton = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:SearchAndFilterHeader:showOrHideSearch")))
		output = writer("VERIFY\tQA:SearchAndFilterHeader:showOrHideSearch present\tPASS",output)
		searchButton.click()
		output = writer("INFO:\tQA:TeamsView:searchInput clicked",output)
	except TimeoutException:
		output = writer("VERIFY\tQA:SearchAndFilterHeader:showOrHideSearch present\tFAIL",output)
	#-------------------------
	#Search Private Team
	try:
		searchInput = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:TeamsView:searchInput")))
		output = writer("VERIFY\tQA:TeamsView:searchInput present\tPASS",output)
		searchInput.send_keys(privateTeam+Keys.ENTER)
		output = writer("INFO:\tQA:TeamsView:searchInput submitted",output)
	except TimeoutException:
		output = writer("VERIFY\tQA:TeamsView:searchInput present\tFAIL",output)
	#-------------------------
	#Click on Private Team
	try:
		privateTeamTile = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//tr[@class='QA:SearchDump:ResultsRow']/.//*[contains(text(),'"+privateTeam+"')]")))
		output = writer("VERIFY\tPrivate team tile is present\tPASS",output)
		privateTeamTile.click()
		output = writer("INFO:\tPrivate team tile clicked",output)
	except TimeoutException:
		output = writer("VERIFY\tPrivate team tile is present\tFAIL",output)
	#-------------------------
	#Click on Members Tab
	try:
		membersTab = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:TeamProfile:membersButton")))
		output = writer("VERIFY\tMembers tab button is present\tPASS",output)
		membersTab.click()
		output = writer("INFO:\tMembers tab button clicked",output)
	except TimeoutException:
		output = writer("VERIFY\tMembers tab button is present\tFAIL",output)
	#-------------------------
	#Check user not on Members Tab
	try:
		WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[contains(text(),'Direct members')]/../../../..//*[contains(text(),'"+name+"')]")))
		output = writer("VERIFY\tName not found in Members list\tFAIL",output)
		#-------------------------
		#Go to TEAMS view for the private team
		try:
			viewInTeams = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:TeamProfile:gotoCentricView")))
			output = writer("VERIFY\tView in Teams button found\tPASS",output)
			viewInTeams.click()
			output = writer("INFO\tView in Teams button clicked",output)
		except TimeoutException:
			output = writer("VERIFY\tView in Teams button found\tFAIL",output)
			output = writer("CATASTROPHIC ERROR:\tUnable to remove the user from team",output)
		#-------------------------
		#Edit Private Team
		try:
			viewInTeams = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,"QA:CentricView:editButton")))
			output = writer("VERIFY\tEdit Teams button found\tPASS",output)
			viewInTeams.click()
			output = writer("INFO\tEdit Teams button clicked",output)
		except TimeoutException:
			output = writer("VERIFY\tEdit Teams button found\tFAIL",output)
			output = writer("CATASTROPHIC ERROR:\tUnable to edit team",output)
		#-------------------------
		#Locate card of the user that should not be team member
		try:
			userCard = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='overflowVisible CardDecorator']/div/div/div[contains(@title,'"+name+"')]")))
			output = writer("VERIFY\tUser card found\tPASS",output)
			ActionChains(driver).move_to_element(userCard).perform()
			output = writer("INFO\tUser card clicked",output)
		except TimeoutException:
			output = writer("VERIFY\tUser card NOT found\tFAIL",output)
			output = writer("CATASTROPHIC ERROR:\tUnable to edit team",output)
		#-------------------------
		#Remove user from team
		try:
			removeOption = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Remove')]")))
			output = writer("VERIFY\tRemove option found\tPASS",output)
			ActionChains(driver).move_to_element(removeOption).perform()
			output = writer("INFO\tRemove option clicked",output)
			removeContributor = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//*[text()='Contributor']")))
			output = writer("VERIFY\tRemove Contributor option found\tPASS",output)
			ActionChains(driver).move_to_element(removeContributor).click().perform()
			output = writer("INFO\tRemove Contributor option clicked",output)
			try:
				userCard = WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH,"//div[@class='overflowVisible CardDecorator']/div/div/div[contains(@title,'"+name+"')]")))
				output = writer("VERIFY\tUser removal\tPASS",output)
			except TimeoutException:
				output = writer("VERIFY\tUser removal\tFAIL",output)
		except TimeoutException:
			output = writer("VERIFY\tRemove option found\tFAIL",output)
			output = writer("CATASTROPHIC ERROR:\tUnable to edit team",output)
	except TimeoutException:
		output = writer("VERIFY\tName not found in Members list\tPASS",output)

if __name__ == "__main__":
	testdriver = webdriver.Firefox()
	testdriver.maximize_window()
	output = []
	output = writer("-"*50,output)
	output = writer("ensure_not_team_member",output)
	url = "https://usqa.jostle.us/jostle-prod/login.html"
	output = writer("URL:\t"+url,output)
	testdriver.get(url)    #navigate to login with URL
	notTeamMember = "Toby Flend"
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
	ensure_not_team_member(testdriver,"PrivateAwesomeTeam",notTeamMember,output)
	testdriver.close()