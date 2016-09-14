from BasePage import BasePage
from BasePage import IncorrectPageException
from JostleWeasealTitlePage import JostleWeasealTitlePage

class JostleWeasealLoginPage(BasePage):
    def __init__(self, driver, username):
        super(JostleWeasealLoginPage, self).__init__(driver)
        self.username = username
        #self.password = password

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10,
                                             "xpath",
                                             "//div/span[contains(text(), 'Welcome! Let') and 'login']"
                                             )
        except:
            raise IncorrectPageException

    def login(self):
        self.fill_out_field("id",
                            "username",
                            self.username
                            )
        self.click(10, "id", "saveAndSubmit")
        self.driver.implicitly_wait(5)
        #self.fill_out_field("id",
         #                   "password",
          #                  self.password
           #                 )
        #self.click(10, "name", "saveAndSubmit")
        return JostleWeasealTitlePage(self.driver)








