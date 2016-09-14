import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from get_buildno import get_buildno
from pathToPythonCode import pathToPythonCode
from writer import writer               #function to handle outputs
import time


def check_page_info(driver, output, arrayExpValues, arrayXpathes):
	
	prog = os.path.basename(__file__).split(".")[0]      	#gets the name of the currently running program	
	result = "pass"		                        	

	output = writer("INFO:\t----------- FUNCTION check_page_info starts work -----------",output)	
	i=0
	for expValue in arrayExpValues:			
		try:
			receivedElement = driver.find_element_by_xpath(arrayXpathes[i])
			valueOf_receivedElement = receivedElement.get_attribute("innerHTML") #Retrieve contents of inside the mailinator mail entry line.
			output = writer("INFO:\t Name of element received by xpath is - "+valueOf_receivedElement+" ",output)

			if (expValue in valueOf_receivedElement):				
				output = writer("VERIFY:\t The field expValue of received element is correct\tPASS",output)					
			else:
				output = writer("VERIFY:\t The field expValue of received element is wrong\tFAIL",output)
				result = "fail"					
		except NoSuchElementException:
			output = writer("INFO:\t NoSuchElementException",output)
			result= "fail"
		i+=1
	output = writer("INFO:\t--------- FUNCTION check_page_info finished work ---------",output)
	return result