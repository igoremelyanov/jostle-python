from BasePage import BasePage
from BasePage import IncorrectPageException
from JostleWeasealAdministrationSettingsPage import JostleWeasealAdministrationSettingsPage

class JostleWeasealTitlePage(BasePage):
    def __init__(self, driver):
        super(JostleWeasealTitlePage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "id", "QA:RichClient:btnAdmin")
        except:
            raise IncorrectPageException


    def get_title(self):
        return self.driver.title

    def welcomePopupCloseButton_click(self):
        self.click(10, "id", "welcomePopupCloseButton")
        return self

    def gear_button_click(self):
        self.click(10, "id", "QA:RichClient:btnAdmin")
        # Switch to 'QA:AdminFrame'
        iFrameElement = self.find_element("id", "QA:AdminFrame")
        self.driver.switch_to.frame(iFrameElement)
        return JostleWeasealAdministrationSettingsPage(self.driver)
