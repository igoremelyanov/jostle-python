from BasePage import BasePage
from BasePage import IncorrectPageException
from GmailTitlePage import GmailTitlePage
import time

#from get_datetime import get_datetime
#now, date = get_datetime()


class GmailLoginPage(BasePage):
    def __init__(self, driver, username, password):
        super(GmailLoginPage, self).__init__(driver)
        self.username = username
        self.password = password

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10,"id","Email")
        except:
            #self..take_screenshot('GmailLoginPage_', date, now, 'IncorrectPageException_001.png')
            raise IncorrectPageException

    def login(self):
        self.fill_out_field("id",
                            "Email",
                            self.username
                            )
        print "INFO:\tEmail input found."
        self.click(10, "id", "next")
        print "INFO:\t'Next' button is Present."
        _title = self.driver.title #debug
        print "INFO:\tStill on --",_title, "--page" #debug
        #self.assertIn("Gmail", _title)

        self.driver.implicitly_wait(5)
        self.fill_out_field("id",
                            "Passwd",
                            self.password
                            )
        print "INFO:\tPassword Input box found."
        _title = self.driver.title #debug
        print "INFO:\tStill on--", _title, "--page" #debug
        self.click(10, "id", "signIn")
        print "INFO:\t'Sign in' button found."
        #self.click(10, "id", "choose-account-0") # debug
        print "INFO:\tOn--", _title, "--page"  # debug
        #self.click(10, "id", "signIn")

        #self.assertIn("Gmail", _title)
        time.sleep(10)
        _title = self.driver.title #debug
        print "INFO:\tOn--", _title, "--page"#debug
        return GmailTitlePage(self.driver)