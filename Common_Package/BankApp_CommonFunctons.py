import os
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest


class BankAPP_CommonFunctions(unittest.TestCase):
    url ="http://www.demo.guru99.com/V4/index.php"
    username = "mngr287834"
    Password = "sEjUnuh"
    excelPath = "E:\\Vidyashri\\PythonSeleniumProjects\\Guru99BankProj\\TestData\\NavigationValidation.xlsx"
    sheet_NavigationValidation = "Navigation_Validation"
    sheet_Profile = "Profile"
    sheet_CustomerID = "Customer_ID"
    sheet_AccountDetails = "Account_Details"

    @staticmethod
    def get_modal_alert(browser):
        try:
            WebDriverWait(browser, 6).until(EC.alert_is_present())
            return browser.switch_to.alert
        except Exception as e:
            print("Timeout Exception for alert: when credentials are right alert will not pop up"
                  " ignore exception message ", type(e).__name__)

    @staticmethod
    def get_cust_id_frm_repo(filename,item):
        print("\nGetting Information from : ",filename)

        last_added_custid_file_path = "E:\\Vidyashri\\PythonSeleniumProjects\\Guru99BankProj\\Common_Package"
        last_added_custid_file_name = filename  #"LastAdded_CustID.txt"

        cust_id_file_absolute_path = Path(last_added_custid_file_path) / last_added_custid_file_name
        print("cust_id file Absolute Path : ", cust_id_file_absolute_path)

        if not os.path.exists(cust_id_file_absolute_path):
            print("Last added customer id has not sttored at " + cust_id_file_absolute_path)

        print("Reading cust_id from File")
        file = open(cust_id_file_absolute_path, "r")
        string_file = file.readlines()
        print(string_file)
        file.close()
        id = string_file[item].split(':')
        exact_id = id[1].lstrip()
        print(exact_id)
        return exact_id

    @staticmethod
    def login_bankApp(driver,userid, password):
        driver.get("http://www.demo.guru99.com/V4/index.php")
        driver.set_page_load_timeout(20)
        driver.maximize_window()
        driver.find_element_by_name("uid").send_keys(userid)  # ("mngr256110")
        driver.find_element_by_name("password").send_keys(password)  # ("UjEzYda")
        try:
            driver.find_element_by_xpath("/html/body/form/table/tbody/tr[3]/td[2]/input[1]").click()
            time.sleep(1)
            if BankAPP_CommonFunctions.get_modal_alert(driver):
                error = driver.switch_to.alert.text
                driver.switch_to.alert.accept()
                print("Login Failed with :", error)
            else:
                if "Guru99 Bank Manager HomePage" in driver.title:
                    print("Login is successful")
                else:
                    print("Failed to login")
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            # print("Failed to login as", error)
            driver.refresh()
            driver.get("http://www.demo.guru99.com/V4/index.php")
            driver.set_page_load_timeout(10)
        finally:
            string1 = driver.find_element_by_xpath("//table/tbody/tr/td/table/tbody/tr[3]/td").text
            if userid in string1:
                print("Login validation is successful with",userid)
            else:
                print("Login validation failed",string1,userid)
        # driver.save_screenshot("E:\BankLogin.jpg")

    @staticmethod
    def click_menu_by_partial_link_text(driver,partial_link_text, linkname):
        driver.implicitly_wait(2)
        driver.find_element(By.PARTIAL_LINK_TEXT, partial_link_text).click()
        driver.set_page_load_timeout(10)
        lable_link = driver.find_element_by_xpath("//table/tbody/tr/td/table/tbody/tr/td").text
        if linkname in lable_link:
            print("Clicked successfully on Menu : ", linkname)
        else:
            print("Failed to click on Menu :", linkname)

    @staticmethod
    def click_menu_by_perform_mouse_action(driver,partial_link_text, linkname):
        menu_obj = driver.find_element(By.PARTIAL_LINK_TEXT, partial_link_text)
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(menu_obj, 5, 5)
        action.click()
        action.perform()
        time.sleep(3)
        driver.set_page_load_timeout(10)
        lable = driver.find_element_by_xpath("//table/tbody/tr/td/table/tbody/tr/td").text
        if linkname in lable:
            print("Clicked successfully on: ", linkname)
        else:
            print("Failed to click :", linkname)

    @staticmethod
    def logout(driver):
        log_out = driver.find_element(By.LINK_TEXT, "Log out")

        driver.execute_script("arguments[0].click();", log_out)
        wait = WebDriverWait(driver,15)
        if wait.until(EC.alert_is_present()):
            driver.switch_to.alert.accept()

        if "Guru99 Bank Home Page" in driver.title:
            print("Bank app logout")
        else:
            print("Bank app logout Failed")

    @staticmethod
    def close_popup(driver):
        try:
            driver.find_element_by_link_text("New Account").is_displayed()
            wait = WebDriverWait(driver, 15)
            wait.until(EC.visibility_of_element_located((By.ID, "flow_close_btn_iframe")))
            driver.switch_to.frame("flow_close_btn_iframe")
            driver.find_element_by_id("closeBtn").click()
            time.sleep(1)
            driver.switch_to.default_content()
        except Exception as e:
            print("Exception from Closing popup:", type(e).__name__)
            print("Error in " + __name__ + " on line {} ".format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


if __name__ == "__main__":
    unittest.main()