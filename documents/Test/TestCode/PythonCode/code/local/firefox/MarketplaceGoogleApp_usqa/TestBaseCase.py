from selenium import webdriver
from Constants import TT_Constants
import unittest
import os

class TestBaseCase(object):

    def setUp(self):
        if TT_Constants['Browser'].lower() == "firefox":
            self.driver = webdriver.Firefox()
            self.driver.maximize_window()
            #self.driver.execute_script("window.scrollTo(0, 500);")
        elif TT_Constants['Browser'].lower() == "chrome":
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        elif TT_Constants['Browser'].lower() == "ie":
            self.driver = webdriver.Ie()
            self.driver.maximize_window()
        else:
            raise Exception("This browser is not supported at the moment.")

    def navigate_to_page(self, url):
        self.driver.get(url)

    def pathToPythonCode(self):
        prog = os.path.abspath(__file__).split(os.sep)  # location of this program
        levels = prog.index("PythonCode")
        folders = prog[:levels + 1]
        path = ''
        for entry in folders:
            path += entry + os.sep
        return path

    def take_screenshot(self, testname, date, now, pngnumber):
        path = self.pathToPythonCode()
        full_path = path + "screenShots" + os.sep + date + os.sep
        #shot_path = '/user/igoremelyanov/documents/root/Test/TestCode/PythonCode/screenShots/"+date+"/'
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        self.driver.get_screenshot_as_file(full_path + os.sep + testname + now + pngnumber)
        return full_path

    def tearDown(self):
        self.driver.quit()
