from BasePage import BasePage
from BasePage import IncorrectPageException
from AdminEditEnterprise import AdminEditEnterprisePage
from selenium.common.exceptions import NoSuchElementException

import time


class AdminEnterprisesPage(BasePage):
    def __init__(self, driver):
        super(AdminEnterprisesPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//h1[contains(text(), 'Enterprises')]")
        except:
            raise IncorrectPageException

    def search_for_enterprise(self):
        # check the search results
        try:
            row = self.find_element("xpath", "//tbody/tr[td[2]//text()='weaseal.com']")
            # print(row.text)
            # print(row.text[:6])
            # id = row.text[:6]
            return True
        except NoSuchElementException:
            return False

    def get_id(self):
            row = self.find_element("xpath", "//tbody/tr[td[2]//text()='weaseal.com']")
            return row.text[:6]

    def id_link_click(self, id):
            self.click(10, "xpath", "//td/a[text()='" + id + "']")
            return AdminEditEnterprisePage(self.driver)

