import time
import unittest
from selenium.webdriver.common.by import By
from Common_Package.BankApp_CommonFunctons import BankAPP_CommonFunctions
from utility import Excelutility
from selenium.webdriver.support.ui import Select


class TC_EditAccountTest(unittest.TestCase):

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
    def search_account_BYID(driver,acc_id):
        driver.find_element_by_name("accountno").send_keys(acc_id)
        driver.find_element_by_name("AccSubmit").click()
        time.sleep(1)
        driver.set_page_load_timeout(20)
        form_name = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[1]/td/p").text
        return form_name == "Edit Account Entry Form"

    @staticmethod
    def get_current_account_type(driver):
        combo_options = driver.find_elements(By.TAG_NAME,"option")
        #option1 = self.driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[11]/td[2]/select/option[1]")
        #option2 = self.driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[11]/td[2]/select/option[2]")
        #print("Option Name:", option2.text)
        #att = option2.get_attribute("selected")
        #val = option1.get_attribute("value")
        #print("option2:",att)
        #print(val)
        for option in combo_options:
            print("List item:",option.text)
            if option.get_attribute("selected"):
                print(option.text + " account type has selected in account combo")
                return option.text
        return None

    @staticmethod
    def edit_account_type(driver):
        present_acc_type = TC_EditAccountTest.get_current_account_type(driver)
        print("Present Account type is:",present_acc_type)

        # Set the string as exactly differnt than present
        to_update_acc_type = None
        if present_acc_type == "Current":
            to_update_acc_type = "Savings"
        elif present_acc_type == "Savings":
            to_update_acc_type = "Current"
        print("To update with :",to_update_acc_type)

        # select the value as per to_update_acc_type veriable
        select = Select(driver.find_element_by_name("a_type"))
        select.select_by_value(to_update_acc_type)
        time.sleep(1)

        driver.find_element_by_name("AccSubmit").click()
        time.sleep(1)
        msg = driver.find_element_by_xpath("//*[@id='account']/tbody/tr[1]/td/p").text
        if "Account details updated Successfully!!!" in msg:
            print(msg)

        updated_acc_type = driver.find_element_by_xpath("//*[@id='account']/tbody/tr[8]/td[2]").text #self.get_current_account_type()
        print("After Update: " + updated_acc_type)

        if present_acc_type != updated_acc_type:
            print("Account type got updated in Bank app with " + updated_acc_type)
        else:
            print("Account type not updated with " + updated_acc_type)

        acc_id = driver.find_element_by_xpath("//*[@id='account']/tbody/tr[4]/td[2]").text
        col,row = Excelutility.search_value_in_column(TC_EditAccountTest.Path,TC_EditAccountTest.Sheet_Name,acc_id,"B")
        print("col,row:",col,row)
        Excelutility.write_data(TC_EditAccountTest.Path,TC_EditAccountTest.Sheet_Name, row, 3, updated_acc_type)

        changed_val_in_xl = Excelutility.read_data(TC_EditAccountTest.Path,TC_EditAccountTest.Sheet_Name,row,3)
        if changed_val_in_xl == updated_acc_type:
            print("New account type got updated in excel with type " + updated_acc_type)

    '''def test_Edit_account(self):
        try:
            BankAPP_CommonFunctions.click_menu_by_partial_link_text(self.driver,"Edit Acc","Edit Account")
            acc_id = BankAPP_CommonFunctions.get_cust_id_frm_repo("LastAdded_AccountID_CustID.txt", 1)
            seraced = self.search_account_BYID(self.driver,acc_id)
            print(seraced)
            self.edit_account_type(self.driver)

            # click continue
            self.driver.find_element_by_xpath("//*[@id='account']/tbody/tr[11]/td/a").click()
            self.driver.implicitly_wait(1)

        except Exception as e:
            print("Exception from Edit Account:", type(e).__name__)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)'''

    # @classmethod
    # def tearDownClass(cls):
    #     BankAPP_CommonFunctions.close_popup(cls.driver)
    #     BankAPP_CommonFunctions.logout(cls.driver)
    #     cls.driver.implicitly_wait(1)
    #     cls.driver.close()


# if __name__ == "__main__":
#     unittest.main()