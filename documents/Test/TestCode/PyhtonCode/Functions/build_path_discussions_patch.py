import os
from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
from get_buildno import get_buildno
from pathToPythonCode import pathToPythonCode


def build_path_discussions_patch(buildNo):
	# driver = webdriver.Firefox()
	# driver.implicitly_wait(20)         	#sets a general time to wait for an element to be found.
	# driver.get("https://caqa.jostle.us/jostle-prod/login.html")    #navigate to login with URL
	# driver.find_element_by_id("username").clear()                          #finding the login fields
	# driver.find_element_by_id("username").send_keys("jasonjones@mailinator.com")
	# driver.find_element_by_id("password").clear()
	# driver.find_element_by_id("password").send_keys("Ship1Stop2")
	# driver.find_element_by_name("saveAndSubmit").click()
	# Build = get_buildno(driver)
	# driver.quit()

	path = pathToPythonCode()
	buildPath_patch = path+"logFiles"+os.sep+"discussions_patch"+os.sep+"buildData"+os.sep+buildNo+os.sep
	if not os.path.exists(buildPath_patch):
		os.makedirs(buildPath_patch)
	return buildPath_patch

if __name__ == "__main__":
	# path = build_path()
	# print path
	print "OK"
