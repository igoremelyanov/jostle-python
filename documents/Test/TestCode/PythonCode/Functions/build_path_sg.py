import os
from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
from get_buildno import get_buildno
from pathToPythonCode import pathToPythonCode


def build_path_sg():
	driver = webdriver.Firefox()
	driver.implicitly_wait(20)         	#sets a general time to wait for an element to be found.
	driver.get("https://sg.jostle.us/jostle-sgprod/login.html")    #navigate to login with URL
	driver.find_element_by_id("username").clear()                          #finding the login fields
	driver.find_element_by_id("username").send_keys("jasonjones_sg@mailinator.com")
	driver.find_element_by_id("password").clear()
	driver.find_element_by_id("password").send_keys("Ship1Stop2")
	driver.find_element_by_name("saveAndSubmit").click()
	Build = get_buildno(driver)
	driver.quit()

	path = pathToPythonCode()
	buildPath_sg = path+"logFiles"+os.sep+"adminPages_sg"+os.sep+"buildData"+os.sep+Build+os.sep
	if not os.path.exists(buildPath_sg):
		os.makedirs(buildPath_sg)
	return buildPath_sg

if __name__ == "__main__":
	path = build_path_sg()
	print path


