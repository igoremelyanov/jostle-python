from BasePage import BasePage
from BasePage import IncorrectPageException
from JostleUSQAEditExcludedUsersPage import JostleUSQAEditExcludedUsersPage
from JostleUSQAQuickSetupCompletePage import JostleUSQAQuickSetupCompletePage
import time

class JostleUSQAImportPeoplePage(BasePage):
    def __init__(self, driver):
        super(JostleUSQAImportPeoplePage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "id", "excludeBlackListUsers")
        except:
            raise IncorrectPageException


    #def get_title(self):
        #return self.driver.title

    def exclude_checkbox_click(self):
        self.click(10, "id", "excludeBlackListUsers")
        return self


    def edit_blacklist_link_click(self):
        self.click(10, "xpath", "//a[contains(.,'Edit blacklist')]")
        return JostleUSQAEditExcludedUsersPage(self.driver)

    def import_people_button_click(self):
        self.click(10, "name", "import")
        time.sleep(10)
        return JostleUSQAQuickSetupCompletePage(self.driver)
