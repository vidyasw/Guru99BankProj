import sys
import unittest
from Common_Package.BankApp_CommonFunctons import BankAPP_CommonFunctions
from utility.Excelutility import Excel_utility
from selenium import webdriver


class TC_BalanceEnquiryTest(unittest.TestCase):

    Path = BankAPP_CommonFunctions.excelPath
    Sheet_Name = BankAPP_CommonFunctions.sheet_AccountDetails

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path="E:\\chromedriver_win32\\chromedriver.exe")
        cls.driver.maximize_window()
        BankAPP_CommonFunctions.login_bankApp(cls.driver, BankAPP_CommonFunctions.username,
                                              BankAPP_CommonFunctions.Password)
        BankAPP_CommonFunctions.close_popup(cls.driver)


    def query_balance_enquiry(self,acc_id):
        self.driver.find_element_by_name("accountno").send_keys(acc_id)
        self.driver.find_element_by_name("accountno").click()
        is_display = self.driver.find_element_by_xpath("//*[@id='balenquiry']/tbody/tr[1]/td/p").is_displayed()
        print(is_display)
        return is_display

    def validate_balance_excelrepo(self,acc_id):
        if "Balance Details for Account " + acc_id in self.driver.find_element_by_xpath("//*[@id='balenquiry']/tbody/tr[1]/td/p").text:
            print("Balance has dispalyed for " + acc_id)

        acc_id_col, acc_id_row = Excel_utility.search_value_in_column(TC_BalanceEnquiryTest.Path,
                                                                      TC_BalanceEnquiryTest.Sheet_Name,acc_id, "B")



    def test_enquire_balance(self):
        try:
            BankAPP_CommonFunctions.click_menu_by_partial_link_text("Balance Enq", "Balance Enquiry")

        except Exception as e:
            print("Exception found in balance enquiry test method :", type(e).__name__)
            print('Error on line {} of ' + __name__ + " of class ".format(sys.exc_info()[-1].tb_lineno),
                  type(e).__name__, e)

    @classmethod
    def tearDownClass(cls):
        BankAPP_CommonFunctions.close_popup(cls.driver)
        # BankAPP_CommonFunctions.logout(cls.driver)
        cls.driver.implicitly_wait(1)
        # cls.driver.close()


if __name__ == "__main__":
    unittest.main()

