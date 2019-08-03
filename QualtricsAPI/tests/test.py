# Run in the Root Directory to run tests
## python3 -m unittest QualtricsAPI/tests/test.py

import unittest
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.Survey import Responses
from QualtricsAPI.JSON import Parser
from QualtricsAPI.XM import MailingList
from QualtricsAPI.XM import XMDirectory

# Setup Tests Class
class setup_tests(object):

    def __init__(self):
        return

    def setup_test_token(self, short=False):
        '''Setup for Test Case 1: qualtrics_api_credentials token parameter lengths.(40)'''

        token = 'ThisIsaFakeAPITokenAndIsTooShortToWork!' if short else 'ThisIsaFakeAPITokenAndIsTooShortToWork!!!'
        return token

    def setup_test_directory_id(self, short=False, false_id=False):
        '''Setup for Test Case 2: qualtrics_api_credentials directory id parameter lengths (20), and the incorrect id (POOL_). '''

        directory_id = 'POOL_ThisIsaFakeID!' if short else 'POOL_ThisIsaFakeDirectoryID!'
        bad_id = 'ThisIsaFakeIDwo/POOL' if false_id else 'POOL_ThisIsaFakeID!'
        return directory_id, bad_id

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

#UnitTest Class
class TestQualtricsAPI(unittest.TestCase):

    correct_token = 'ThisIsaFakeAPITokenAndIsTooShortToWork!!'

    def test_credentials_long_token(self):
        '''This method tests that an assertion is raised in the Credentials Module when the user enters an api token that is too long.'''
        token = setup_tests().setup_test_token(short=False)
        directory_id, bad_id = setup_tests().setup_test_directory_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Credentials().qualtrics_api_credentials(token=token, data_center='FAKE', directory_id=directory_id)

    #Test Assertion Error is handled: Short Token
    def test_credentials_short_token(self):
        '''This method tests that an assertion is raised in the Credentials Module when the user enters an api token that is too short.'''
        token = setup_tests().setup_test_token(short=True)
        directory_id, bad_id = setup_tests().setup_test_directory_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Credentials().qualtrics_api_credentials(token=token, data_center='FAKE', directory_id=directory_id)

    ## API Credentials: Directory ID
    #Test Assertion Error is handled: Short Directory id
    def test_credentials_short_directory_id(self):
        '''This method tests that an assertion is raised in the Credentials Module when the user enters a directory id that is too short.'''
        token = setup_tests().setup_test_token(short=True)
        directory_id, bad_id = setup_tests().setup_test_directory_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Credentials().qualtrics_api_credentials(token=TestQualtricsAPI.correct_token, data_center='FAKE', directory_id=directory_id)

    #Test Assertion Error is handled: Long Directory id
    def test_credentials_long_directory_id(self):
        '''This method tests that an assertion is raised in the Credentials Module when the user enters a directory id that is too long.'''
        token = setup_tests().setup_test_token(short=True)
        directory_id, bad_id = setup_tests().setup_test_directory_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Credentials().qualtrics_api_credentials(token=TestQualtricsAPI.correct_token, data_center='FAKE', directory_id=directory_id)

    #Test Assertion Error is handled: Incorrect Dictonary ID
    def test_credentials_bad_directory_id(self):
        '''This method tests that an assertion is raised in the Credentials Module when the user enters a directory id that is incorrect.'''
        token = setup_tests().setup_test_token(short=True)
        directory_id, bad_id = setup_tests().setup_test_directory_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Credentials().qualtrics_api_credentials(token=TestQualtricsAPI.correct_token, data_center='FAKE', directory_id=bad_id)

    ## MailingList: Mailing List IDs (list_lists)
    def test_ml_short_pg_sz_list_lists(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a page_size of 0.'''
        with self.assertRaises(AssertionError):
            MailingList().list_lists(page_size=0)

    ## MailingList: Mailing List IDs (rename_list)
    #Test Assertion Error is handled: Short Mailing List ID
    def test_ml_short_ml_id_rename(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is too long.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            MailingList().rename_list(mailing_list=mailing_list_id, name='Fake')

    #Test Assertion Error is handled: Long Mailing List ID
    def test_ml_long_ml_id_rename(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is too short.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            MailingList().rename_list(mailing_list=mailing_list_id, name='Fake')

    #Test Assertion Error is handled: Incorrect Mailing List ID
    def test_ml_bad_ml_id_rename(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is incorrect. '''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            MailingList().rename_list(mailing_list=bad_id, name='Fake')

    ## MailingList: Mailing List IDs (delete_list)
    #Test Assertion Error is handled: Short Mailing List ID
    def test_ml_short_ml_id_delete(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is too long.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            MailingList().delete_list(mailing_list=mailing_list_id)

    #Test Assertion Error is handled: Long Mailing List ID
    def test_ml_long_ml_id_delete(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is too short.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            MailingList().delete_list(mailing_list=mailing_list_id)

    #Test Assertion Error is handled: Incorrect Mailing List ID
    def test_ml_bad_ml_id_delete(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id is that is incorrect.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            MailingList().delete_list(mailing_list=bad_id)

    ## MailingList: Mailing List IDs (list_contacts)
    #Test Assertion Error is handled: Short Mailing List ID
    def test_ml_short_ml_id_list_contacts(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is too long.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            MailingList().list_contacts(mailing_list=mailing_list_id)

    #Test Assertion Error is handled: Long Mailing List ID
    def test_ml_long_ml_id_list_contacts(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is too short. '''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            MailingList().list_contacts(mailing_list=mailing_list_id)

    #Test Assertion Error is handled: Incorrect Mailing List ID
    def test_ml_bad_ml_id_list_contacts(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is incorrect. '''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            MailingList().list_contacts(mailing_list=bad_id)

    ## MailingList: Mailing List IDs (create_contact_in_list)
    #Test Assertion Error is handled: Short Mailing List ID
    def test_ml_short_ml_id_create(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is too long.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            MailingList().create_contact_in_list(mailing_list=mailing_list_id)

    #Test Assertion Error is handled: Long Mailing List ID
    def test_ml_long_ml_id_create(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is too short.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            MailingList().create_contact_in_list(mailing_list=mailing_list_id)

    #Test Assertion Error is handled: Incorrect Mailing List ID
    def test_ml_bad_ml_id_create(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id is that is incorrect.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            MailingList().create_contact_in_list(mailing_list=bad_id)

    ## XMDirectory: Contact IDs (delete_contact)
    #Test Assertion Error is handled: Short Contact id
    def test_xm_short_contact_id_delete(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is too long. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            XMDirectory().delete_contact(contact_id=contact_id)

    #Test Assertion Error is handled: Long Contact id
    def test_xm_long_contact_id_delete(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is too short. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            XMDirectory().delete_contact(contact_id=contact_id)

    #Test Assertion Error is handled: Incorrect Contact id
    def test_xm_bad_contact_id_delete(self):
        '''This method tests that an assertion is raised in the  XMDirectory Module when the user enters a contact_id that is incorrect. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            XMDirectory().delete_contact(contact_id=bad_id)

    ## XMDirectory: Contact IDs (update_contact)
    #Test Assertion Error is handled: Short Contact id
    def test_xm_short_contact_id_update(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is too long. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            XMDirectory().update_contact(contact_id=contact_id)

    #Test Assertion Error is handled: Long Contact id
    def test_xm_long_contact_id_update(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is too short. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            XMDirectory().update_contact(contact_id=contact_id)

    #Test Assertion Error is handled: Incorrect Contact id
    def test_xm_bad_contact_id_update(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is incorrect. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            XMDirectory().update_contact(contact_id=bad_id)

    ## XMDirectory: Contact IDs (get_contact)
    #Test Assertion Error is handled: Short Contact id
    def test_xm_short_contact_id_get(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is too long. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            XMDirectory().get_contact(contact_id=contact_id)

    #Test Assertion Error is handled: Long Contact id
    def test_xm_long_contact_id_get(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is too short. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            XMDirectory().get_contact(contact_id=contact_id)

    #Test Assertion Error is handled: Incorrect Contact id
    def test_xm_bad_contact_id_get(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is incorrect. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            XMDirectory().get_contact(contact_id=bad_id)

    ## XMDirectory: Contact IDs (get_contact_additional_info)
    #Test Assertion Error is handled: Short Contact id
    def test_xm_short_contact_id_get_add(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is too long. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            XMDirectory().get_contact_additional_info(contact_id=contact_id)

    #Test Assertion Error is handled: Long Contact id
    def test_xm_long_contact_id_get_add(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is too short. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            XMDirectory().get_contact_additional_info(contact_id=contact_id)

    #Test Assertion Error is handled: Incorrect Contact id
    def test_xm_bad_contact_id_get_add(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is incorrect. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            XMDirectory().get_contact_additional_info(contact_id=bad_id)

    ## Responses: Survey IDs ##
    #Test Assertion Error is handled: Short Survey id
    def test_responses_short_survey_id(self):
        '''This method tests that an assertion is raised in the Responses Module when the user enters a survey_id that is too long. '''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Responses().setup_request(file_format='csv', survey_id=survey_id)

    #Test Assertion Error is handled: Long Survey id
    def test_responses_long_survey_id(self):
        '''This method tests that an assertion is raised in the Responses Module when the user enters a survey_id that is too short. '''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Responses().setup_request(file_format='csv', survey_id=survey_id)

    #Test Assertion Error is handled: Incorrect Survey id
    def test_responses_bad_survey_id(self):
        '''This method tests that an assertion is raised in the Responses Module when the user enters a survey_id that is incorrect. '''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Responses().setup_request(file_format='csv', survey_id=bad_id)

if __name__ == "__main__":
    unittest.main()
