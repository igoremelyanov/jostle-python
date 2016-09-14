import os
from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
from get_buildno import get_buildno
from pathToPythonCode import pathToPythonCode


def build_path_News_qaload():
	driver = webdriver.Firefox()
	driver.implicitly_wait(20)         	#sets a general time to wait for an element to be found.
	driver.get("https://qaload.jostle.us/jostle-qaload/login.html")    #navigate to login with URL
	driver.find_element_by_id("username").clear()                          #finding the login fields
	driver.find_element_by_id("username").send_keys("Robin.Martinez@mailinator.com")
	driver.find_element_by_id("password").clear()
	driver.find_element_by_id("password").send_keys("Ship1Stop2")
	driver.find_element_by_name("saveAndSubmit").click()
	Build = get_buildno(driver)
	driver.quit()

	path = pathToPythonCode()
	News_buildPath_QALOAD = path+"logFiles"+os.sep+"News_qaload"+os.sep+"buildData"+os.sep+Build+os.sep
	if not os.path.exists(News_buildPath_QALOAD):
		os.makedirs(News_buildPath_QALOAD)

	return News_buildPath_QALOAD

if __name__ == "__main__":
	path = build_path_News_qaload()
	print path


