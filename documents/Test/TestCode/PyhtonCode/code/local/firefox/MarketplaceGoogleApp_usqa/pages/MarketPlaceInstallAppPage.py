from BasePage import BasePage
from BasePage import IncorrectPageException



from selenium.common.exceptions import NoSuchElementException
from GoogleJostleUSQASettingsPage import GoogleJostleUSQASettingsPage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class MarketPlaceInstallAppPage(BasePage):
    def __init__(self, driver):
        super(MarketPlaceInstallAppPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//div/h1[text()='Jostle USQA App']")
        except:
            raise IncorrectPageException

    def get_title(self):
        return self.driver.title

    #def scroll_down(self):
        #return self.driver.execute_script("window.scrollTo(0, 500);")



    def install_app_button_click(self):
        # Switch to 'INSTALL APP' iFrame
        #iFrameXPAth = "//div[@id='___additnow_0']/iframe"
        iFrameElement = self.find_element("xpath", "//div[@id='___additnow_0']/iframe")
        #iFrameElement = WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_id(iFrameXPAth))
        self.driver.switch_to.frame(iFrameElement)
        #self.find_element("xpath", "//div/span[text()='INSTALL APP']")
        self.click(10, "xpath", "//div/span[text()='INSTALL APP']")
        print "\tSwitched to iFrame and clicked to INSTALL APP button"

        # Get main and child window handles and swith to child window
        #allWindowsHandlesList = self.driver.window_handles  # handles[0]: parent - handles[1]: child
        #self.switch_to_window(self, allWindowsHandlesList)


        return self
        #return GoogleJostleUSQASettingsPage(self.driver)




    #def MarketPlace_Apps_Button_click(self):
        #self.click(10, "xpath", "//div[@aria-label='3 Marketplace apps Add and manage third-party apps']")
        #return self

