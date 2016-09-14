from BasePage import BasePage
from BasePage import IncorrectPageException
from JostleWeasealTitlePage import JostleWeasealTitlePage

class JostleUSQAQuickSetupCompletePage(BasePage):
    def __init__(self, driver):
        super(JostleUSQAQuickSetupCompletePage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "name", "launch")
        except:
            raise IncorrectPageException


    #def get_title(self):
        #return self.driver.title


    def launch_jostle_button_click(self):
        self.click(10, "name", "launch")
        return JostleWeasealTitlePage(self.driver)
