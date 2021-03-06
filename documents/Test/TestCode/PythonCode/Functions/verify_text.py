#function to get the build number from the Jostle platform
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

def get_buildno(driver = None):
	"""this is a function that is used to grab the Jostle Build number from the
	platform and print to the console either that the build number was found or not.
	If the build number is found it returns that number, if not found it returns
	white space
	"""
	try:
		element = driver.find_element_by_class_name("buildno")
		text = element.text
		build = text
	except NoSuchElementException:
		print "Couldn't Find Build No."
		build = "    "
	return build


if __name__ == "__main__":
	driver = webdriver.Firefox()
	driver.implicitly_wait(20)         	#sets a general time to wait for an element to be found.
	#driver.maximize_window()
	driver.get("https://caqa.jostle.us/jostle-prod/login.html")    #navigate to login with URL
	driver.find_element_by_id("username").clear()                          #finding the login fields
	driver.find_element_by_id("username").send_keys("jasonjones@mailinator.com")
	driver.find_element_by_id("password").clear()
	driver.find_element_by_id("password").send_keys("Ship1Stop2")
	driver.find_element_by_name("saveAndSubmit").click()
	Build = get_buildno(driver) #must pass a webdriver
	print Build
	driver.close()

