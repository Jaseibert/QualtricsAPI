#Imports
import unittest
import requests as r
import json
import time as t
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Contacts import XMDirectory, MailingList
from QualtricsAPI.Survey import Responses

# Setup Tests Class
class setup_tests(object):

    def __init__(self):
        return

    # Test Case 1: qualtrics_api_credentials parameter lengths
    def setup_test_token(self, short=False):
        '''Setup for Test Case 1: qualtrics_api_credentials token parameter lengths'''
        token = 'ThisIsaFakeAPITokenAndIsTooShortToWork!' if short else 'ThisIsaFakeAPITokenAndIsTooShortToWork!!!'
        return token

    def setup_test_dictionary_id(self, short=False, false_id=False):
        '''Setup for Test Case 2: qualtrics_api_credentials dictionary id parameter lengths, and the incorrect id. '''
        #len(20) Start(POOL_)
        #Setup a short Dictionary id
        #Setup a Long Dictonary id
        #Setup false id
        return

    def setup_test_mailing_list_id(self, short=False, false_id=False):
        '''Setup for Test Case 3: Mailing List Sub-Module method's exception handling.'''
        #len(18) start(CG_)
        #Setup a short MailingList id
        #Setup a Long MailingList id
        #Setup False id
        return

    def setup_test_contact_id(self, short=False, false_id=False):
        '''Setup for Test Case 4: XMDirectory Sub-Module method's exception handling.'''
        #Len(19) Start(CID_)
        #Setup a short Contact id
        #Setup a Long Contact id
        #Setup False id
        return

    def setup_test_survey_id(self, short=False, false_id=False):
        '''Setup for Test Case 5: Responses Sub-Module method's exception handling.'''
        #len(18) and Start (SV_)
        #Setup a short Survey id
        #Setup a Long Survey id
        #Setup False id
        return

    def setup_methods(self, module=None):
        #if 'mailing'
            #return an object that will hold all of the methods that are needing to be tested.
        #elif 'xm'
            #return an object that will hold all of the methods that are needing to be tested.
        #elif 'responses'
            #return an object that will hold all of the methods that are needing to be tested.
        return

    def setup_itterator():
        #for method in setup_methods
        #test a given set of exceptions
        return

#UnitTest Class
class TestQualtricsAPI(unittest.TestCase):

    ## API Credentials: Token ##
    #Test Assertion Error is handled: Short Token
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
