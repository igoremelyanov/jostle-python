from BasePage import BasePage
from BasePage import IncorrectPageException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class GoogleConfirmRemovalOfAppPage(BasePage):
    def __init__(self, driver):
        super(GoogleConfirmRemovalOfAppPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//div[text()='Confirm removal of Jostle USQA']")
        except:
            raise IncorrectPageException

    def get_title(self):
        return self.driver.title

    #def scroll_down(self):
        #return self.driver.execute_script("window.scrollTo(0, 500);")




    def confirm_removal_app_button_click(self):
        self.click(10, "xpath", "//div[text()='Remove App']")
        return self
            #GoogleJostleUSQASettingsPage(self.driver)

