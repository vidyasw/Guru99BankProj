import time
import unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Common_Package.BankApp_CommonFunctons import BankAPP_CommonFunctions
from utility import Excelutility
from Functionality_Account.TC_AddAccount import TC_AddAccountTest


class TC_DeleteAccountTest(unittest.TestCase):

    Path = BankAPP_CommonFunctions.excelPath
    Sheet_Name = BankAPP_CommonFunctions.sheet_AccountDetails
    Sheet_Verify = BankAPP_CommonFunctions.sheet_CustomerID

    # @classmethod
    # def setUpClass(cls):
    #     cls.driver = webdriver.Chrome(executable_path="E:\\chromedriver_win32\\chromedriver.exe")
    #     cls.driver.maximize_window()
    #     BankAPP_CommonFunctions.login_bankApp(cls.driver, BankAPP_CommonFunctions.username,
    #                                           BankAPP_CommonFunctions.Password)
    #     BankAPP_CommonFunctions.close_popup(cls.driver)

    @staticmethod
    def create_dummy_account(driver):
        total_row = Excelutility.get_row_count(TC_DeleteAccountTest.Path,TC_DeleteAccountTest.Sheet_Name)
        print("Total Row:",total_row)
        last_cust_id = Excelutility.read_data(TC_DeleteAccountTest.Path,TC_DeleteAccountTest.Sheet_Name,total_row,1)
        print("Last Cust Id :",last_cust_id)
        BankAPP_CommonFunctions.close_popup(driver)
        BankAPP_CommonFunctions.click_menu_by_perform_mouse_action(driver, "New Acc", "new account")
        TC_AddAccountTest.add_account_details(driver,last_cust_id,"Savings",3000)
        TC_AddAccountTest.validate_account_info(driver,"Savings",3000)
        total_row_after_addition = Excelutility.get_row_count(TC_DeleteAccountTest.Path, TC_DeleteAccountTest.Sheet_Name)
        print("Total row in excel after adding new account:",total_row_after_addition)
        account_id_to_delete = Excelutility.read_data(TC_DeleteAccountTest.Path,TC_DeleteAccountTest.Sheet_Name,
                                                       total_row_after_addition,2)
        print("Account Id to delete is :",account_id_to_delete)
        return account_id_to_delete

    @staticmethod
    def search_acc_BYID_Delete(driver, id, action):
        driver.find_element_by_name("accountno").send_keys(id)
        driver.find_element_by_css_selector("input[name='AccSubmit']").click()
        time.sleep(2)
        msg = driver.switch_to.alert.text
        if "Do you really want to delete this Account?" in msg and action == "No":
            print(msg)
            driver.switch_to.alert.dismiss()
        elif "Do you really want to delete this Account?" in msg and action == "Yes":
            print(msg)
            driver.switch_to.alert.accept()
            wait = WebDriverWait(driver, 35)
            wait.until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
            msgon_deletion = driver.switch_to.alert.text

            if "Account does not exist" in msgon_deletion:
                print(msgon_deletion)
                driver.switch_to.alert.accept()
            elif "Account Deleted Sucessfully" in msgon_deletion:
                print(msgon_deletion)
                driver.switch_to.alert.accept()
                driver.implicitly_wait(1)

        col, row = Excelutility.search_value_in_column(TC_DeleteAccountTest.Path, TC_DeleteAccountTest.Sheet_Name,
                                                        id, "B")
        print("Row {0},Col {1}:".format(row, col))
        total_row = Excelutility.get_row_count(TC_DeleteAccountTest.Path, TC_DeleteAccountTest.Sheet_Name)
        print("Total Row :", total_row)

        if row != None:
            Excelutility.delete_row(TC_DeleteAccountTest.Path, TC_DeleteAccountTest.Sheet_Name, row, 1)

        if Excelutility.get_row_count(TC_DeleteAccountTest.Path,
                                       TC_DeleteAccountTest.Sheet_Name) == total_row - 1 and Excelutility.read_data(
                TC_DeleteAccountTest.Path, TC_DeleteAccountTest.Sheet_Name, row, 1) != id:
            print(id + " got deleted from xls")
        elif Excelutility.get_row_count(TC_DeleteAccountTest.Path, TC_DeleteAccountTest.Sheet_Name) == total_row:
            print(id + " not found in excel or already deleted!!!")

    '''def test_delete_account(self):
        try:
            account_id_delete = TC_DeleteAccountTest.create_dummy_account(self.driver)
            BankAPP_CommonFunctions.click_menu_by_partial_link_text(self.driver,"Delete Acc","Delete Account")
            TC_DeleteAccountTest.search_acc_BYID_Delete(self.driver,account_id_delete,"Yes")
            #TC_DeleteAccountTest.search_acc_BYID_Delete(self.driver,"78433","Yes")
        except Exception as e:
            print("Exception from Delete Account:", type(e).__name__)
            print('Error on line {} '.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)'''

    # @classmethod
    # def tearDownClass(cls):
    #     BankAPP_CommonFunctions.close_popup(cls.driver)
    #     BankAPP_CommonFunctions.logout(cls.driver)
    #     cls.driver.implicitly_wait(1)
    #     cls.driver.close()


# if __name__ == "__main__":
#     unittest.main()