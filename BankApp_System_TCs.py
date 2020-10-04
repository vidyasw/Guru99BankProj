from Common_Package.BankApp_CommonFunctons import BankAPP_CommonFunctions
from Functionality_MenuClick.TC_MenuClickingInSequence import TC_MenuClickInSequenceTest
from Functionality_Navigation.TC_NavigationValidation import TC_NavigationValidationTest
from Functionality_Customer.TC_AddCustomer import TC_AddCustomerTest
from Functionality_Customer.TC_EditCustomer import TC_EditCustmerTest
from Functionality_Customer.TC_DeleteCustmer import TC_DeleteCustomerTest
from Functionality_Account.TC_AddAccount import TC_AddAccountTest
from Functionality_Account.TC_EditAccount import TC_EditAccountTest
from Functionality_Account.TC_DeleteAccount import TC_DeleteAccountTest
from selenium import webdriver
import unittest
import HtmlTestRunner


class BankApp_System_AllTC_Test(unittest.TestCase):

    Path = BankAPP_CommonFunctions.excelPath
    SheetName = BankAPP_CommonFunctions.sheet_NavigationValidation
    url = BankAPP_CommonFunctions.url

    @classmethod
    def setUp(self):
        print("Setup called........")
        self.driver = webdriver.Chrome() # executable_path="E:\\chromedriver_win32\\chromedriver.exe"
        self.driver.get(self.url)
        self.driver.set_page_load_timeout(10)
        self.driver.maximize_window()

    def test_2menu_click_Validation_in_sequence(self):
        print("2menu_click_Validation_in_sequence called........")
        BankAPP_CommonFunctions.login_bankApp(self.driver, BankAPP_CommonFunctions.username,
                                              BankAPP_CommonFunctions.Password)
        BankAPP_CommonFunctions.close_popup(self.driver)

        dict_menu = {"Manag": "Manager", "New Cust": "New Customer", "Edit Cust": "Edit Customer",
                     "Delete Cust": "Delete Customer",
                     "New Acc": "new account", "Edit Acc": "Edit Account", "Delete Acc": "Delete Account",
                     "Deposit": "Deposit",
                     "Withdrawal": "Withdrawal", "Fund Transfer": "Fund transfer", "Change Pass": "Change Password",
                     "Balance Enq": "Balance Enquiry",
                     "Mini State": "Mini Statement", "Customised State": "Customized Statement"}

        TC_MenuClickInSequenceTest.menu_click_sequence(self.driver,dict_menu)
        BankAPP_CommonFunctions.logout(self.driver)

    def test_1validationNavigation(self):
        print("1validationNavigation called")
        TC_NavigationValidationTest.login_with_diff_credentials(self.driver,self.Path,self.SheetName,self.url)

    def test_3add_customer(self):
        print("3add_customer called..........")
        BankAPP_CommonFunctions.login_bankApp(self.driver, BankAPP_CommonFunctions.username,
                                              BankAPP_CommonFunctions.Password)
        BankAPP_CommonFunctions.click_menu_by_partial_link_text(self.driver, "New Cust", "New Customer")
        TC_AddCustomerTest.add_customer(self.driver, "M")
        TC_AddCustomerTest.validate_custinfo(self.driver)

        # Click Continue
        self.driver.find_element_by_xpath("//*[@id='customer']/tbody/tr[14]/td/a").click()
        self.driver.implicitly_wait(1)
        BankAPP_CommonFunctions.logout(self.driver)

    def test_4edit_customer(self):
        print("4edit_customer................")
        BankAPP_CommonFunctions.login_bankApp(self.driver, BankAPP_CommonFunctions.username,
                                              BankAPP_CommonFunctions.Password)
        BankAPP_CommonFunctions.click_menu_by_partial_link_text(self.driver, "Edit Cust", "Edit Customer")
        cust_id_modify = BankAPP_CommonFunctions.get_cust_id_frm_repo("LastAdded_CustID.txt", 0)
        bool_true = TC_EditCustmerTest.search_cust_BYID(self.driver,cust_id_modify)
        print("ID has Searched?:",bool_true)

        TC_EditCustmerTest.edit_address(self.driver,cust_id_modify)
        # Click Continue
        self.driver.find_element_by_xpath("//*[@id='customer']/tbody/tr[14]/td/a").click()
        self.driver.implicitly_wait(1)
        BankAPP_CommonFunctions.logout(self.driver)

    def test_5delete_customer(self):
        print("5delete_customer called..............")
        BankAPP_CommonFunctions.login_bankApp(self.driver, BankAPP_CommonFunctions.username,
                                              BankAPP_CommonFunctions.Password)
        BankAPP_CommonFunctions.click_menu_by_partial_link_text(self.driver, "Delete Cust", "Delete Customer")
        TC_DeleteCustomerTest.search_cust_BYID_Delete(self.driver, "19943", "Yes")
        BankAPP_CommonFunctions.logout(self.driver)

    def test_6add_account(self):
        print("6add_account called............")
        BankAPP_CommonFunctions.login_bankApp(self.driver, BankAPP_CommonFunctions.username,
                                              BankAPP_CommonFunctions.Password)
        BankAPP_CommonFunctions.close_popup(self.driver)
        BankAPP_CommonFunctions.click_menu_by_perform_mouse_action(self.driver, "New Acc", "new account")
        cust_id = BankAPP_CommonFunctions.get_cust_id_frm_repo("LastAdded_CustID.txt", 0)
        account_type, initial_amt = TC_AddAccountTest.add_account_details(self.driver, cust_id, "Current", 3000)
        print(account_type, initial_amt)
        TC_AddAccountTest.validate_account_info(self.driver, account_type, initial_amt)

        # Click continue
        self.driver.find_element_by_xpath("//*[@id='account']/tbody/tr[11]/td/a").click()
        self.driver.implicitly_wait(1)
        BankAPP_CommonFunctions.logout(self.driver)

    def test_7edit_account(self):
        print("7edit_account called........")
        BankAPP_CommonFunctions.login_bankApp(self.driver, BankAPP_CommonFunctions.username,
                                              BankAPP_CommonFunctions.Password)
        BankAPP_CommonFunctions.close_popup(self.driver)
        BankAPP_CommonFunctions.click_menu_by_partial_link_text(self.driver, "Edit Acc", "Edit Account")
        acc_id = BankAPP_CommonFunctions.get_cust_id_frm_repo("LastAdded_AccountID_CustID.txt", 1)
        searched = TC_EditAccountTest.search_account_BYID(self.driver, acc_id)
        print(searched)
        TC_EditAccountTest.edit_account_type(self.driver)

        # Click continue
        self.driver.find_element_by_xpath("//*[@id='account']/tbody/tr[11]/td/a").click()
        self.driver.implicitly_wait(1)
        BankAPP_CommonFunctions.logout(self.driver)

    def test_8delete_account(self):
        print("8delete_account called............")
        BankAPP_CommonFunctions.login_bankApp(self.driver, BankAPP_CommonFunctions.username,
                                              BankAPP_CommonFunctions.Password)
        BankAPP_CommonFunctions.close_popup(self.driver)
        account_id_delete = TC_DeleteAccountTest.create_dummy_account(self.driver)
        print("Acc id to delete:",account_id_delete)
        BankAPP_CommonFunctions.click_menu_by_partial_link_text(self.driver, "Delete Acc", "Delete Account")
        TC_DeleteAccountTest.search_acc_BYID_Delete(self.driver, account_id_delete, "Yes")
        BankAPP_CommonFunctions.logout(self.driver)

    @classmethod
    def tearDown(self):
        print("teardown called........")
        self.driver.close()


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='E:\\Vidyashri\\PythonSeleniumProjects'
                                                                  '\\Guru99BankProj\\Execution_Reports\\HTML_Reports'))