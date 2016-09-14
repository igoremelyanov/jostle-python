from BasePage import BasePage
from BasePage import IncorrectPageException


from selenium.common.exceptions import NoSuchElementException
from GoogleJostleUSQASettingsPage import GoogleJostleUSQASettingsPage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class TermOfServiceAgreementPage(BasePage):
    def __init__(self, driver):
        super(TermOfServiceAgreementPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//div/span[contains(text(),'You are granting') and 'Jostle USQA' and 'the right to access your domain data:']")
        except:
            raise IncorrectPageException

    def get_title(self):
        return self.driver.title

    #def scroll_down(self):
        #return self.driver.execute_script("window.scrollTo(0, 500);")

    def term_of_service_checkbox_click(self):
        self.click(10, "xpath", "//div[@role='checkbox']")
        return self



    def accept_button_click(self):
        self.click(10, "cssSelector", ".goog-buttonset-action.buttonRight")
        return self
        #return GoogleJostleUSQASettingsPage(self.driver)




    #def MarketPlace_Apps_Button_click(self):
        #self.click(10, "xpath", "//div[@aria-label='3 Marketplace apps Add and manage third-party apps']")
        #return self

