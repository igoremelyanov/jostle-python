from BasePage import BasePage
from BasePage import IncorrectPageException

class JostleTitlePage(BasePage):
    def __init__(self, driver):
        super(JostleTitlePage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//div[contains(@class,'popupContent')]")
        except:
            raise IncorrectPageException

