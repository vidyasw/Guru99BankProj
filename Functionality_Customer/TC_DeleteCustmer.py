import unittest
import time
from Common_Package.BankApp_CommonFunctons import BankAPP_CommonFunctions
from utility import Excelutility
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TC_DeleteCustomerTest(unittest.TestCase):

    Path = BankAPP_CommonFunctions.excelPath
    SheetName = BankAPP_CommonFunctions.sheet_Profile
    SheetToStore = BankAPP_CommonFunctions.sheet_CustomerID
    SheetToStore_index = 2

    # @classmethod
    # def setUpClass(cls):
    #     cls.driver = webdriver.Chrome(executable_path="E:\\chromedriver_win32\\chromedriver.exe")
    #     cls.driver.maximize_window()
    #     BankAPP_CommonFunctions.login_bankApp(cls.driver, BankAPP_CommonFunctions.username,
    #                                           BankAPP_CommonFunctions.Password)
    #     BankAPP_CommonFunctions.close_popup(cls.driver)

    @staticmethod
    def search_cust_BYID_Delete(driver,id,action):
        driver.find_element_by_xpath("//input[@name='cusid']").send_keys(id)
        driver.find_element_by_css_selector("input[name='AccSubmit']").click()
        time.sleep(2)
        msg = driver.switch_to.alert.text
        if "Do you really want to delete this Customer?" in msg and action == "No":
            print(msg)
            driver.switch_to.alert.dismiss()
        elif "Do you really want to delete this Customer?" in msg and action == "Yes":
            print(msg)
            driver.switch_to.alert.accept()
            wait = WebDriverWait(driver, 35)
            wait.until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
            msgon_deletion = driver.switch_to.alert.text

            if "Customer does not exist!!" in msgon_deletion:
                print(msgon_deletion)
                driver.switch_to.alert.accept()
            elif "Customer deleted Successfully" in msgon_deletion:
                print(msgon_deletion)
                driver.switch_to.alert.accept()

        col, row = Excelutility.search_value_in_column(TC_DeleteCustomerTest.Path, TC_DeleteCustomerTest.SheetToStore,id,"A")
        print("Row {0},Col {1}:".format(row, col))
        total_row = Excelutility.get_row_count(TC_DeleteCustomerTest.Path,TC_DeleteCustomerTest.SheetToStore)
        print("Total Row :",total_row)

        if row != None:
            Excelutility.delete_row(TC_DeleteCustomerTest.Path,TC_DeleteCustomerTest.SheetToStore,row,1)
        '''print("done")
        afterdelete = Excel_utility.get_row_count(TC_DeleteCustomerTest.Path,TC_DeleteCustomerTest.SheetToStore)
        print(afterdelete)
        print("1st condition:", afterdelete == total_row-1)
        id_new = Excel_utility.read_data(TC_DeleteCustomerTest.Path,TC_DeleteCustomerTest.SheetToStore,row, 1)
        print(id_new)
        print("2nd condition:",id_new != id)'''
        if Excelutility.get_row_count(TC_DeleteCustomerTest.Path,TC_DeleteCustomerTest.SheetToStore) == total_row-1 and Excel_utility.read_data(TC_DeleteCustomerTest.Path,TC_DeleteCustomerTest.SheetToStore,row, 1) != id:
            print(id + " got deleted from xls")
        elif Excelutility.get_row_count(TC_DeleteCustomerTest.Path,TC_DeleteCustomerTest.SheetToStore) == total_row:
            print(id + " not found in excel or already deleted!!!")

    '''def test_DeleteCust(self):
        try:
            BankAPP_CommonFunctions.click_menu_by_partial_link_text(self.driver, "Delete Cust", "Delete Customer")
            self.search_cust_BYID_Delete(self.driver,"2726","Yes")
        except Exception as e:
            print("Exception from Delete Customer:", type(e).__name__)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)'''

    # @classmethod
    # def tearDownClass(cls):
    #     BankAPP_CommonFunctions.close_popup(cls.driver)
    #     BankAPP_CommonFunctions.logout(cls.driver)
    #     cls.driver.implicitly_wait(1)
    #     cls.driver.close()

# if __name__ == "__main__":
#     unittest.main()

