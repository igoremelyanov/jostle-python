from BasePage import BasePage
from BasePage import IncorrectPageException
from JostleUSQAImportPeoplePage import JostleUSQAImportPeoplePage

class JostleUSQAEnableAPIAccessPage(BasePage):
    def __init__(self, driver):
        super(JostleUSQAEnableAPIAccessPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "id", "linkDiv")
        except:
            raise IncorrectPageException


    #def get_title(self):
        #return self.driver.title

    def continue_link_click(self):
        self.click(10, "id", "linkDiv")
        return JostleUSQAImportPeoplePage(self.driver)


