import requests as r
import zipfile
import json
import io
import pandas as pd
from time import gmtime, strftime
from datetime import date
import datetime
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Exceptions import ServerError

class Distributions(Credentials):
    '''This is a child class to the credentials class that gathers information about from Qualtrics Distributions.'''

    def __init__(self, token=None, directory_id=None, data_center=None):
        self.token = token
        self.data_center = data_center
        self.directory_id = directory_id
        return


    def create_distribution(self, subject, reply_email, from_email, from_name, mailing_list, library, survey, message, link_type='Individual',):

        # Use for Assert Statements
        '''
        directoryId = "POOL_9H1MGk0YcdGVXKt"
        mailingListId = "CG_bNn39KKI3zmfTeJ"
        messageId = 'MS_1Mt2Nj5kczdnjMh'
        libraryId = 'UR_8cRedheujEbcxgN'
        surveyId = 'SV_cOPSAfYR8XR3TqR'
        '''

        headers, url = self.header_setup(content_type=True, responses=False, distributions=True)
        data = {
            'header': {
                'fromEmail': from_email,
                'fromName': from_name,
                'replyToEmail': reply_email,
                'subject': subject
            },
            'surveyLink': {
                'surveyId': survey,
                'type': 'Individual'
            },
            'recipients': {
                'mailingListId': mailing_list
            },
            'sendDate': strftime('%Y-%m-%dT%H:%M:%SZ', gmtime()),
            'message': {
                    'libraryId': library,
                    'messageID': message
            }
        }
        request = r.post(url, json=data, headers=headers)
        response = request.json()
        return

# Get Distributions

#Create Reminder

#Create Thank you
