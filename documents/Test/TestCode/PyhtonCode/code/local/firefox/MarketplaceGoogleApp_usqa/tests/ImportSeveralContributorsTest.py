#  Verify that we can Import contributors from Google App Market to Jostle (Weaesal enterprise)
# make sure that Weaseal enterprise exist there

from TestBaseCase import TestBaseCase
from Constants import TT_Constants
from pages.JostleWeasealLoginPage import JostleWeasealLoginPage
from pages.JostleWeasealTitlePage import JostleWeasealTitlePage
from pages.GmailLoginPage import GmailLoginPage
from pages.GmailTitlePage import GmailTitlePage
from pages.GoogleAdminConsolePage import GoogleAdminConsolePage
from pages.GoogleAppsSettingsPage import GoogleAppsSettings
from pages.GoogleMarketplaceAppsPage import GoogleMarketplaceAppsPage
from pages.GoogleJostleUSQASettingsPage import GoogleJostleUSQASettingsPage
from pages.GoogleConfirmRemovalOfAppPage import GoogleConfirmRemovalOfAppPage
from pages.MarketPlaceInstallAppPage import MarketPlaceInstallAppPage
from pages.TermOfServiceAgeementPage import TermOfServiceAgreementPage
from pages.JostleWeasealAdministrationSettingsPage import JostleWeasealAdministrationSettingsPage
from pages.JostleUSQAConfigInstancePage import JostleUSQAConfigInstancePage
from pages.JostleUSQAMasterAccountPage import JostleUSQAMasterAccountPage
from pages.JostleUSQAUploadLogoPage import JostleUSQAUploadLogoPage
from pages.JostleUSQAEnableAPIAccessPage import JostleUSQAEnableAPIAccessPage
from pages.JostleUSQAImportPeoplePage import JostleUSQAImportPeoplePage
from pages.JostleUSQAEditExcludedUsersPage import JostleUSQAEditExcludedUsersPage
from pages.JostleUSQAQuickSetupCompletePage import JostleUSQAQuickSetupCompletePage

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

#custom functions
from path_est import path_est           #function to open date folders for dumps
from selenium.common.exceptions import TimeoutException
from writer import writer
import unittest, os, time
from get_datetime import get_datetime
from get_buildno import get_buildno   #function to get the build number from the Jostle platform
from build_path_MarketplaceGoogleApp_usqa import build_path_MarketplaceGoogleApp_usqa

#globals
output = []                             #empty list to append Test Outputs
prog = os.path.basename(__file__)       #gets the name of the currently running program
now, date = get_datetime() 	            #get date and time string
total = 2                                   #total number of tests
res = {"P": 0}	                        #initializing pass/fail counters
log_path, shot_path = path_est(date)
buildPath = build_path_MarketplaceGoogleApp_usqa()

class ImportSeveralContributorsTest(TestBaseCase, unittest.TestCase):

    def setUp(self):
        super(ImportSeveralContributorsTest, self).setUp()

    def tearDown(self):
        global output
        if res["P"] == total:
            f = open(log_path + os.sep + prog + "_" + now + "_PASS.log", 'w')
            g = open(buildPath + os.sep + prog + "_PASS.log", 'w')
            output = writer("RESULTS:\t" + prog + "\tPASS\t" + str(elapsed)[0:-1]+"\t"+Build, output)
            f.writelines(output)
            g.writelines(output)
        else:
            f = open(log_path + os.sep + prog + "_" + now + "_FAIL.log", 'w')
            g = open(buildPath + os.sep + prog + "_FAIL.log", 'w')
            output = writer("RESULTS:\t" + prog + "\tFAIL\t" + str(elapsed)[0:-1]+"\t"+Build, output)
            f.writelines(output)
            g.writelines(output)
        f.close()
        g.close()
        super(ImportSeveralContributorsTest, self).tearDown()


    def test_Can_import_several_contributors_from_Google_to_Weaseal(self):
        global output
        output = writer("-" * 50, output)
        output = writer(prog, output)
        output = writer("-" * 50, output)
        output = writer("DATE:\t" + date, output)
        output = writer("OS PLATFORM:\t\t" + self.driver.capabilities["platform"], output)
        output = writer(
            "BROWSER VERSION:\t" + self.driver.capabilities["browserName"] + " " + self.driver.capabilities["version"],
            output)
        output = writer("SELENIUM VERSION:\t" + str(webdriver.__version__), output)
        start = time.time()


        '''#Make sure that GoogleMarketPlaceApp has been not removed and insatall one in such a case of.'''
        output = writer("INFO:\tProxy check for existing Market Place in GoogleApps", output)
        #Login to Google Gmail Weaseal
        output = writer("INFO:\tLogin to Weasel Gmail to make proxy check for Marketplase App", output)
        gmailLoginPageURL = TT_Constants['Gmail_Weaseal_URL']
        self.navigate_to_page(gmailLoginPageURL)
        self.take_screenshot('ImportTest_', date, now, 'gmailloginpage_001.png')
        gmail_page_obj = GmailLoginPage(self.driver,
                                        TT_Constants['Jostle_Weaseal_Username'],
                                        TT_Constants['Jostle_Weaseal_Password']
                                        )
        gmail_page_obj.login()
        self.take_screenshot('ImportTest_', date, now, 'gmailtitlePage_002.png')
        gmail_title_page_obj = GmailTitlePage(self.driver)
        _titlePage = gmail_title_page_obj.get_title()
        self.assertIn(" - dwight@weaseal.com - Weaseal.com Mail", _titlePage)
        output = writer("INFO:\tGoogle Gmail Launched", output)
        gmail_title_page_obj.googleApp_Button_click()
        output = writer("INFO:\tClick on GoogleApp menu", output)
        # Move to drop down menu with Action chain, switch to child handle, and click App Gear button
        gmail_title_page_obj.googleApp_Admin_Button_click()
        #self.driver.get_screenshot_as_file('/temp/screenshots/'+'ImportExcludeTest_'+now+'_001png')
        self.take_screenshot('ImportTest_', date, now, 'googleAdminConsolePage_003.png')
        output = writer("INFO:\tClick on Admin Google App Gear", output)
        google_Admin_console_page_obj = GoogleAdminConsolePage(self.driver)
        _titlePage = google_Admin_console_page_obj.get_title()
        self.assertIn("Admin console", _titlePage)
        output = writer("INFO:\tGoogle Admin console Launched", output)
        time.sleep(5)
        google_Admin_console_page_obj.Apps_Button_click()

        google_Apps_settings_page_obj = GoogleAppsSettings(self.driver)
        output = writer("INFO:\tManager Apps (APPS SETTINGS) Launched", output)
        google_Apps_settings_page_obj.MarketPlace_Apps_Button_click()

        ''''Check if Marketplace is there or not'''
        google_Marketplace_apps_page_obj = GoogleMarketplaceAppsPage(self.driver)
        if google_Marketplace_apps_page_obj.check_JostleUSQA_row_exists() == False :
            #output = writer("INFO:\tRemoving Marketplace App from Admin console", output)
            #'''Removing MarketplaceApp'''
            #google_Marketplace_apps_page_obj.JostleUSQA_Link_click()
            #google_Settings_for_JostleUSQA_page_obj = GoogleJostleUSQASettingsPage(self.driver)
            #google_Settings_for_JostleUSQA_page_obj.remove_app_button_click()
            #action = GoogleConfirmRemovalOfAppPage(self.driver)
            #action.confirm_removal_app_button_click()
            #output = writer("INFO:\tMarketplace App Jostle USQA has been removed", output)
            '''#Install MarkPlaceApp'''
            output = writer("INFO:\tInstalling Markerplace App", output)
            marketPlaceInstalApplURL = TT_Constants['Marketplace_Insatall_App_URL']
            self.navigate_to_page(marketPlaceInstalApplURL)
            marketplace_install_app_page_obj = MarketPlaceInstallAppPage(self.driver)
            _titlePage = marketplace_install_app_page_obj.get_title()
            self.assertIn("Jostle USQA App - Google Apps Marketplace", _titlePage)
            output = writer("INFO:\tMarketplace Install App Page show up ", output)
            # time.sleep(5)
            marketplace_install_app_page_obj.install_app_button_click()
            '''Accepting Google's Term of Service'''
            # Get window handles and switch to child window
            allWindowsHandlesList = self.driver.window_handles  # handles[0]: parent - handles[1]: child
            term_service_child_handle = allWindowsHandlesList[2]
            marketplace_install_app_page_obj.switch_to_child_handle(term_service_child_handle)
            # Click agreement checkbox and accept button
            term_of_service_page_obj = TermOfServiceAgreementPage(self.driver)
            term_of_service_page_obj.term_of_service_checkbox_click()
            term_of_service_page_obj.accept_button_click()
            output = writer("INFO:\tJostle USQA App has been installed ", output)
            #Switch back to parent window
            marketplace_install_app_page_obj.switch_to_child_handle(allWindowsHandlesList[1])
        else:
            output = writer("INFO:\tMarketplace has been installed previously", output)
            #time.sleep(5)

        '''#Removing Contributor "Takeuchi Len" and "Chark Wong" from Jostle (Weaseal enterprise)'''
        output = writer("INFO:\tRemoving 'Takeuchi Len' and 'Chark Wong' form Weaseal enterprise", output)
        jostleWeasealLoginPagelURL = TT_Constants['Jostle_Weaseal_URL']
        self.navigate_to_page(jostleWeasealLoginPagelURL)
        jostle_Weaseal_page_obj = JostleWeasealLoginPage(self.driver,
                                                        TT_Constants['Jostle_Weaseal_Username']
                                                        #TT_Constants['Jostle_Weaseal_Password']
                                                        )
        jostle_Weaseal_page_obj.login()
        jostle_Weaseal_title_page_obj = JostleWeasealTitlePage(self.driver)
        _titlePage = jostle_Weaseal_title_page_obj.get_title()
        self.assertIn("weaseal.com - connected by Jostle", _titlePage)
        output = writer("INFO:\t usqa Jostle Weaseal Launched", output)

        global Build
        Build = get_buildno(self.driver)  # must pass self.driver to get_buildno()
        output = writer("BUILD:\t" + Build, output)

        #Get around the welcome popup screens
        try:
            print "INFO:\tTrying to close Welcome popup"
            jostle_Weaseal_title_page_obj.welcomePopupCloseButton_click()
            #return None  # abort function as pop is already closed.
        except TimeoutException:
            pass
        #try:
            #print "INFO:\tTrying to close New feature popup"
            #jostle_Weaseal_title_page_obj.newFeaturePopup_button_click()
            ##return None  # abort function as pop is already closed.
        #except TimeoutException:
            #pass
        #try:
            #print "INFO:\tTrying to close startJostlingNow"
            #jostle_Weaseal_title_page_obj.startJostlingPopup_button_click()
            ##return None  # abort function as pop is already closed.
        #except TimeoutException:
            #pass
        #Click Gear button and Switch to 'QA:AdminFrame'
        jostle_Weaseal_title_page_obj.gear_button_click()
        jostle_Weaseal_administration_settings_page_obj = JostleWeasealAdministrationSettingsPage(self.driver)
        jostle_Weaseal_administration_settings_page_obj.edit_delete_contributors_href_click()
        #jostle_Weaseal_administration_settings_page_obj.search_for_contributor('Len Takeuchi')
        if jostle_Weaseal_administration_settings_page_obj.search_for_contributor('Len Takeuchi') == True:
            output = writer("INFO:\tRemoving 'Chark Wong' from Jostle Weaseal", output)
            #Click delete red button and switch to Alert to confirm of removing contributor
            jostle_Weaseal_administration_settings_page_obj.delete_click()
            _successfully_delete_message = jostle_Weaseal_administration_settings_page_obj.delete_conformation_message()
            self.assertIn("Requested change was successfully performed!", _successfully_delete_message.text)
            output = writer("INFO:\tContributor 'Len Takeuchi' has been removed", output)
        else:
            output = writer("INFO:\tContributor 'Len Takeuchi' not in Jostle Weaseal", output)

        if jostle_Weaseal_administration_settings_page_obj.search_for_contributor('Chark Wong') == True:
            output = writer("INFO:\tRemoving 'Len Takeuchi' from Jostle Weaseal", output)
            # Click delete red button and switch to Alert to confirm of removing contributor
            jostle_Weaseal_administration_settings_page_obj.delete_click()
            _successfully_delete_message = jostle_Weaseal_administration_settings_page_obj.delete_conformation_message()
            self.assertIn("Requested change was successfully performed!", _successfully_delete_message.text)
            output = writer("INFO:\tContributor 'Chark Wong' has been removed", output)
        else:
            output = writer("INFO:\tContributor 'Chark Wong' not in Jostle Weaseal", output)

        time.sleep(2) #for Debuggin

        '''#Go to JostleUSQA Setup Settings and Import 'Len Takeuchi' and 'Chark Wong' '''
        output = writer("INFO:\tExcluding 'Takeuchi Len' form JostleUSQA Setup Setting", output)
        #Go to Config Instance page
        jostleUSQAWeasealSetupSettingsPageURL = TT_Constants['JostleUSQA_Weaseal_Setup_Settings_URL']
        self.navigate_to_page(jostleUSQAWeasealSetupSettingsPageURL)
        #Go to Master Account page - keep dwight@weaseal.com
        jostleUSQA_config_instance_page_obj = JostleUSQAConfigInstancePage(self.driver)
        # Choose your host location "USQA"  #not "Australia"
        jostleUSQA_config_instance_page_obj.choose_your_host_location_click(TT_Constants['HostLocation'])
        jostleUSQA_config_instance_page_obj.continue_button_click()
        #Go to upload your logo page - skip - Step 1
        jostleUSQA_master_account_page_obj = JostleUSQAMasterAccountPage(self.driver)
        jostleUSQA_master_account_page_obj.continue_button_click()
        #Go to Enable API Access page - Step 2
        jostleUSQA_upload_your_logo_page_obj = JostleUSQAUploadLogoPage(self.driver)
        jostleUSQA_upload_your_logo_page_obj.skip_it_link_click()
        #Go to Import your people page - Step 3
        jostleUSQA_api_access_page_obj = JostleUSQAEnableAPIAccessPage(self.driver)
        jostleUSQA_api_access_page_obj.continue_link_click()
        #Click Exclude checkbox and go to Edit Excluded Contributors Page
        jostleUSQA_import_your_people_page_obj = JostleUSQAImportPeoplePage(self.driver)
        jostleUSQA_import_your_people_page_obj.exclude_checkbox_click()
        jostleUSQA_import_your_people_page_obj.edit_blacklist_link_click()
        #Remove "Len" from Exclude list
        jostleUSQA_edit_excluded_contributors_page_obj = JostleUSQAEditExcludedUsersPage(self.driver)
        if jostleUSQA_edit_excluded_contributors_page_obj.remove_selected_option_click('len@') == True:
            jostleUSQA_edit_excluded_contributors_page_obj.remove_selected_list_button_click()
        jostleUSQA_edit_excluded_contributors_page_obj = JostleUSQAEditExcludedUsersPage(self.driver)
        # Remove "Chark" from Exclude list
        if jostleUSQA_edit_excluded_contributors_page_obj.remove_selected_option_click('chark@') == True:
            jostleUSQA_edit_excluded_contributors_page_obj.remove_selected_list_button_click()
        time.sleep(2) #for Debuging
        #click Save
        jostleUSQA_edit_excluded_contributors_page_obj.save_excluded_users_button_click()
        #Back to Import People Page
        self.take_screenshot('ImportTest_', date, now, 'importyourpeoplePage_004.png')
        jostleUSQA_import_your_people_page_obj.import_people_button_click()


        '''#Lanch USQA Weaseal and make sure that 'Len Takeuchi' is not there '''
        #Lanch Jostle Weaseal
        jostleUSQA_quick_setup_complete_page_obj = JostleUSQAQuickSetupCompletePage(self.driver)
        jostleUSQA_quick_setup_complete_page_obj.launch_jostle_button_click()
        jostle_Weaseal_title_page_obj = JostleWeasealTitlePage(self.driver)
        _titlePage = jostle_Weaseal_title_page_obj.get_title()
        self.assertIn("weaseal.com - connected by Jostle", _titlePage)
        output = writer("INFO:\t Jostle Weaseal Launched again for make sure that 'Len' is not there ", output)
        # Get around the welcome popup screens
        try:
            print "INFO:\tTrying to close Welcome popup"
            jostle_Weaseal_title_page_obj.welcomePopupCloseButton_click()
            # return None  # abort function as pop is already closed.
        except TimeoutException:
            pass
        #try:
            #print "INFO:\tTrying to close New feature popup"
            #jostle_Weaseal_title_page_obj.newFeaturePopup_button_click()
            ##return None  # abort function as pop is already closed.
        # except TimeoutException:
            #pass
        #try:
            #print "INFO:\tTrying to close startJostlingNow"
            #jostle_Weaseal_title_page_obj.startJostlingPopup_button_click()
            ##return None  # abort function as pop is already closed.
        # except TimeoutException:
            # pass

        # Click Gear button and Switch to 'QA:AdminFrame'
        jostle_Weaseal_title_page_obj.gear_button_click()
        jostle_Weaseal_administration_settings_page_obj = JostleWeasealAdministrationSettingsPage(self.driver)
        jostle_Weaseal_administration_settings_page_obj.edit_delete_contributors_href_click()
        #Make sure that "Len" has been imported to Weaseal
        if jostle_Weaseal_administration_settings_page_obj.search_for_contributor('Len Takeuchi') == True:
            output = writer("VERIFY:\tContributor 'Len Takeuchi' is in Weaseal.\tPASSED", output)
            res["P"] += 1  # add  1 to pass counter"
            assert(True)
        else:
            output = writer("INFO:\tContributor 'Len Takeuchi' is in Jostle Weaseal, witch is wrong.\tFAILED", output)
            self.take_screenshot('ImportSeveralContributorsTest_', date, now, 'FALEDsearchforImportedLen_000.png')
            self.failIf(True, "Test failed because 'Len Takeuchi' has not been imported for some reason")
        #Make sure that "Chark" ihas been imported to Weaseal
        if jostle_Weaseal_administration_settings_page_obj.search_for_contributor('Chark Wong') == True:
            output = writer("VERIFY:\tContributor 'Chark Wong' is in Weaseal.\tPASSED", output)
            res["P"] += 1  # add  1 to pass counter"
            assert (True)
        else:
            output = writer("VERIFY:\tContributor 'Chark Wong' is in Jostle Weaseal, witch is wrong.\tFAILED",
                            output)
            self.take_screenshot('ImportSeveralContributorsTest_', date, now, 'FALEDsearchforImportedLen_000.png')
            self.failIf(True, "Test failed because 'Chark Wong' has not been imported for some reason")


        time.sleep(5)

        # Test wrap up
        end = time.time()
        global elapsed
        elapsed = end - start
        output = writer("INFO:\ttestResultCount:\t" + str(res["P"]) + "\t/\t" + str(total), output)
        output = writer("INFO:\tTEST\t                                          RESULT\t TIME\t BUILD", output)




if __name__ == "__main__":
    unittest.main()



