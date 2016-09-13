from BasePage import BasePage
from BasePage import IncorrectPageException
from JostleUSQAUploadLogoPage import JostleUSQAUploadLogoPage

class JostleUSQAMasterAccountPage(BasePage):
    def __init__(self, driver):
        super(JostleUSQAMasterAccountPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//input[@value='Continue']")
        except:
            raise IncorrectPageException


    #def get_title(self):
        #return self.driver.title

    def continue_button_click(self):
        self.click(10, "xpath", "//input[@value='Continue']")
        return JostleUSQAUploadLogoPage(self.driver)


