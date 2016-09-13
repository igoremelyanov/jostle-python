from BasePage import BasePage
from BasePage import IncorrectPageException

import time


class AdminEditEnterprisePage(BasePage):
    def __init__(self, driver):
        super(AdminEditEnterprisePage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10,
                                             "xpath",
                                             "//h1[contains(text(), 'Edit Enterprise')]"
                                             )
        except:
            raise IncorrectPageException

    def delete_link_click(self):
        self.click(10, "xpath", "//a[text()='Delete']")
        time.sleep(5) #for Debuging
        alert = self.driver.switch_to_alert()
        alert.accept()
        return self