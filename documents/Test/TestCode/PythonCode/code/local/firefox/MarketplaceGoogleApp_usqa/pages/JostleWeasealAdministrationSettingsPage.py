from BasePage import BasePage
from BasePage import IncorrectPageException
from selenium.common.exceptions import NoSuchElementException

class JostleWeasealAdministrationSettingsPage(BasePage):
    def __init__(self, driver):
        super(JostleWeasealAdministrationSettingsPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//div[text()='Administration settings']")
        except:
            raise IncorrectPageException

    def edit_delete_contributors_href_click(self):
        self.click(10, "id", "QA:editDeleteContributors")
        return self
        #return JostleWeasealEditDeleteContributorsPage(self.driver)

    def search_for_contributor(self, contributor):
        self.fill_out_field("id",
                            "searchText",
                            contributor
                            )
        self.click(10, "id", "searchButton")
        #check the search results
        try:
            self.find_element("xpath", "//a/span[@class='delete-item']")
            return True
        except NoSuchElementException:
            return False

    def delete_click(self):
        self.click(10, "xpath", "//a/span[@class='delete-item']")
        #Switch to Alert and confirm to delete contributor
        alert = self.driver.switch_to_alert()
        alert.accept()
        return self

    def delete_conformation_message(self):
        #element = None
        element = self.find_element("xpath", "//td/span[@class='success-result']")
        return element

    def initialaze_storage_href_click(self):
        self.click(10, "id", "QA:initializeLibrary")
        return self
        # return JostleWeasealEditDeleteContributorsPage(self.driver)

    def own_google_doamin_radio_button_click(self):
        # check if radio button there and clickable
        try:
            self.click(10, "id", "libraryPermissionGoogleGroupsInDomainOn")
            return True
        except NoSuchElementException:
            return False

    def hidden_google_doamin_radio_button_click(self):
        # check if radio button there and clickable
        try:
            self.click(10, "id", "libraryPermissionGoogleGroupsInDomain")
            return True
        except NoSuchElementException:
            return False

    def initialize_button_click(self):
        self.click(10, "id", "enableDisableButton")
        return self

    def can_see_manage_library_screen(self):
        try:
            self.wait_for_element_visibility(10, "xpath", "//div[text()='Manage Categories and Volumes']")
            return True
        except NoSuchElementException:
            return False







