from BasePage import BasePage
from BasePage import IncorrectPageException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
#from JostleUSQAEditExcludedUsersPage import JostleUSQAEditExcludedUsersPage

class JostleUSQAEditExcludedUsersPage(BasePage):
    def __init__(self, driver):
        super(JostleUSQAEditExcludedUsersPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//input[contains(@name,'updateBlackList')]")
        except:
            raise IncorrectPageException


    #def get_title(self):
        #return self.driver.title

    def add_select_option_click(self):
        self.click(10, "xpath", "//select[contains(@ondblclick,'addSelected')]/option[contains(@title,'len@')]")
        return self


    def add_to_black_list_button_click(self):
        self.click(10, "xpath", "//input[contains(@id,'addSelected')]")
        return self

    def remove_selected_option_click(self, contributor):
        # check the search results
        try:
            self.click(10, "xpath", "//select[contains(@ondblclick,'removeSelected')]/option[contains(text(),'"+contributor+"')]")
            return True
        except TimeoutException:
            return False

    def remove_selected_list_button_click(self):
        self.click(10, "xpath", "//input[contains(@id,'removeSelected')]")
        return self



    def save_excluded_users_button_click(self):
        self.click(10, "xpath", "//input[contains(@name,'updateBlackList')]")
        return self
            #JostleUSQAEditExcludedUsersPage(self.driver)


