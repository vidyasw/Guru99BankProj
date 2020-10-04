import sys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from utility.Excelutility import Excel_utility
from Common_Package.BankApp_CommonFunctons import BankAPP_CommonFunctions
from selenium import webdriver
import unittest
import datetime


class TC_DepositeTest(unittest.TestCase):

    Path = "C:\\Users\\Sony\\PycharmProjects\\Guru99BankProj\\NavigationValidation.xlsx"
    Sheet_Name = "Account_Details"

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path="E:\\chromedriver_win32\\chromedriver.exe")
        cls.driver.maximize_window()
        BankAPP_CommonFunctions.login_bankApp(cls.driver, "mngr259708", "YmEgYge")
        BankAPP_CommonFunctions.close_popup(cls.driver)

    @staticmethod
    def validate_deposite_details(driver,acc_id,amount_credited,desc_added):
        if "Transaction details of Deposit for Account " + id in driver.find_element_by_xpath("//*[@id='deposit']/tbody/tr[1]/td/p").text:
            print("Added deposit successfully")

            acc_id_col,acc_id_row = Excel_utility.search_value_in_column(TC_DepositeTest.Path, TC_DepositeTest.Sheet_Name,acc_id,"B")
            tranjaction_id = driver.find_element_by_xpath("//*[@id='deposit']/tbody/tr[6]/td[2]").text
            Excel_utility.write_data(TC_DepositeTest.Path,TC_DepositeTest.Sheet_Name,acc_id_row,6,tranjaction_id)

            amount_cr = driver.find_element_by_xpath("//*[@id ='deposit']/tbody/tr[12]/td[2]").text
            if int(amount_cr) == int(amount_credited):
                Excel_utility.write_data(TC_DepositeTest.Path, TC_DepositeTest.Sheet_Name, acc_id_row, 7, amount_cr)
            else:
                print("Amount is not matching")

            type_tranjaction = driver.find_element_by_xpath("//*[@id='deposit']/tbody/tr[16]/td[2]").text == "Deposit"
            Excel_utility.write_data(TC_DepositeTest.Path, TC_DepositeTest.Sheet_Name, acc_id_row, 8, type_tranjaction)
            tranjaction_date = datetime.datetime.now()
            print(tranjaction_date)
            Excel_utility.write_data(TC_DepositeTest.Path,TC_DepositeTest.Sheet_Name,acc_id_row,9,tranjaction_date)

            desc_tranjaction = driver.find_element_by_xpath("//*[@id='deposit']/tbody/tr[20]/td[2]").text
            if desc_tranjaction == desc_added:
                Excel_utility.write_data(TC_DepositeTest.Path,TC_DepositeTest.Sheet_Name,acc_id_row,10,desc_tranjaction)
            else:
                print(desc_added + "is not matching with "+ desc_tranjaction)

            cur_balance = driver.find_element_by_xpath("//*[@id='deposit']/tbody/tr[23]/td[2]").text
            ini_amount = Excel_utility.read_data(TC_DepositeTest.Path,TC_DepositeTest.Sheet_Name,acc_id_row,5)
            if int(cur_balance) == int(ini_amount) + int(amount_cr):
                print("Curent balance is " + cur_balance)
                Excel_utility.write_data(TC_DepositeTest.Path, TC_DepositeTest.Sheet_Name, acc_id_row,11, cur_balance)
            else:
                print("Current balance is not matching")

            print("Validation is done of tranjaction "+ tranjaction_id + " done for account id " + acc_id + " of type " + type_tranjaction + " Successfully!!!")

    @staticmethod
    def add_deposit_to_accountid(driver,acc_id,amt_deposit,desc_deposit):
        driver.find_element_by_name("accountno").send_keys(acc_id)
        driver.find_element_by_name("ammount").send_keys(amt_deposit)
        driver.find_element_by_name("desc").send_keys(desc_deposit)
        driver.find_element_by_name("AccSubmit").click()

        driver.set_page_load_timeout(20)
        success_msg = driver.find_element_by_xpath("//*[@id='deposit']/tbody/tr[1]/td/p").text
        return success_msg == "Transaction details of Deposit for Account " + acc_id


    def test_deposite_money(self):
        try:
            #BankAPP_CommonFunctions.click_menu_by_partial_link_text(self.driver,"Deposit","Deposit")
            parent = self.driver.find_element_by_class_name("menusubnav")
            list_links = parent.find_elements(By.TAG_NAME,"a")
            for link in list_links:
                if link.text == "Deposit":
                    print("Reached")
                    size = link.size
                    print(size)
                    ac = ActionChains(self.driver)
                    ac.move_to_element_with_offset(link,int(size["width"])/ 2 + 2, int(size["height"])/ 2 + 2).click(link)
                    #ac.move_ToElement(link).moveByOffset((width / 2) + 2, (height / 2) + 2).click();
                    #ac.move_to_element(link).move_by_offset(, y_offset).click().perform()
            #acc_id = BankAPP_CommonFunctions.get_cust_id_frm_repo("LastAdded_AccountID_CustID.txt", 1)
            #TC_DepositeTest.add_deposit_to_accountid(self.driver,acc_id,"1000","Deposit done")
            #TC_DepositeTest.validate_deposite_details(self.driver,acc_id,1000,"Deposit done")

            # click continue
            #self.driver.find_element_by_xpath("//*[@id='account']/tbody/tr[11]/td/a").click()
            self.driver.implicitly_wait(1)
        except Exception as e:
            print("Exception found in deposite money test method :",type(e).__name__)
            print('Error on line {} of '+ __name__ + " of class ".format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    @classmethod
    def tearDownClass(cls):
        BankAPP_CommonFunctions.close_popup(cls.driver)
        #BankAPP_CommonFunctions.logout(cls.driver)
        cls.driver.implicitly_wait(1)
        #cls.driver.close()


if __name__ == "__main__":
    unittest.main()