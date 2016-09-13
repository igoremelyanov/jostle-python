from BasePage import BasePage
from BasePage import IncorrectPageException
from GoogleAppsSettingsPage import GoogleAppsSettings
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time

class GoogleAdminConsolePage(BasePage):
    def __init__(self, driver):
        super(GoogleAdminConsolePage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//div[text()='Admin console']")
        except:
            raise IncorrectPageException

    def get_title(self):
        return self.driver.title

    #def scroll_down(self):
        #return self.driver.execute_script("window.scrollTo(0, 500);")

    def Apps_Button_click(self):
        self.click(10, "xpath", "//div[@aria-label='Manage apps and their settings']")
        return GoogleAppsSettings(self.driver)
        #time.sleep(5)



    def validation_check(self):
        self.fill_out_field("xpath", "//input[contains(@name, 'first')]", "Paul")
        self.fill_out_field("xpath", "//input[contains(@name, 'last')]", "Pierce")
        self.fill_out_field("xpath", "(//input[contains(@id, 'input')])[3]", "contactemail@test.com")
        self.fill_out_field("xpath", "//textarea", "My comment")
        self.click(10, "xpath", "//span[.='Submit']")
        return self