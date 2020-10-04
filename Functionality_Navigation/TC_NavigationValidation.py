import sys
import time
import unittest
# from Common_Package.BankApp_CommonFunctons import BankAPP_CommonFunctions
from utility import Excelutility
from Common_Package.BankApp_CommonFunctons import BankAPP_CommonFunctions


class TC_NavigationValidationTest(unittest.TestCase):

    Path = BankAPP_CommonFunctions.excelPath
    SheetName = BankAPP_CommonFunctions.sheet_NavigationValidation
    url = BankAPP_CommonFunctions.url

    # @classmethod
    # def setUpClass(cls):
    #     cls.driver = webdriver.Chrome(executable_path="E:\chromedriver_win32\chromedriver.exe")
    #     cls.driver.get(cls.url)
    #     cls.driver.set_page_load_timeout(10)
    #     cls.driver.maximize_window()
    #     # cls.assertIn("Guru99 Bank Home Page", cls.driver.title, "Guru99 bank site is active")

    @staticmethod
    def login_with_diff_credentials(driver, excel_path, excel_sheet, app_url):
        rows = Excelutility.get_row_count(excel_path, excel_sheet)
        # self.site_open()

        for row in range(2, rows + 1):
            print(row)
            username = Excelutility.read_data(excel_path, excel_sheet, row, 1)
            print("Current username:", username)
            password = Excelutility.read_data(excel_path, excel_sheet, row, 2)
            print("Current Password:", password)
            driver.find_element_by_name("uid").send_keys(username)
            driver.find_element_by_name("password").send_keys(password)
            time.sleep(1)
            error = "Shri"
            try:
                driver.find_element_by_xpath("/html/body/form/table/tbody/tr[3]/td[2]/input[1]").click()
                time.sleep(1)
                if BankAPP_CommonFunctions.get_modal_alert(driver):
                    error = driver.switch_to.alert.text
                    driver.switch_to.alert.accept()
                    print("Login Failed with :", error)
                    Excelutility.write_data(excel_path, excel_sheet, row, 3, "Test Failed")
                else:
                    if "Guru99 Bank Manager HomePage" in driver.title:
                        print("Login is successful")
                        Excelutility.write_data(excel_path, excel_sheet, row, 3, "Test Passed")
                    else:
                        print("Failed to login")
                        Excelutility.write_data(excel_path, excel_sheet, row, 3, "Test Failed")
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                # print("Failed to login as", error)
                Excelutility.write_data(excel_path, excel_sheet, row, 3, "Test Failed")
                driver.refresh()
                driver.get(app_url)
                driver.set_page_load_timeout(10)
            finally:
                print("Completed Iteration with excel row no :", row)

            if "User or Password is not valid" not in error:
                BankAPP_CommonFunctions.close_popup(driver)
                driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
                time.sleep(1)
                BankAPP_CommonFunctions.logout(driver)

    # def test_validationNavigation(self):
    #     self.login_with_diff_credentials(self.driver,self.Path,self.SheetName,self.url)

    # @classmethod
    # def tearDownClass(cls):
    #     cls.driver.close()


# if __name__ == "__main__":
#     unittest.main()