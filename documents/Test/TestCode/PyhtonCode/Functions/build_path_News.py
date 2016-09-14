import os
from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
from get_buildno import get_buildno
from pathToPythonCode import pathToPythonCode


def build_path_News(Build,servername):

	path = pathToPythonCode()
	News_buildPath = path+"logFiles" +os.sep+"News_"+servername+os.sep+"buildData"+os.sep+Build+os.sep
	if not os.path.exists(News_buildPath):
		os.makedirs(News_buildPath)

	return News_buildPath

if __name__ == "__main__":
	path = build_path_News("1234",'usqa')
	print path