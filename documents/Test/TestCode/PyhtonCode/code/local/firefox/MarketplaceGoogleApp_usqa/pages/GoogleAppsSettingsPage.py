from BasePage import BasePage
from BasePage import IncorrectPageException
from GoogleMarketplaceAppsPage import GoogleMarketplaceAppsPage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class GoogleAppsSettings(BasePage):
    def __init__(self, driver):
        super(GoogleAppsSettings, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(20, "xpath", "//div[text()='APPS SETTINGS']")
        except:
            raise IncorrectPageException

    def get_title(self):
        return self.driver.title

    #def scroll_down(self):
        #return self.driver.execute_script("window.scrollTo(0, 500);")



    def MarketPlace_Apps_Button_click(self):
        self.click(10, "xpath", "//div[contains(@aria-label,'Marketplace apps Add and manage third-party apps')]")
        return GoogleMarketplaceAppsPage(self.driver)

