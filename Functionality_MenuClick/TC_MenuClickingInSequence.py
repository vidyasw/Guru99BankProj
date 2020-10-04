import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Common_Package.BankApp_CommonFunctons import BankAPP_CommonFunctions


class TC_MenuClickInSequenceTest(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     cls.driver = webdriver.Chrome(executable_path="E:\\chromedriver_win32\\chromedriver.exe")
    #     cls.driver.maximize_window()
    #     BankAPP_CommonFunctions.login_bankApp(cls.driver, BankAPP_CommonFunctions.username,
    #                                           BankAPP_CommonFunctions.Password)
    #     BankAPP_CommonFunctions.close_popup(cls.driver)

    @staticmethod
    def click_menu(driver,menuname):
        if driver.find_element(By.PARTIAL_LINK_TEXT, menuname).is_enabled():
            driver.find_element(By.PARTIAL_LINK_TEXT, menuname).click()
            time.sleep(1)
            print("Clicked ", menuname)
        else:
            wait = WebDriverWait(driver, 15)
            wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, menuname)))
            driver.find_element(By.PARTIAL_LINK_TEXT, menuname).click()
            time.sleep(1)
            print("Clicked ", menuname)

    @staticmethod
    def getlist_menu(driver):
        main_menu = driver.find_element_by_class_name("menusubnav")
        element_list = main_menu.find_elements(By.TAG_NAME, "a")
        return element_list, len(element_list)

    @staticmethod
    def get_menu_item(driver,index):
        main_menu = driver.find_element_by_class_name("menusubnav")
        element_list = main_menu.find_elements(By.TAG_NAME, "a")
        return element_list[index]

    dict_menu = {"Manag":"Manager","New Cust":"New Customer","Edit Cust":"Edit Customer","Delete Cust":"Delete Customer",
                 "New Acc":"new account","Edit Acc": "Edit Account","Delete Acc":"Delete Account","Deposit":"Deposit",
                 "Withdrawal":"Withdrawal","Fund Transfer":"Fund transfer","Change Pass":"Change Password","Balance Enq": "Balance Enquiry",
                 "Mini State":"Mini Statement","Customised State":"Customized Statement"}

    @staticmethod
    def menu_click_sequence(driver,dict_menu):
        try:
            for key in dict_menu:
                print("Key:",key)
                if key == "New Acc" or key == "Deposit" or key == "Withdrawal" or key == "Fund Transfer":
                    print(dict_menu[key])
                    BankAPP_CommonFunctions.click_menu_by_perform_mouse_action(driver,key,str(dict_menu[key]))
                else:
                    if key == "Delete Acc":
                        driver.execute_script("window.scrollBy(0,1000)", "")
                        time.sleep(2)
                    print("Value:",dict_menu[key])
                    BankAPP_CommonFunctions.click_menu_by_partial_link_text(driver,key,str(dict_menu[key]))
                BankAPP_CommonFunctions.close_popup(driver)
        except Exception as e:
            print("Exception found in menu_click_sequence method",type(e).__name__)
            print('Error in menu_click_sequence method on line {}'.format(sys.exc_info()[-1].tb_lineno),type(e).__name__,e)

    # def test_menu_click_Validation_InSequence(self):
    #     try:
    #         self.menu_click_sequence(self.driver,self.dict_menu)

            '''self.click_menu_by_partial_link_text("Manag","Manager")
            BankApp_CommonFunctons.close_popup(self.driver)

            self.click_menu_by_partial_link_text("New Cust", "New Customer")
            BankApp_CommonFunctons.close_popup(self.driver)

            self.click_menu_by_partial_link_text("Edit Cust", "Edit Customer")
            BankApp_CommonFunctons.close_popup(self.driver)

            self.click_menu_by_partial_link_text("Delete Cust", "Delete Customer")
            # BankApp_CommonFunctons.close_popup(self.driver)

            self.click_menu_by_perform_mouse_action("New Acc", "new account")
            BankApp_CommonFunctons.close_popup(self.driver)

            self.click_menu_by_partial_link_text("Edit Acc", "Edit Account")
            BankApp_CommonFunctons.close_popup(self.driver)

            self.click_menu_by_partial_link_text("Delete Acc", "Delete Account")
            BankApp_CommonFunctons.close_popup(self.driver)

            self.driver.execute_script("window.scrollBy(0,1000)", "")
            time.sleep(2)

            self.click_menu_by_perform_mouse_action("Deposit", "Deposit")  # Amount Deposit Form
            BankApp_CommonFunctons.close_popup(self.driver)

            self.click_menu_by_perform_mouse_action("Withdrawal", "Withdrawal")  # Amount Withdrawal Form
            BankApp_CommonFunctons.close_popup(self.driver)

            self.click_menu_by_perform_mouse_action("Fund Transfer", "Fund transfer")  # Fund transfer
            BankApp_CommonFunctons.close_popup(self.driver)

            self.click_menu_by_partial_link_text("Change Pass", "Change Password")
            BankApp_CommonFunctons.close_popup(self.driver)

            self.click_menu_by_partial_link_text("Balance Enq", "Balance Enquiry")
            BankApp_CommonFunctons.close_popup(self.driver)

            self.click_menu_by_partial_link_text("Mini State", "Mini Statement")
            BankApp_CommonFunctons.close_popup(self.driver)

            self.click_menu_by_partial_link_text("Customised State", "Customized Statement")
            BankApp_CommonFunctons.close_popup(self.driver)'''

        # except Exception as e:
        #     print("Exception from Menu Click in Sequence:", type(e).__name__)
        #     print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    # @classmethod
    # def tearDownClass(cls):
    #     BankAPP_CommonFunctions.logout(cls.driver)
    #     cls.driver.close()


# if __name__ == "__main__":
#   unittest.main()