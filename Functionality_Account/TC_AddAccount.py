import os
from enum import Enum
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Common_Package.BankApp_CommonFunctons import BankAPP_CommonFunctions
from utility import Excelutility


def store_accid_custid(acc_id,cust_id):
    print("\nWriting cust_id and acc_id Information : ")

    last_added_custid_file_path = "E:\\Vidyashri\\PythonSeleniumProjects\\Guru99BankProj\\Common_Package"
    last_added_custaccid_file_name = "LastAdded_AccountID_CustID.txt"

    if not os.path.exists(last_added_custid_file_path):
        os.mkdir(last_added_custid_file_path)

    print("cust_id file Name : ", last_added_custaccid_file_name)

    custaccid_file_absolute_path = Path(last_added_custid_file_path) / last_added_custaccid_file_name
    print("cust_id file Absolute Path : ", custaccid_file_absolute_path)

    print("Writing to cust_id,acc_id into File")
    file = open(custaccid_file_absolute_path, "w+")
    file.write("Custmer Id : " + cust_id + '\n')
    file.write("Account Id : " + acc_id)
    file.close()


class account(Enum):
    Savings = 0
    Current = 1


def get_accountype_index(account_type):
    index = None
    if account_type == "Savings":
        savings = account.Savings #self.account.Savings
        index = savings.value
    elif account_type == "Current":
        current = account.Current  #self.account.Current
        index = current.value
    else:
        print("Wrong ACcount Type Entered!!")
    return index


class TC_AddAccountTest(unittest.TestCase):

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
    def add_account_details(driver,cust_id,account_type,initial_amt):
        driver.find_element_by_xpath("//input[@name='cusid']").send_keys(cust_id)

        select = Select(driver.find_element_by_name("selaccount"))
        account = get_accountype_index(account_type)
        select.select_by_index(account)
        # select.select_by_index(0)

        driver.find_element_by_name("inideposit").send_keys(initial_amt)

        # Submit button
        driver.find_element_by_name("button2").click()

        wait = WebDriverWait(driver, 55)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='account']/tbody/tr[1]/td/p")))

        return account_type,initial_amt

    @staticmethod
    def validate_account_info(driver,account_type,initial_amount):
        if "Account Generated Successfully!!!" in driver.find_element_by_xpath("//*[@id='account']/tbody/tr[1]/td/p").text:
            print("Added Account successfully")

            row = Excelutility.get_row_count(TC_AddAccountTest.Path, TC_AddAccountTest.Sheet_Name)
            acc_id = driver.find_element_by_xpath("//*[@id='account']/tbody/tr[4]/td[2]").text
            Excelutility.write_data(TC_AddAccountTest.Path,TC_AddAccountTest.Sheet_Name,row+1,2,acc_id)

            cust_id = driver.find_element_by_xpath("//*[@id='account']/tbody/tr[5]/td[2]").text
            Excelutility.write_data(TC_AddAccountTest.Path,TC_AddAccountTest.Sheet_Name,row+1,1,cust_id)
            store_accid_custid(acc_id,cust_id)

            col_inCustID,row_inCustID =Excelutility.search_value_in_column(TC_AddAccountTest.Path,TC_AddAccountTest.Sheet_Verify,cust_id,"A")
            cust_name = driver.find_element_by_xpath("//*[@id ='account']/tbody/tr[6]/td[2]").text
            cust_nameFromXl = Excelutility.read_data(TC_AddAccountTest.Path, TC_AddAccountTest.Sheet_Verify, row_inCustID, 2)
            if cust_name == cust_nameFromXl:
                print(cust_name+" is matching Of id "+ cust_id + " from " +TC_AddAccountTest.Sheet_Verify)
            else:
                print("Customer name is not matching")
            TC_AddAccountTest.assertTrue(cust_name == cust_nameFromXl,cust_name + " is matching with id " + cust_id)

            cust_mail = driver.find_element_by_xpath("//*[@id ='account']/tbody/tr[7]/td[2]").text
            cust_mailFromXl = Excelutility.read_data(TC_AddAccountTest.Path, TC_AddAccountTest.Sheet_Verify, row_inCustID, 10)
            if cust_mail == cust_mailFromXl:
                print(cust_mail+" is matching of id "+ cust_id + " from " + TC_AddAccountTest.Sheet_Verify)
            else:
                print("Customer mail is not matching")
            TC_AddAccountTest.assertTrue(cust_mail == cust_mailFromXl,cust_mail + " is matching with id " + cust_id)

            acc_type = driver.find_element_by_xpath("//*[@id ='account']/tbody/tr[8]/td[2]").text
            if acc_type == account_type:
                Excelutility.write_data(TC_AddAccountTest.Path, TC_AddAccountTest.Sheet_Name, row + 1, 3, acc_type)
            else:
                print("Account type is not matching")

            date_of_opening = driver.find_element_by_xpath("//*[@id ='account']/tbody/tr[9]/td[2]").text
            Excelutility.write_data(TC_AddAccountTest.Path, TC_AddAccountTest.Sheet_Name, row + 1, 4, date_of_opening)

            cur_amount = driver.find_element_by_xpath("//*[@id='account']/tbody/tr[10]/td[2]").text
            #print(cur_amount)
            #print(initial_amount)
            if int(cur_amount) == int(initial_amount):
                print("Initial amount added " + cur_amount)
                Excelutility.write_data(TC_AddAccountTest.Path, TC_AddAccountTest.Sheet_Name, row + 1, 5, cur_amount)
            else:
                print("Initial amount is not matching")

            print("Validation is done for added account " + acc_id + " of type " + acc_type + " Successfully!!!")

    '''def test_addition_new_account(self):
        try:
            BankAPP_CommonFunctions.click_menu_by_perform_mouse_action(self.driver, "New Acc", "new account")
            cust_id = BankAPP_CommonFunctions.get_cust_id_frm_repo("LastAdded_CustID.txt",0)
            account_type,initial_amt = self.add_account_details(self.driver,cust_id,"Current",3000)
            print(account_type,initial_amt )
            self.validate_account_info(self.driver,account_type,initial_amt)

            # click continue
            self.driver.find_element_by_xpath("//*[@id='account']/tbody/tr[11]/td/a").click()
            self.driver.implicitly_wait(1)

        except Exception as e:
            print("Exception from AddAccount : ", type(e).__name__)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)'''

    # @classmethod
    # def tearDownClass(cls):
    #     BankAPP_CommonFunctions.close_popup(cls.driver)
    #     BankAPP_CommonFunctions.logout(cls.driver)
    #     cls.driver.implicitly_wait(1)
    #     cls.driver.close()


# if __name__ == "__main__":
#     unittest.main()