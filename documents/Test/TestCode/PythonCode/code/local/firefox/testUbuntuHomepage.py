#!/usr/bin/env python

import unittest
from selenium import webdriver


class testUbuntuHomepage(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        
    def test_Title(self):
        self.browser.get('http://www.ubuntu.com/')
        self.assertIn('Ubuntu', self.browser.title)
        
    def tearDown(self):
        self.browser.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)
