from TestBaseCase import BaseTestCase
from Constants import TT_Constants
from pages.GmailLoginPage import GmailLoginPage
from writer import writer

#globals
output = []             #empty list to append Test Outputs

class BaseTestCase_GmailLogin(BaseTestCase):
    def setUp(self):
        super(BaseTestCase_GmailLogin, self).setUp()
        global output
        gmailLoginPageURL = TT_Constants['Gmail_Weaseal_URL']
        self.navigate_to_page(gmailLoginPageURL)
        gmail_page_obj = GmailLoginPage(self.driver,
                                        TT_Constants['Jostle_Weaseal_Username'],
                                        TT_Constants['Jostle_Weaseal_Password']
                                        )
        gmail_page_obj.login()
        _titlePage = gmail_page_obj.get_title()
        self.assertIn(" - dwight@weaseal.com - Weaseal.com Mail", _titlePage)
        output = writer("INFO:\tProxy check for Weaseal: Google Gmail Login Launched", output)
        # time.sleep(5)

    def tearDown(self):
        super(BaseTestCase_GmailLogin, self).tearDown()
