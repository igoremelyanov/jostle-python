from BasePage import BasePage
from BasePage import IncorrectPageException
from selenium.common.exceptions import NoSuchElementException
from GoogleJostleUSQASettingsPage import GoogleJostleUSQASettingsPage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class GoogleMarketplaceAppsPage(BasePage):
    def __init__(self, driver):
        super(GoogleMarketplaceAppsPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//div[text()='Marketplace apps']")
        except:
            raise IncorrectPageException

    def get_title(self):
        return self.driver.title

    #def scroll_down(self):
        #return self.driver.execute_script("window.scrollTo(0, 500);")

    def check_JostleUSQA_row_exists(self):
        try:
            self.find_element("xpath", "//a[text()='Jostle USQA']")
            return True
        except NoSuchElementException:
            return False


    def JostleUSQA_Link_click(self):
        self.click(10, "xpath", "//a[@aria-label='Settings for Jostle USQA']")
        return GoogleJostleUSQASettingsPage(self.driver)


    #def MarketPlace_Apps_Button_click(self):
        #self.click(10, "xpath", "//div[@aria-label='3 Marketplace apps Add and manage third-party apps']")
        #return self

