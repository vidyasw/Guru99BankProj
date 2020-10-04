import unittest
# Navigation
from Functionality_Navigation.TC_NavigationValidation import TC_NavigationValidationTest
# MenuClick sequesnce
from Functionality_MenuClick.TC_MenuClickingInSequence import TC_MenuClickInSequenceTest
# Add Customer
from Functionality_Customer.TC_AddCustomer import TC_AddCustomerTest
from Functionality_Customer.TC_EditCustomer import TC_EditCustmerTest
from Functionality_Customer.TC_DeleteCustmer import TC_DeleteCustomerTest
# Add Account
from Functionality_Account.TC_AddAccount import TC_AddAccountTest
from Functionality_Account.TC_EditAccount import TC_EditAccountTest
from Functionality_Account.TC_DeleteAccount import TC_DeleteAccountTest

# All test from all modules
tc1 = unittest.TestLoader().loadTestsFromTestCase(TC_NavigationValidationTest)
tc2 = unittest.TestLoader().loadTestsFromTestCase(TC_MenuClickInSequenceTest)
tc3 = unittest.TestLoader().loadTestsFromTestCase(TC_AddCustomerTest)
tc4 = unittest.TestLoader().loadTestsFromTestCase(TC_EditCustmerTest)
tc5 = unittest.TestLoader().loadTestsFromTestCase(TC_DeleteCustomerTest)
tc6 = unittest.TestLoader().loadTestsFromTestCase(TC_AddAccountTest)
tc7 = unittest.TestLoader().loadTestsFromTestCase(TC_EditAccountTest)
tc8 = unittest.TestLoader().loadTestsFromTestCase(TC_DeleteAccountTest)

# Execute Suite wise
sanity = unittest.TestSuite([tc1,tc2])
system = unittest.TestSuite([tc1,tc2,tc3,tc4,tc5,tc6,tc7,tc8])

unittest.TextTestRunner().run(system)
