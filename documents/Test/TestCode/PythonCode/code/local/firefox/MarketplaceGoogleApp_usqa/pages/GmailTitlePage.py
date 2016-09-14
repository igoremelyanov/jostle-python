from BasePage import BasePage
from BasePage import IncorrectPageException
from GoogleAdminConsolePage import GoogleAdminConsolePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time


class GmailTitlePage(BasePage):
    def __init__(self, driver):
        super(GmailTitlePage, self).__init__(driver)

    def _verify_page(self):
        try:
            # skeeping verification
            #self.wait_for_element_visibility(15, "xpath", "//div[contains(text(),'COMPOSE')]")
            #self.wait_for_element_visibility(10, "id", ":2w")
            time.sleep(5)
            _title = self.driver.title #debug
            print "INFO:\tStill on--", _title, "--page" #debug
        except:
            raise IncorrectPageException

    def get_title(self):
        return self.driver.title

    #def scroll_down(self):
        #return self.driver.execute_script("window.scrollTo(0, 500);")

    def googleApp_Button_click(self):
        self.click(10, "xpath", "//div/a[contains(@title,'Google apps')]")
        return self

    def googleApp_Admin_Button_click(self):
        #Scrool Down To adminAppGearButton
        #hidden_adminAppGearButton = self.find_element("xpath", "//span[contains(@class,'gb_4') and contains(text(),'Admin')]")
        actionChains = ActionChains(self.driver)
        #actionChains.execute_script("window.scrollTo('Admin');")
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        #self.driver.set_window_size(1000, 800)
        actionChains.send_keys(Keys.SPACE)
        actionChains.perform()

        #time.sleep(5)

        # Get main and child window handles and switch to child window
        mainWindowHandle = self.driver.window_handles
        print "\tmain Window handle: %s" % mainWindowHandle
        #time.sleep(5)
        self.click(10, "xpath", "//span[contains(@class,'gb_4') and contains(text(),'Admin')]")
        #Get all handlers
        allWindowsHandlesList = self.driver.window_handles  # handles[0]: parent - handles[1]: child
        print "\tall Window handles: %s" % allWindowsHandlesList
        #Switching to new window: - child
        for handle in allWindowsHandlesList:
            if handle != mainWindowHandle[0]:
                self.driver.switch_to.window(handle)
                childWindowHandle = allWindowsHandlesList[1]
                print "\tswitch to child Window handle: %s" % childWindowHandle
                break
        #actionChains.move_to_element(hidden_adminAppGearButton)
        #actionChains.click(hidden_adminAppGearButton)
        #actionChains.perform()
        time.sleep(5)
        return GoogleAdminConsolePage(self.driver)


    def validation_check(self):
        self.fill_out_field("xpath", "//input[contains(@name, 'first')]", "Paul")
        self.fill_out_field("xpath", "//input[contains(@name, 'last')]", "Pierce")
        self.fill_out_field("xpath", "(//input[contains(@id, 'input')])[3]", "contactemail@test.com")
        self.fill_out_field("xpath", "//textarea", "My comment")
        self.click(10, "xpath", "//span[.='Submit']")
        return self