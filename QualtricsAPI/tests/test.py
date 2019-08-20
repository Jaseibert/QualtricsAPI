# Run in the Root Directory to run tests
## python3 -m unittest QualtricsAPI/tests/test.py

import unittest
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.Survey import Responses
from QualtricsAPI.JSON import Parser
from QualtricsAPI.XM import MailingList
from QualtricsAPI.XM import XMDirectory
from QualtricsAPI.Library import Messages
from QualtricsAPI.Survey import Distributions

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

    def setup_test_library_id_ur(self, short=False, false_id=False):
        '''Setup for Test Case 6: Responses Sub-Module method's exception handling of the library_id's length (18), and
        the incorrect id (UR_).'''

        lib_id = 'UR_ThisIsaFakeID!' if short else 'UR_ThisIsaFakeMailingID!'
        bad_id = 'ThisIsaFakeIDwo/UR' if false_id else None
        return lib_id, bad_id

    def setup_test_library_id_gr(self, short=False, false_id=False):
        '''Setup for Test Case 7: Responses Sub-Module method's exception handling of the library_id's length (18), and
        the incorrect id (GR_).'''

        lib_id = 'GR_ThisIsaFakeID!' if short else 'GR_ThisIsaFakeMailingID!'
        bad_id = 'ThisIsaFakeIDwo/GR' if false_id else None
        return lib_id, bad_id

    def setup_test_dist_id(self, short=False, false_id=False):
        '''Setup for Test Case 8: Responses Sub-Module method's exception handling of the distribution_id's length (19), and
        the incorrect id (UMD_).'''

        dist_id = 'EMD_ThisIsaFakeID!' if short else 'EMD_ThisIsaFakeMailingID!'
        bad_id = 'ThisIsaFakeIDwo/EMD' if false_id else None
        return dist_id, bad_id

    def setup_test_message_id(self, short=False, false_id=False):
        '''Setup for Test Case 9: Responses Sub-Module method's exception handling of the message_id's length (18), and
        the incorrect id (MS_).'''

        msg_id = 'MS_ThisIsaFakeID!' if short else 'MS_ThisIsaFakeMailingID!'
        bad_id = 'ThisIsaFakeIDwo/MS' if false_id else None
        return msg_id, bad_id

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


    ## MailingList: Mailing List IDs (rename_list)
    #Test Assertion Error is handled: Long Mailing List ID
    def test_ml_short_ml_id_rename(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is too long.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            MailingList().rename_list(mailing_list=mailing_list_id, name='Fake')

    #Test Assertion Error is handled: Short Mailing List ID
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
    #Test Assertion Error is handled: Long Mailing List ID
    def test_ml_short_ml_id_delete(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is too long.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            MailingList().delete_list(mailing_list=mailing_list_id)

    #Test Assertion Error is handled: Short Mailing List ID
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
    #Test Assertion Error is handled: Long Mailing List ID
    def test_ml_short_ml_id_list_contacts(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is too long.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            MailingList().list_contacts(mailing_list=mailing_list_id)

    #Test Assertion Error is handled: Short Mailing List ID
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
    #Test Assertion Error is handled: Long Mailing List ID
    def test_ml_short_ml_id_create(self):
        '''This method tests that an assertion is raised in the MailingList Module when the user enters a mailing_list_id that is too long.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            MailingList().create_contact_in_list(mailing_list=mailing_list_id)

    #Test Assertion Error is handled: Short Mailing List ID
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
    #Test Assertion Error is handled: Long Contact id
    def test_xm_short_contact_id_delete(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is too long. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            XMDirectory().delete_contact(contact_id=contact_id)

    #Test Assertion Error is handled: Short Contact id
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
    #Test Assertion Error is handled: Long Contact id
    def test_xm_short_contact_id_update(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is too long. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            XMDirectory().update_contact(contact_id=contact_id)

    #Test Assertion Error is handled: Short Contact id
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
    #Test Assertion Error is handled: Long Contact id
    def test_xm_short_contact_id_get(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is too long. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            XMDirectory().get_contact(contact_id=contact_id)

    #Test Assertion Error is handled: Short Contact id
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
    #Test Assertion Error is handled: Long Contact id
    def test_xm_short_contact_id_get_add(self):
        '''This method tests that an assertion is raised in the XMDirectory Module when the user enters a contact_id that is too long. '''
        contact_id, bad_id = setup_tests().setup_test_contact_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            XMDirectory().get_contact_additional_info(contact_id=contact_id)

    #Test Assertion Error is handled: Short Contact id
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
    #Test Assertion Error is handled: Long Survey id
    def test_responses_short_survey_id(self):
        '''This method tests that an assertion is raised in the Responses Module when the user enters a survey_id that is too long. '''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Responses().setup_request(file_format='csv', survey_id=survey_id)

    #Test Assertion Error is handled: Short Survey id
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

    ## Messages: Library IDs ##
    #Test Assertion Error is handled: Long Library id (list_messages: UR)
    def test_responses_short_library_id_list_msgs_ur(self):
        '''This method tests that an assertion is raised in the Messages Module's list_messages method when the user enters a
        library_id (UR: User-Defined Resource) that is too long. '''
        lib_id, bad_id = setup_tests().setup_test_library_id_ur(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Messages().list_messages(library=lib_id)

    #Test Assertion Error is handled: Short Library id (list_messages: UR)
    def test_responses_long_library_id_lst_msgs_ur(self):
        '''This method tests that an assertion is raised in the Messages Module's list_messages method when the user enters a
         library_id (UR: User-Defined Resource) that is too short. '''
        lib_id, bad_id = setup_tests().setup_test_library_id_ur(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Messages().list_messages(library=lib_id)

    #Test Assertion Error is handled: Incorrect Library id (list_messages: UR)
    def test_responses_bad_libary_id_lst_msgs_ur(self):
        '''This method tests that an assertion is raised in the Messages Module's list_messages method when the user enters
         a library_id (UR: User-Defined Resource) that is incorrect. '''
        lib_id, bad_id = setup_tests().setup_test_library_id_ur(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Messages().list_messages(library=bad_id)

    #Test Assertion Error is handled: Long Library id (list_messages: GR)
    def test_responses_short_library_id_list_msgs_gr(self):
        '''This method tests that an assertion is raised in the Messages Module's list_messages method when the user enters
         a library_id (GR: Global Resource) that is too long. '''
        lib_id, bad_id = setup_tests().setup_test_library_id_gr(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Messages().list_messages(library=lib_id)

    #Test Assertion Error is handled: Short Library id (list_messages: GR)
    def test_responses_long_library_id_lst_msgs_gr(self):
        '''This method tests that an assertion is raised in the Messages Module's list_messages method when the user enters
         a library_id (GR: Global Resource) that is too short. '''
        lib_id, bad_id = setup_tests().setup_test_library_id_gr(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Messages().list_messages(library=lib_id)

    #Test Assertion Error is handled: Incorrect Library id (list_messages: GR)
    def test_responses_bad_libary_id_lst_msgs_gr(self):
        '''This method tests that an assertion is raised in the Messages Module's list_messages method when the user enters
         a library_id (GR: Global Resource) that is incorrect. '''
        lib_id, bad_id = setup_tests().setup_test_library_id_gr(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Messages().list_messages(library=bad_id)

    ## Messages: Library IDs ##
    #Test Assertion Error is handled: Long Library id (get_message: UR)
    def test_responses_short_library_id_get_msg_ur(self):
        '''This method tests that an assertion is raised in the Messages Module's get_message method when the user enters a
        library_id (UR: User-Defined Resource) that is too long. '''
        lib_id, bad_id = setup_tests().setup_test_library_id_ur(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Messages().get_message(library=lib_id, message="MS_ThisIsaFakeMsg!")

    #Test Assertion Error is handled: Short Library id (get_message: UR)
    def test_responses_long_library_id_get_msg_ur(self):
        '''This method tests that an assertion is raised in the Messages Module's get_message method when the user enters a
         library_id (UR: User-Defined Resource) that is too short. '''
        lib_id, bad_id = setup_tests().setup_test_library_id_ur(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Messages().get_message(library=lib_id, message="MS_ThisIsaFakeMsg!")

    #Test Assertion Error is handled: Incorrect Library id (get_message: UR)
    def test_responses_bad_libary_id_get_msg_ur(self):
        '''This method tests that an assertion is raised in the Messages Module's get_message method when the user enters
         a library_id (UR: User-Defined Resource) that is incorrect. '''
        lib_id, bad_id = setup_tests().setup_test_library_id_ur(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Messages().get_message(library=bad_id, message="MS_ThisIsaFakeMsg!")

    #Test Assertion Error is handled: Long Library id (get_message: GR)
    def test_responses_short_library_id_get_msg_gr(self):
        '''This method tests that an assertion is raised in the Messages Module's get_message method when the user enters
         a library_id (GR: Global Resource) that is too long. '''
        lib_id, bad_id = setup_tests().setup_test_library_id_gr(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Messages().get_message(library=lib_id, message="MS_ThisIsaFakeMsg!")

    #Test Assertion Error is handled: Short Library id (get_message: GR)
    def test_responses_long_library_id_get_msg_gr(self):
        '''This method tests that an assertion is raised in the Messages Module's get_message method when the user enters
         a library_id (GR: Global Resource) that is too short. '''
        lib_id, bad_id = setup_tests().setup_test_library_id_gr(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Messages().get_message(library=lib_id, message="MS_ThisIsaFakeMsg!")

    #Test Assertion Error is handled: Incorrect Library id (get_message: GR)
    def test_responses_bad_libary_id_get_msg_gr(self):
        '''This method tests that an assertion is raised in the Messages Module's get_message method when the user enters
         a library_id (GR: Global Resource) that is incorrect. '''
        lib_id, bad_id = setup_tests().setup_test_library_id_gr(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Messages().get_message(library=bad_id, message="MS_ThisIsaFakeMsg!")

    ## Messages: Message IDs ##
    #Test Assertion Error is handled: Long Message ID (get_message)
    def test_responses_short_msg_id_get_msgs(self):
        '''This method tests that an assertion is raised in the Messages Module's get_message method when the user enters a
        message_id that is too long. '''
        msg_id, bad_id = setup_tests().setup_test_message_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Messages().get_message(library="GR_ThisIsaFakeLib!", message=msg_id)

    #Test Assertion Error is handled: Short Message ID (get_message)
    def test_responses_long_msg_id_get_msgs(self):
        '''This method tests that an assertion is raised in the Messages Module's get_message method when the user enters a
         message_id that is too short. '''
        msg_id, bad_id = setup_tests().setup_test_message_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Messages().get_message(library="GR_ThisIsaFakeLib!", message=msg_id)

    #Test Assertion Error is handled: Incorrect Message ID (get_message)
    def test_responses_bad_msg_id_get_msgs(self):
        '''This method tests that an assertion is raised in the Messages Module's get_message method when the user enters
         a message_id that is incorrect. '''
        msg_id, bad_id = setup_tests().setup_test_message_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Messages().get_message(library="GR_ThisIsaFakeLib!", message=msg_id)

    ## Distribution: MailiingList IDs ##
    #Test Assertion Error is handled: Long MailiingListID (create_distribution)
    def test_responses_short_ml_id_create_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters a
        mailing_list_id that is too long. '''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(mailing_list=mailing_list_id, library="GR_ThisIsaFakeLib!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake", survey="SV_ThisIsaFakeID!!")

    #Test Assertion Error is handled: Short MailiingList ID (create_distribution)
    def test_responses_long_ml_id_create_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters a
         mailing_list_id that is too short.'''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(mailing_list=mailing_list_id, library="GR_ThisIsaFakeLib!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake", survey="SV_ThisIsaFakeID!!")

    #Test Assertion Error is handled: Incorrect MailiingList ID (create_distribution)
    def test_responses_bad_ml_id_create_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters
         a mailing_list_id that is incorrect. '''
        mailing_list_id, bad_id = setup_tests().setup_test_mailing_list_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(mailing_list=bad_id, library="GR_ThisIsaFakeLib!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake", survey="SV_ThisIsaFakeID!!")

    ## Distribution: Survey IDs ##
    #Test Assertion Error is handled: Long Survey ID (create_distribution)
    def test_responses_short_sv_id_create_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters a
        survey_id that is too long. '''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(survey=survey_id, mailing_list="CG_ThisIsaFakeMail", library="GR_ThisIsaFakeLib!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Short Survey ID (create_distribution)
    def test_responses_long_sv_id_create_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters a
         survey_id that is too short.'''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(survey=survey_id, mailing_list="CG_ThisIsaFakeMail", library="GR_ThisIsaFakeLib!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Incorrect Survey ID (create_distribution)
    def test_responses_bad_sv_id_create_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters
         a survey_id that is incorrect. '''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(survey=bad_id, mailing_list="CG_ThisIsaFakeMail", library="GR_ThisIsaFakeLib!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    ## Distribution: Survey IDs ##
    #Test Assertion Error is handled: Long Survey ID (list_distributions)
    def test_responses_short_sv_id_list_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's list_distributions method when the user enters a
        survey_id that is too long. '''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().list_distributions(survey=survey_id)

    #Test Assertion Error is handled: Short Survey ID (list_distributions)
    def test_responses_long_sv_id_list_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's list_distributions method when the user enters a
         survey_id that is too short.'''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().list_distributions(survey=survey_id)

    #Test Assertion Error is handled: Incorrect Survey ID (list_distributions)
    def test_responses_bad_sv_id_list_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's list_distributions method when the user enters
         a survey_id that is incorrect. '''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().list_distributions(survey=bad_id)

    ## Distribution: Survey IDs ##
    #Test Assertion Error is handled: Long Survey ID (get_distribution)
    def test_responses_short_sv_id_get_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's get_distributionmethod when the user enters a
        survey_id that is too long. '''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().get_distribution(survey=survey_id, distribution="EMD_ThisIsaFakeID!")

    #Test Assertion Error is handled: Short Survey ID (get_distribution)
    def test_responses_long_sv_id_get_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's get_distribution method when the user enters a
         survey_id that is too short.'''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().get_distribution(survey=survey_id, distribution="EMD_ThisIsaFakeID!")

    #Test Assertion Error is handled: Incorrect Survey ID (get_distribution)
    def test_responses_bad_sv_id_get_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's get_distribution method when the user enters
         a survey_id that is incorrect. '''
        survey_id, bad_id = setup_tests().setup_test_survey_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().get_distribution(survey=bad_id, distribution="EMD_ThisIsaFakeID!")

    ## Distribution: Library IDs (UR) ##
    #Test Assertion Error is handled: Long Library ID (create_distribution: UR)
    def test_responses_short_lib_id_create_dist_ur(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters a
        library_id (UR: User-Defined Resource) that is too long. '''
        library_id, bad_id = setup_tests().setup_test_library_id_ur(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(library=library_id, survey="SV_ThisIsaFakeID!!", mailing_list="CG_ThisIsaFakeMail", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Short Library ID (create_distribution: UR)
    def test_responses_long_lib_id_create_dist_ur(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters a
         library_id (UR: User-Defined Resource) that is too short.'''
        library_id, bad_id = setup_tests().setup_test_library_id_ur(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(library=library_id, survey="SV_ThisIsaFakeID!!", mailing_list="CG_ThisIsaFakeMail", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Incorrect Library ID (create_distribution: UR)
    def test_responses_bad_lib_id_create_dist_ur(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters
         a library_id (UR: User-Defined Resource) that is incorrect. '''
        library_id, bad_id = setup_tests().setup_test_library_id_ur(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(library=bad_id, survey="SV_ThisIsaFakeID!!", mailing_list="CG_ThisIsaFakeMail", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    ## Distribution: Library IDs (GR) ##
    #Test Assertion Error is handled: Long Library ID (create_distribution: GR)
    def test_responses_short_lib_id_create_dist_gr(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters a
        library_id (GR: Global Resource) that is too long. '''
        library_id, bad_id = setup_tests().setup_test_library_id_gr(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(library=library_id, survey="SV_ThisIsaFakeID!!", mailing_list="CG_ThisIsaFakeMail", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Short Library ID (create_distribution: GR)
    def test_responses_long_lib_id_create_dist_gr(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters a
         library_id (GR: Global Resource) that is too short.'''
        library_id, bad_id = setup_tests().setup_test_library_id_gr(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(library=library_id, survey="SV_ThisIsaFakeID!!", mailing_list="CG_ThisIsaFakeMail", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Incorrect Library ID (create_distribution: GR)
    def test_responses_bad_lib_id_create_dist_gr(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters
         a library_id (GR: Global Resource) that is incorrect. '''
        library_id, bad_id = setup_tests().setup_test_library_id_gr(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(library=bad_id, survey="SV_ThisIsaFakeID!!", mailing_list="CG_ThisIsaFakeMail", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    ## Distribution: Library IDs (UR) ##
    #Test Assertion Error is handled: Long Library ID (create_reminder: UR)
    def test_responses_short_lib_id_create_remind_ur(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_reminder method when the user enters a
        library_id (UR: User-Defined Resource) that is too long. '''
        library_id, bad_id = setup_tests().setup_test_library_id_ur(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_reminder(library=library_id, distribution="EMD_ThisIsaFakeID!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Short Library ID (create_reminder: UR)
    def test_responses_long_lib_id_create_remind_ur(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_reminder method when the user enters a
         library_id (UR: User-Defined Resource) that is too short.'''
        library_id, bad_id = setup_tests().setup_test_library_id_ur(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_reminder(library=library_id, distribution="EMD_ThisIsaFakeID!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Incorrect Library ID (create_reminder: UR)
    def test_responses_bad_lib_id_create_remind_ur(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_reminder method when the user enters
         a library_id (UR: User-Defined Resource) that is incorrect. '''
        library_id, bad_id = setup_tests().setup_test_library_id_ur(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_reminder(library=bad_id, distribution="EMD_ThisIsaFakeID!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    ## Distribution: Library IDs (GR) ##
    #Test Assertion Error is handled: Long Library ID (create_reminder: GR)
    def test_responses_short_lib_id_create_remind_gr(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_reminder method when the user enters a
        library_id (GR: Global Resource) that is too long. '''
        library_id, bad_id = setup_tests().setup_test_library_id_gr(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_reminder(library=library_id, distribution="EMD_ThisIsaFakeID!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Short Library ID (create_reminder: GR)
    def test_responses_long_lib_id_create_remind_gr(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_reminder method when the user enters a
         library_id (GR: Global Resource) that is too short.'''
        library_id, bad_id = setup_tests().setup_test_library_id_gr(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_reminder(library=library_id, distribution="EMD_ThisIsaFakeID!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Incorrect Library ID (create_reminder: GR)
    def test_responses_bad_lib_id_create_remind_gr(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_reminder method when the user enters
         a library_id (GR: Global Resource) that is incorrect. '''
        library_id, bad_id = setup_tests().setup_test_library_id_gr(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_reminder(library=bad_id, distribution="EMD_ThisIsaFakeID!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    ## Distribution: Library IDs ##
    #Test Assertion Error is handled: Long Library ID (create_thank_you: UR)
    def test_responses_short_lib_id_create_ty_ur(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_thank_you method when the user enters a
        library_id (UR: User-Defined Resource) that is too long. '''
        library_id, bad_id = setup_tests().setup_test_library_id_ur(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_thank_you(library=library_id, distribution="EMD_ThisIsaFakeID!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Short Library ID (create_thank_you: UR)
    def test_responses_long_lib_id_create_ty_ur(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_thank_you method when the user enters a
         library_id (UR: User-Defined Resource) that is too short.'''
        library_id, bad_id = setup_tests().setup_test_library_id_ur(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_thank_you(library=library_id, distribution="EMD_ThisIsaFakeID!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Incorrect Library ID (create_thank_you: UR)
    def test_responses_bad_lib_id_create_ty_ur(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_thank_you method when the user enters
         a library_id (UR: User-Defined Resource) that is incorrect. '''
        library_id, bad_id = setup_tests().setup_test_library_id_ur(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_thank_you(library=bad_id, distribution="EMD_ThisIsaFakeID!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    ## Distribution: Library IDs (GR) ##
    #Test Assertion Error is handled: Long Library ID (create_reminder: GR)
    def test_responses_short_lib_id_create_ty_gr(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_thank_you method when the user enters a
        library_id (GR: Global Resource) that is too long. '''
        library_id, bad_id = setup_tests().setup_test_library_id_gr(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_thank_you(library=library_id, distribution="EMD_ThisIsaFakeID!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Short Library ID (create_reminder: GR)
    def test_responses_long_lib_id_create_ty_gr(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_thank_you method when the user enters a
         library_id (GR: Global Resource) that is too short.'''
        library_id, bad_id = setup_tests().setup_test_library_id_gr(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_thank_you(library=library_id, distribution="EMD_ThisIsaFakeID!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Incorrect Library ID (create_reminder: GR)
    def test_responses_bad_lib_id_create_ty_gr(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_thank_you method when the user enters
         a library_id (GR: Global Resource) that is incorrect. '''
        library_id, bad_id = setup_tests().setup_test_library_id_gr(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_thank_you(library=bad_id, distribution="EMD_ThisIsaFakeID!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    ## Distribution: Distribution IDs ##
    #Test Assertion Error is handled: Long Distribution ID (get_distribution)
    def test_responses_short_dist_id_get_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's get_distribution method when the user enters a
        distribution_id that is too long. '''
        dist_id, bad_id = setup_tests().setup_test_dist_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().get_distribution(survey="SV_ThisIsaFakeID!!", distribution=dist_id)

    #Test Assertion Error is handled: Short Distribution ID (get_distribution)
    def test_responses_long_dist_id_get_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's get_distribution method when the user enters a
         distribution_id that is too short.'''
        dist_id, bad_id = setup_tests().setup_test_dist_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().get_distribution(survey="SV_ThisIsaFakeID!!", distribution=dist_id)

    #Test Assertion Error is handled: Incorrect Distribution ID (get_distribution)
    def test_responses_bad_dist_id_get_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's get_distribution method when the user enters
         a distribution_id that is incorrect. '''
        dist_id, bad_id = setup_tests().setup_test_dist_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().get_distribution(survey="SV_ThisIsaFakeID!!", distribution=bad_id)

    ## Distribution. Distribution IDs ##
    #Test Assertion Error is handled: Long Distribution ID (create_reminder)
    def test_responses_short_dist_id_create_remind(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_reminder method when the user enters a
        distrubution_id that is too long. '''
        distribution_id, bad_id = setup_tests().setup_test_dist_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_reminder(distribution=distribution_id, library="GR_ThisIsaFakeLib!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Short Distribution ID (create_reminder)
    def test_responses_long_dist_id_create_remind(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_reminder method when the user enters a
         distrubution_id that is too short.'''
        distribution_id, bad_id = setup_tests().setup_test_dist_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_reminder(distribution=distribution_id, library="GR_ThisIsaFakeLib!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Incorrect Distribution ID (create_reminder)
    def test_responses_bad_dist_id_create_remind(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_reminder method when the user enters
         a distrubution_id that is incorrect. '''
        distribution_id, bad_id = setup_tests().setup_test_dist_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_reminder(distribution=bad_id, library="GR_ThisIsaFakeLib!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    ## Distribution: Distribution IDs ##
    #Test Assertion Error is handled: Long Distribution ID (create_thank_you)
    def test_responses_short_dist_id_create_ty(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_thank_you method when the user enters a
        distrubution_id that is too long. '''
        distribution_id, bad_id = setup_tests().setup_test_dist_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_thank_you(distribution=distribution_id, library="GR_ThisIsaFakeLib!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Short Distribution ID (create_thank_you)
    def test_responses_long_dist_id_create_ty(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_thank_you method when the user enters a
         distrubution_id that is too short.'''
        distribution_id, bad_id = setup_tests().setup_test_dist_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_thank_you(distribution=distribution_id, library="GR_ThisIsaFakeLib!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Incorrect Distribution ID (create_thank_you)
    def test_responses_bad_dist_id_create_ty(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_thank_you method when the user enters
         a distrubution_id that is incorrect. '''
        distribution_id, bad_id = setup_tests().setup_test_dist_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_thank_you(distribution=bad_id, library="GR_ThisIsaFakeLib!", message="MS_ThisIsaFakeMsg!", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    ## Distribution: Message IDs ##
    #Test Assertion Error is handled: Long Message ID (create_distribution)
    def test_responses_short_msg_id_create_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters a
        message_id that is too long. '''
        msg_id, bad_id = setup_tests().setup_test_message_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(message=msg_id, library="GR_ThisIsaFakeLib!", survey="SV_ThisIsaFakeID!!", mailing_list="CG_ThisIsaFakeMail", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Short Message ID (create_distribution)
    def test_responses_long_msg_id_create_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters a
         message_id that is too short.'''
        msg_id, bad_id = setup_tests().setup_test_message_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(message=msg_id ,library="GR_ThisIsaFakeLib!", survey="SV_ThisIsaFakeID!!", mailing_list="CG_ThisIsaFakeMail", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Incorrect Message ID (create_distribution)
    def test_responses_bad_msg_id_create_dist(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_distribution method when the user enters
         a message_id that is incorrect. '''
        msg_id, bad_id = setup_tests().setup_test_message_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_distribution(message=bad_id, library="GR_ThisIsaFakeLib!", survey="SV_ThisIsaFakeID!!", mailing_list="CG_ThisIsaFakeMail", subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    ## Distribution: Message IDs ##
    #Test Assertion Error is handled: Long Message ID (create_reminder)
    def test_responses_short_msg_id_create_remind(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_reminder method when the user enters a
        message_id that is too long. '''
        msg_id, bad_id = setup_tests().setup_test_message_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_reminder(distribution="EMD_ThisIsaFakeID!", library="GR_ThisIsaFakeLib!", message=msg_id, subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Short Message ID (create_reminder)
    def test_responses_long_msg_id_create_remind(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_reminder method when the user enters a
         message_id that is too short.'''
        msg_id, bad_id = setup_tests().setup_test_message_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_reminder(distribution="EMD_ThisIsaFakeID!", library="GR_ThisIsaFakeLib!", message=msg_id, subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Incorrect Message ID (create_reminder)
    def test_responses_bad_msg_id_create_remind(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_reminder method when the user enters
         a message_id that is incorrect. '''
        msg_id, bad_id = setup_tests().setup_test_message_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_reminder(distribution="EMD_ThisIsaFakeID!", library="GR_ThisIsaFakeLib!", message=bad_id, subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    ## Distribution Message IDs ##
    #Test Assertion Error is handled: Long Message ID (create_thank_you)
    def test_responses_short_msg_id_create_ty(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_thank_you method when the user enters a
        message_id that is too long. '''
        msg_id, bad_id = setup_tests().setup_test_message_id(short=False, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_thank_you(distribution="EMD_ThisIsaFakeID!", library="GR_ThisIsaFakeLib!", message=msg_id, subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Short Message ID (create_thank_you)
    def test_responses_long_msg_id_create_ty(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_thank_you method when the user enters a
         message_id that is too short.'''
        msg_id, bad_id = setup_tests().setup_test_message_id(short=True, false_id=False)
        with self.assertRaises(AssertionError):
            Distributions().create_thank_you(distribution="EMD_ThisIsaFakeID!", library="GR_ThisIsaFakeLib!", message=msg_id, subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

    #Test Assertion Error is handled: Incorrect Message ID (create_thank_you)
    def test_responses_bad_msg_id_create_ty(self):
        '''This method tests that an assertion is raised in the Distribution Module's create_thank_you method when the user enters
         a message_id that is incorrect. '''
        msg_id, bad_id = setup_tests().setup_test_message_id(short=False, false_id=True)
        with self.assertRaises(AssertionError):
            Distributions().create_thank_you(distribution="EMD_ThisIsaFakeID!", library="GR_ThisIsaFakeLib!", message=bad_id, subject="Fake", reply_email="Fake@Fake.com", from_email="Fake@Fake.com", from_name="Fake")

if __name__ == "__main__":
    unittest.main()
