import unittest
from Common_Package.BankApp_CommonFunctons import BankAPP_CommonFunctions
from utility import Excelutility


class TC_EditCustmerTest(unittest.TestCase):
    # driver = webdriver.Chrome(executable_path="E:\chromedriver_win32\chromedriver.exe")
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
    def search_cust_BYID(driver, id):
        driver.find_element_by_name("cusid").send_keys(id)
        driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr/td/table/tbody/tr[11]/td[2]/input[1]").click()
        driver.implicitly_wait(2)
        driver.set_page_load_timeout(20)
        return driver.find_element_by_name("sub").is_displayed()

    @staticmethod
    def edit_address(driver, id):
        address_field = driver.find_element_by_name("addr")
        prsentaddr = address_field.text

        address_field.clear()
        driver.implicitly_wait(1)
        to_update_addr = prsentaddr + " A"

        address_field.send_keys(to_update_addr)
        driver.find_element_by_name("sub").click()
        driver.implicitly_wait(1)
        msg = driver.find_element_by_xpath("//*[@id='customer']/tbody/tr[1]/td/p").text
        if "Customer details updated Successfully!!!" in msg:
            print(msg)
        add_filed = driver.find_element_by_xpath("//*[@id='customer']/tbody/tr[8]/td[2]")
        updated_address = add_filed.text
        if prsentaddr != updated_address:
            print("New Address got updated in Bank app for " + id)
        else:
            print("Address wrongly updated or not updated")
        driver.implicitly_wait(1)
        col, row = Excelutility.search_value_in_column(TC_EditCustmerTest.Path, TC_EditCustmerTest.SheetToStore, id,
                                                        "A")
        # print("col,row:",col,row)
        Excelutility.write_data(TC_EditCustmerTest.Path, TC_EditCustmerTest.SheetToStore, row, 5, updated_address)
        changed_val_in_xl = Excelutility.read_data(TC_EditCustmerTest.Path, TC_EditCustmerTest.SheetToStore, row, 5)
        if changed_val_in_xl == updated_address:
            print("New Address got updated in excel for " + id)

    '''def test_edit_customer(self):
        try:
            BankAPP_CommonFunctions.click_menu_by_partial_link_text(self.driver, "Edit Cust", "Edit Customer")
            cust_id_modify = BankAPP_CommonFunctions.get_cust_id_frm_repo("LastAdded_CustID.txt",0)
            boolTrue = self.search_cust_BYID(self.driver,cust_id_modify)
            print(boolTrue)
            self.edit_address(self.driver,cust_id_modify)
            # Click Continue
            self.driver.find_element_by_xpath("//*[@id='customer']/tbody/tr[14]/td/a").click()

            self.driver.implicitly_wait(1)
        except Exception as e:
            print("Exception from Edit Customer:", type(e).__name__)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)'''

    # @classmethod
    # def tearDownClass(cls):
    #     BankAPP_CommonFunctions.close_popup(cls.driver)
    #     BankAPP_CommonFunctions.logout(cls.driver)
    #     cls.driver.implicitly_wait(1)
    #     cls.driver.close()

# if __name__ == "__main__":
#     unittest.main()