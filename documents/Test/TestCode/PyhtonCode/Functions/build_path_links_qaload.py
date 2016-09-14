import os
from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
from get_buildno import get_buildno
from pathToPythonCode import pathToPythonCode


def build_path_links_qaload():
	driver = webdriver.Firefox()
	driver.implicitly_wait(20)         	#sets a general time to wait for an element to be found.
	driver.get("https://qaload.jostle.us/jostle-prod/login.html")    #navigate to login with URL
	driver.find_element_by_id("username").clear()                          #finding the login fields
	driver.find_element_by_id("username").send_keys("Tom.Merritt@mailinator.com")
	driver.find_element_by_id("password").clear()
	driver.find_element_by_id("password").send_keys("WTFoxtrot19")
	driver.find_element_by_name("saveAndSubmit").click()
	Build = get_buildno(driver)
	driver.quit()

	path = pathToPythonCode()
	build_path_links_qaload = path+"logFiles"+os.sep+"links_qaload"+os.sep+"buildData"+os.sep+Build+os.sep
	if not os.path.exists(build_path_links_qaload):
		os.makedirs(build_path_links_qaload)

	return build_path_links_qaload

if __name__ == "__main__":
	path = build_path_links_qaload()
	print path


