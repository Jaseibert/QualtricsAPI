#Imports
import unittest
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.Survey import Responses
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Contacts import MailingList
from QualtricsAPI.Contacts import XMDirectory

# Setup Tests Class
class setup_tests(object):

    def __init__(self):
        return

    ## I know ternary statements arent pythonic but they are succinct and I want to use them.
    def setup_test_token(self, short=False):
        '''Setup for Test Case 1: qualtrics_api_credentials token parameter lengths.(40)'''

        token = 'ThisIsaFakeAPITokenAndIsTooShortToWork!' if short else 'ThisIsaFakeAPITokenAndIsTooShortToWork!!!'
        correct_token = 'ThisIsaFakeAPITokenAndIsTooShortToWork!!'
        return token, correct_token

    def setup_test_dictionary_id(self, short=False, false_id=False):
        '''Setup for Test Case 2: qualtrics_api_credentials dictionary id parameter lengths (20), and the incorrect id (POOL_). '''

        dictonary_id = 'POOL_ThisIsaFakeID!' if short else 'POOL_ThisIsaFakeDictionaryID!'
        bad_id = 'ThisIsaFakeIDwo/POOL' if false_id else 'POOL_ThisIsaFakeID!'
        return dictonary_id, bad_id

    def setup_test_mailing_list_id(self, short=False, false_id=False):
        '''Setup for Test Case 3: Mailing List Sub-Module method's exception handling of the mailing list's length (18), and
        the incorrect id (CG_).'''

        mailing_list_id = 'CG_ThisIsaFakeID!' if short else 'CG_ThisIsaFakeMailingID!'
        bad_id = 'ThisIsaFakeIDwo/CG' if false_id else None
        return mailing_list_id, bad_id

    def setup_test_contact_id(self, short=False, false_id=False):
        '''Setup for Test Case 4: XMDirectory Sub-Module method's exception handling of the contact_id's length (18), and
        the incorrect id (CG_).'''

        contact_id = 'CID_ThisIsaFakeID!' if short else 'CID_ThisIsaFakeMailingID!'
        bad_id = 'ThisIsaFakeIDwo/CID' if false_id else None
        return contact_id, bad_id

    def setup_test_survey_id(self, short=False, false_id=False):
        '''Setup for Test Case 5: Responses Sub-Module method's exception handling of the survey_id's length (18), and
        the incorrect id (SV_).'''

        survey_id = 'SV_ThisIsaFakeID!' if short else 'SV_ThisIsaFakeMailingID!'
        bad_id = 'ThisIsaFakeIDwo/SV' if false_id else None
        return survey_id, bad_id

    def setup_methods(self, module=None):
        if module is 'credentials':
            c = Credentials()
            methods = [c.qualtrics_api_credentials()]
        elif module is 'mailing':
            m = MailingList()
            methods = [m.get_list(), m.rename_list(), m.delete_list(), m.list_contacts(), m.create_contacts_in_list()]
        elif module is 'xm':
            x = XMDirectory()
            methods = [x.get_contact(), x.delete_contact(), x.get_contact_additional_info()]
        elif module is 'responses':
            r = responses
            methods = [r.setup_request()]
        return methods

    def setup_itterator(self, module=None, param=None):
        #for method in setup_methods
        for method in self.setup_methods(module=module):
            method(param)
        #test a given set of exceptions
        return

#UnitTest Class
class TestQualtricsAPI(unittest.TestCase):

    ## API Credentials: Token ##
    #Test Assertion Error is handled: Short Token
    def test_credentials_one(self):
        s = setup_tests()
        token, correct_token = s.setup_test_token(short=False)
        with self.assertRaises(AssertionError):
            s.setup_itterator(module='credentials', param=token)




    #Test Assertion Error is handled: Long Token

    ## API Credentials: Dictorary ID ##
    #Test Assertion Error is handled: Short Dictonary id
    #Test Assertion Error is handled: Long Dictionary id
    #Test Assertion Error is handled: Incorrect Dictonary ID
    #Test Assertion Error is handled: Incorrect Dictonary ID and Short Dictonary id
    #Test Assertion Error is handled: Incorrect Dictonary ID and Long Dictonary id

    ## MailingList: Mailing List IDs ##
    #Test Assertion Error is handled: Short Dictonary id
    #Test Assertion Error is handled: Long Dictionary id
    #Test Assertion Error is handled: Incorrect Dictonary ID
    #Test Assertion Error is handled: Incorrect Dictonary ID and Short Dictonary id
    #Test Assertion Error is handled: Incorrect Dictonary ID and Long Dictonary id

    ## XMDirectory: Contact IDs ##
    #Test Assertion Error is handled: Short Contact id
    #Test Assertion Error is handled: Long Contact id
    #Test Assertion Error is handled: Incorrect Contact ID
    #Test Assertion Error is handled: Incorrect Contact ID and Short Contact id
    #Test Assertion Error is handled: Incorrect Contact ID and Long Contact id

    ## Responses: Survey IDs ##
    #Test Assertion Error is handled: Short Survey id
    #Test Assertion Error is handled: Long Survey id
    #Test Assertion Error is handled: Incorrect Survey id
    #Test Assertion Error is handled: Incorrect Survey id and Short Survey id
    #Test Assertion Error is handled: Incorrect Survey id and Long Survey id


if __name__ == "__main__":
    unittest.main()
