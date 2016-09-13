from BasePage import BasePage
from BasePage import IncorrectPageException
from AdminWelcomeTitlePage import AdminWelcomeTitlePage

import time


class AdminWelcomeLoginPage(BasePage):
    def __init__(self, driver, username, password):
        super(AdminWelcomeLoginPage, self).__init__(driver)
        self.username = username
        self.password = password

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10,
                                             "id",
                                             "username"
                                             )
        except:
            raise IncorrectPageException

    def login(self):
        self.fill_out_field("id",
                            "username",
                            self.username
                            )
        self.click(10, "id", "continueButton")
        self.driver.implicitly_wait(3)
        self.fill_out_field("id",
                            "password",
                            self.password
                            )
        self.click(10, "id", "saveAndSubmit")
        time.sleep(2)
        return AdminWelcomeTitlePage(self.driver)