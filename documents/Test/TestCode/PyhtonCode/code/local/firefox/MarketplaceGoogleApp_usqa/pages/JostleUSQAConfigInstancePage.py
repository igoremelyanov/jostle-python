from BasePage import BasePage
from BasePage import IncorrectPageException
from JostleUSQAMasterAccountPage import JostleUSQAMasterAccountPage


class JostleUSQAConfigInstancePage(BasePage):
    def __init__(self, driver):
        super(JostleUSQAConfigInstancePage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//input[@value='Continue']")
        except:
            raise IncorrectPageException


    #def get_title(self):
        #return self.driver.title

    def choose_your_host_location_click(self, hostlocation):
        #self.click(10, "xpath", "//span[contains(text(), 'Australia')]")
        self.click(10, "xpath", "//span[contains(text(), '"+hostlocation+"')]")
        return self

    def continue_button_click(self):
        self.click(10, "xpath", "//input[@value='Continue']")
        return JostleUSQAMasterAccountPage(self.driver)


