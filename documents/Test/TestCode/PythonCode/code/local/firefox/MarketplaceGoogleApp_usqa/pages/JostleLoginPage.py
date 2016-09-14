from BasePage import BasePage
from BasePage import IncorrectPageException
from JostleTitlePage import JostleTitlePage

class JostleLoginPage(BasePage):
    def __init__(self, driver, username, password):
        super(JostleLoginPage, self).__init__(driver)
        self.username = username
        self.password = password

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10,
                                             "xpath",
                                             "//input[contains(@value,'Login')]"
                                             )
        except:
            raise IncorrectPageException

    def login(self):
        self.fill_out_field("id",
                            "username",
                            self.username
                            )
        self.fill_out_field("id",
                            "password",
                            self.password
                            )
        self.click(10, "name", "saveAndSubmit")
        return JostleTitlePage(self.driver)








