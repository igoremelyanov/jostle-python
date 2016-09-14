from BasePage import BasePage
from BasePage import IncorrectPageException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class GoogleJostleUSQASettingsPage(BasePage):
    def __init__(self, driver):
        super(GoogleJostleUSQASettingsPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//div[text()='Settings for Jostle USQA']")
        except:
            raise IncorrectPageException

    def get_title(self):
        return self.driver.title

    #def scroll_down(self):
        #return self.driver.execute_script("window.scrollTo(0, 500);")




    def remove_app_button_click(self):
        self.click(10, "xpath", "//img[@alt='Remove App']")
        return self
            #GoogleJostleUSQASettingsPage(self.driver)

