from BasePage import BasePage
from BasePage import IncorrectPageException
from AdminEnterprisesPage import AdminEnterprisesPage

import time


class AdminWelcomeTitlePage(BasePage):
    def __init__(self, driver):
        super(AdminWelcomeTitlePage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10,
                                             "xpath",
                                             "//a[contains(text(), 'Welcome')]"
                                             )
        except:
            raise IncorrectPageException

    def get_title(self):
        return self.driver.title

    def list_enterprises_link_click(self):
        self.click(10, "xpath", "//a[contains(text(), 'List Enterprises')]")
        return AdminEnterprisesPage(self.driver)

