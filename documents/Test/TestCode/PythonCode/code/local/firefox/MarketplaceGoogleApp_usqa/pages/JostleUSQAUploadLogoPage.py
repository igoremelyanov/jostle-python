from BasePage import BasePage
from BasePage import IncorrectPageException
from JostleUSQAEnableAPIAccessPage import JostleUSQAEnableAPIAccessPage


class JostleUSQAUploadLogoPage(BasePage):
    def __init__(self, driver):
        super(JostleUSQAUploadLogoPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//*[@class='standard-links']/a")
        except:
            raise IncorrectPageException


    #def get_title(self):
        #return self.driver.title

    def skip_it_link_click(self):
        self.click(10, "xpath", "//*[@class='standard-links']/a")
        return JostleUSQAEnableAPIAccessPage(self.driver)


