import datetime
import os
import re
import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Common_Package.BankApp_CommonFunctons import BankAPP_CommonFunctions
from faker import Faker
# from random import choice
from utility import Excelutility
from enum import Enum
from pathlib import Path


# global global_cust_id
cust_data = {}  # dictionary
'''logging.basicConfig(filename="C://Users/Sony//PycharmProjects//Guru99BankProj//Loggings//test.log",
                    format = '%(asctime)s: % (levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %T:%M:%S %P'
                    #level = logging.DEBUG
                    )
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)'''


def store_custid(cust_id):
    print("\nWriting Custmer_id Information : ")

    last_added_custid_file_path = "E:\\Vidyashri\\PythonSeleniumProjects\\Guru99BankProj\\Common_Package"
    last_added_custid_file_name = "LastAdded_CustID.txt"

    if not os.path.exists(last_added_custid_file_path):
        os.mkdir(last_added_custid_file_path)

    print("cust_id file Name : ", last_added_custid_file_name)

    custid_file_absolute_path = Path(last_added_custid_file_path) / last_added_custid_file_name
    print("cust_id file Absolute Path : ", custid_file_absolute_path)

    print("Writing to cust_id into File")
    file = open(custid_file_absolute_path, "w+")
    file.write("Custmer Id : " + cust_id)
    file.close()


class TC_AddCustomerTest(unittest.TestCase):

    class gender(Enum):
        F = "female"
        M = "male"

    Path = BankAPP_CommonFunctions.excelPath
    SheetName = BankAPP_CommonFunctions.sheet_Profile
    SheetToStore = BankAPP_CommonFunctions.sheet_CustomerID

    # @classmethod
    # def setUpClass(cls):
    #     cls.driver = webdriver.Chrome(executable_path="E:\\chromedriver_win32\\chromedriver.exe")
    #     cls.driver.maximize_window()
    #     BankAPP_CommonFunctions.login_bankApp(cls.driver, BankAPP_CommonFunctions.username,
    #                                           BankAPP_CommonFunctions.Password)
    #     BankAPP_CommonFunctions.close_popup(cls.driver)

    @staticmethod
    def __data_generator(profile_of):
        faker = Faker()
        fake1 = Faker('en_GB')
        for i in range(0, 1):
            cust_data[i] = {}
            # student_data[i]['id'] = randint(1, 100)
            # student_data[i]['name'] = faker.name()
            # student_data[i]['address'] = faker.address()
            cust_data[i]['Date of Birth'] = faker.date(pattern="%m-%d-%Y", end_datetime=datetime.date(2000, 1, 1))
            cust_data[i]['Phone No'] = f'{fake1.phone_number()}'
            cust_data[i]['Profile'] = faker.simple_profile(profile_of)
        print(cust_data)
        return cust_data

    '''def name_generator():
        first_names = ('Smitha', 'Reeta', 'Naina', 'Mary', 'John', 'Andy', 'Joe', 'Tony')
        last_names = ('Johnson', 'Smith', 'Williams', 'Ray', 'Denjafa', 'JoJo', 'Albero', 'Koshy')
        name = " ".join(["%s %s" % (choice(first_names), choice(last_names)) for _ in range(1)])
        return name'''

    @staticmethod
    def __get_propercity(city):
        cty = str(city).split('\n')  # name[0]["Profile"]["address"]
        # print("cty:", cty)
        cit = None
        if ',' in cty[1]:
            cit = cty[1].split(',')
        elif ' ' in cty[1]:
            cit = cty[1].split(' ')
        else:
            print("Comma and space is not there in " + str(cty))

        if len(cit) == 4:
            proper_city = cit[0] + " " + cit[1][0:len(cit[0]) - 1]
        else:
            proper_city = cit[0]
        # print("propercity :", proper_city)
        return proper_city

    @staticmethod
    def __get_properState(address):
        cty = str(address).split('\n')  # name[0]["Profile"]["address"]
        statenZip = str(cty[1]).split(' ')
        if len(statenZip) == 4:
            proper_state = str(statenZip[2])
        else:
            proper_state = statenZip[1]
        # print(proper_state)
        return proper_state

    @staticmethod
    def __get_properPin(address):
        cty = str(address).split('\n')  # name[0]["Profile"]["address"]
        statenZip = str(cty[1]).split(' ')
        if len(statenZip) == 4:
            proper_pin = str(statenZip[3]) + "0"
        else:
            proper_pin = str(statenZip[2]) + "0"
        return proper_pin

    @classmethod
    def gender_fullform(cls,cust_nameFromXl):
        gen_fromxl = None
        if cust_nameFromXl.lower() == "f":
            f = cls.gender.F                  # self.gender.F
            gen_fromxl = f.value
        elif cust_nameFromXl.lower() == "m":
            m = cls.gender.M                  # self.gender.M
            gen_fromxl = m.value
        else:
            print("Gender Not Available!!")
        return gen_fromxl

    @classmethod
    def date_Conversion(cls,cust_dobFromXl):
        date = datetime.datetime.strptime(cust_dobFromXl,"%m-%d-%Y")
        date1 = datetime.datetime.strftime(date,"%Y-%m-%d")
        return date1

    @staticmethod
    def cust_name(driver,name):
        name_filed = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[4]/td[2]/input")
        name_filed.send_keys(name)
        Excelutility.write_data(TC_AddCustomerTest.Path,TC_AddCustomerTest.SheetName,2, 1, name)

    @staticmethod
    def select_gender(driver,gender):
        radios = None
        if gender.lower() == "m":
            radios = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[5]/td[2]/input[1]")
        elif gender.lower() == "f":
            radios = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[5]/td[2]/input[2]")
        else:
            print("Wrong input!!!")
        radios.click()
        time.sleep(1)
        if radios.is_selected():
            print("Gender "+ radios.get_property("value").upper() + " got selected")
        else:
            print("Failed to select :" + radios.get_property("value").upper())
        Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 2, radios.get_property("value").upper())
        return radios.get_property("value").upper()

    @staticmethod
    def add_dateBirth(driver,date):
        driver.find_element_by_xpath("//*[@id='dob']").send_keys(date)
        Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 3, date)

    @staticmethod
    def add_address(driver,address):
        driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[7]/td[2]/textarea").send_keys(address)
        Excelutility.write_data(TC_AddCustomerTest.Path,TC_AddCustomerTest.SheetName, 2, 4, address)

    @staticmethod
    def add_city(driver,city):
        driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[8]/td[2]/input").send_keys(city)
        Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 5, city)

    @staticmethod
    def add_state(driver,state):
        driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[9]/td[2]/input").send_keys(state)
        Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 6, state)

    @staticmethod
    def add_pin(driver,pin):
        driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[10]/td[2]/input").send_keys(pin)
        Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 7, pin)
        #return self.driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[10]/td[2]/input").text

    @staticmethod
    def add_phoneno(driver,phoneno):
        driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[11]/td[2]/input").send_keys(phoneno)
        Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 8, phoneno)

    @staticmethod
    def add_mail(driver,mail):
        driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[12]/td[2]/input").send_keys(mail)
        Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 9, mail)

    @staticmethod
    def add_password(driver,password):
        driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[13]/td[2]/input").send_keys(password)
        Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 10, password)

    @staticmethod
    def validate_custinfo(driver):
        if "Customer Registered Successfully!!!" in driver.find_element_by_xpath("//*[@id='customer']/tbody/tr[1]/td/p").text:
            print("Customer registered successfully")

        row = Excelutility.get_row_count(TC_AddCustomerTest.Path,TC_AddCustomerTest.SheetToStore)
        cust_id = driver.find_element_by_xpath("//*[@id='customer']/tbody/tr[4]/td[2]").text
        #global_cust_id = cust_id
        store_custid(cust_id)
        Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetToStore, row + 1, 1,cust_id)

        cust_name = driver.find_element_by_xpath("//*[@id ='customer']/tbody/tr[5]/td[2]").text
        cust_nameFromXl = Excelutility.read_data(TC_AddCustomerTest.Path,TC_AddCustomerTest.SheetName,2,1)
        if cust_name == cust_nameFromXl:
            Excelutility.write_data(TC_AddCustomerTest.Path,TC_AddCustomerTest.SheetToStore,row+1,2,cust_name)
        else:
            print(cust_name + " is not same as " + cust_nameFromXl + " added")

        cust_gender = driver.find_element_by_xpath("//*[@id ='customer']/tbody/tr[6]/td[2]").text
        #print(cust_gender)
        cust_genderFromXl = Excelutility.read_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 2)
        gen_fromxl = TC_AddCustomerTest.gender_fullform(cust_genderFromXl)
        if cust_gender == gen_fromxl:
            Excelutility.write_data(TC_AddCustomerTest.Path,TC_AddCustomerTest.SheetToStore,row+1,3,cust_gender)
        else:
            print(cust_gender + " is not same as " + cust_genderFromXl + " added")

        cust_dob = driver.find_element_by_xpath("//*[@id ='customer']/tbody/tr[7]/td[2]").text
        cust_dobFromXl = Excelutility.read_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 3)

        x= TC_AddCustomerTest.date_Conversion(cust_dobFromXl)
        #print(x)
        if cust_dob == x:
            Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetToStore, row + 1, 4, cust_dob)
        else:
            print(cust_dob + " is not same as " + cust_dobFromXl + " added")

        cust_addr = driver.find_element_by_xpath("//*[@id ='customer']/tbody/tr[8]/td[2]").text
        cust_addrFromXl = Excelutility.read_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 4)

        if cust_addr == re.sub(' +', ' ', cust_addrFromXl): #cust_addrFromXl:
            Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetToStore, row + 1, 5, cust_addr)
        else:
            print(cust_addr + " is not same as " + cust_addrFromXl + " added")

        cust_city = driver.find_element_by_xpath("//*[@id ='customer']/tbody/tr[9]/td[2]").text
        cust_cityFromXl = Excelutility.read_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 5)
        if cust_city == cust_cityFromXl:
            Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetToStore, row + 1, 6, cust_city)
        else:
            print(cust_city + " is not same as " + cust_cityFromXl + " added")

        cust_state = driver.find_element_by_xpath("//*[@id ='customer']/tbody/tr[10]/td[2]").text
        cust_stateFromXl = Excelutility.read_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 6)
        if cust_state == cust_stateFromXl:
            Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetToStore, row + 1, 7, cust_state)
        else:
            print(cust_state + " is not same as " + cust_stateFromXl + " added")

        cust_pin = driver.find_element_by_xpath("//*[@id ='customer']/tbody/tr[11]/td[2]").text
        cust_pinFromXl = Excelutility.read_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 7)
        if cust_pin == cust_pinFromXl:
            Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetToStore, row + 1, 8, cust_pin)
        else:
            print(cust_pin + " is not same as " + cust_pinFromXl + " added")

        cust_mobile = driver.find_element_by_xpath("//*[@id ='customer']/tbody/tr[12]/td[2]").text
        cust_mobileFromXl = Excelutility.read_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 8)
        if cust_mobile == cust_mobileFromXl:
            Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetToStore, row + 1, 9, cust_mobile)
        else:
            print(cust_mobile + " is not same as " + cust_mobileFromXl + " added")

        cust_mail = driver.find_element_by_xpath("//*[@id ='customer']/tbody/tr[13]/td[2]").text
        cust_mailFromXl = Excelutility.read_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetName, 2, 9)
        if cust_mail == cust_mailFromXl:
            Excelutility.write_data(TC_AddCustomerTest.Path, TC_AddCustomerTest.SheetToStore, row + 1, 10, cust_mail)
        else:
            print(cust_mail + " is not same as " + cust_mailFromXl + " added")

        print("Validation is done for added customer with id " + cust_id + " " + cust_name + " Successfully!!!")

        Excelutility.delete_row(TC_AddCustomerTest.Path,TC_AddCustomerTest.SheetName,2,1)
        TC_AddCustomerTest.assertTrue(Excelutility.get_row_count(TC_AddCustomerTest.Path,TC_AddCustomerTest.SheetName) == 1,"Temp Profile got deleted!!!")

    @staticmethod
    def add_customer(driver,profile_gender_required):

        cust_info = TC_AddCustomerTest.__data_generator(profile_gender_required)
        TC_AddCustomerTest.assertIsNotNone(cust_info, "Data has Generated Successfully")

        # Addition of customer Name
        TC_AddCustomerTest.cust_name(driver,cust_info[0]["Profile"]["name"])

        # Addition of customer gender
        TC_AddCustomerTest.select_gender(driver,cust_info[0]["Profile"]["sex"])

        # Addition of customer dob
        TC_AddCustomerTest.add_dateBirth(driver,cust_info[0]["Date of Birth"])

        # Addition of customer address
        adress = str(cust_info[0]["Profile"]["address"]).split('\n')
        bad_chars = [';', ':', '!', '*', ' ', '(', ')', '.', ',']
        for i in bad_chars:
            adress[0] = str(adress[0]).replace(i, ' ')
        TC_AddCustomerTest.add_address(driver,adress[0])

        # Addition of customer city
        proper_city = TC_AddCustomerTest.__get_propercity(cust_info[0]["Profile"]["address"])
        TC_AddCustomerTest.add_city(driver,proper_city)

        # Addition of customer state
        proper_state = TC_AddCustomerTest.__get_properState(cust_info[0]["Profile"]["address"])
        TC_AddCustomerTest.add_state(driver,proper_state)

        # Addition of customer pin
        proper_pin = TC_AddCustomerTest.__get_properPin(cust_info[0]["Profile"]["address"])
        TC_AddCustomerTest.add_pin(driver,str(proper_pin))

        # Addition of customer phone no
        bad_chars = [';', ':', '!', "*", ' ', '(', ')']
        phoneNo = cust_info[0]["Phone No"]
        for i in bad_chars:
            phoneNo = phoneNo.replace(i, '')
        TC_AddCustomerTest.add_phoneno(driver,phoneNo)

        # Addition of customer mail id
        TC_AddCustomerTest.add_mail(driver,cust_info[0]["Profile"]["mail"])

        # Addition of customer profile password
        TC_AddCustomerTest.add_password(driver,"#Welcome123")

        # click Submit and wait for success message link
        driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[14]/td[2]/input[1]").click()

        wait = WebDriverWait(driver, 75)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='customer']/tbody/tr[1]/td/p")))

    '''def test_addition_cust(self):
        try:
            BankAPP_CommonFunctions.click_menu_by_partial_link_text(self.driver, "New Cust", "New Customer")
            TC_AddCustomerTest.add_customer(self.driver,"M")
            TC_AddCustomerTest.validate_custinfo(self.driver)

        except Exception as e:
            print("Exception from Adding Customer:", type(e).__name__)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno),type(e).__name__, e)'''

    # @classmethod
    # def tearDownClass(cls):
    #     BankAPP_CommonFunctions.close_popup(cls.driver)
    #     BankAPP_CommonFunctions.logout(cls.driver)
    #     cls.driver.implicitly_wait(1)
    #     cls.driver.close()


# if __name__ == "__main__":
#     unittest.main()