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

    def create_distribution(self, subject, reply_email, from_email, from_name, mailing_list, library, survey, message, send_date=gmtime(), link_type='Individual'):
        '''This method gives users the ability to create a distribution for a given mailing list and survey. In order to use this method you
        must already have access to pre-defined Messages and their MessageID's existing within a User-Defined (starts with UR_)
        or Global (starts with GR_) Library. You can list the messages and their MessageID's(starts with MS_)  that are available to your user
        account by using the "QualtricsAPI.Library.Messages.list_messages()" method. As a final note, this method gives users the ability to
        define the different types of


        :param subject: The subject for the reminder email.
        :type subject: str
        :param reply_email: The reply email address.
        :type reply_email: str
        :param from_email: The email address that the distribution is sent from.
        :type from_email: str
        :param from_name: The name that shows up on the distribution.
        :type from_name: str
        :param library: The (Global or User) Library ID which the messages are located within.
        :type library: str
        :param message: The Message ID corresponding with the message that is to be sent.
        :type message: str
        :param mailing_list: The Mailing List ID corresponding with the Mailing List that the distribution is to be sent to.
        :type mailing_list: str
        :param survey: The Survey ID corresponding with the Survey that the distribution is to be sent to.
        :type survey: str
        :param send_date: The date that the distribution is supposed to be sent on. Default Behavior is the current time.
        :type send_date:
        :param link_type: This parameter refers to the type of link that is to be sent within the distribution.
        :type link_type: str
        '''

        assert len(mailing_list) == 18, 'Hey, the parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert len(library) == 18, 'Hey, the parameter for "library" that was passed is the wrong length. It should have 18 characters.'
        assert len(survey) == 18, 'Hey, the parameter for "survey" that was passed is the wrong length. It should have 18 characters.'
        assert len(message) == 18, 'Hey, the parameter for "message" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.'
        assert survey[:3] == 'SV_', 'Hey there! It looks like your SurveyID is incorrect. You can find the SurveyID on the Qualtrics site under your account settings. It will begin with "SV_". Please try again.'
        assert message[:3] == 'MS_', 'Hey there! It looks like your MessageID is incorrect. You can find the MessageID by using the list messages method available in the Messages module of this Package. It will begin with "MS_". Please try again.'

        try:
            headers, url = self.header_setup(content_type=True, xm=False, path='distributions')
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
                'sendDate': strftime('%Y-%m-%dT%H:%M:%SZ', send_date),
                'message': {
                        'libraryId': library,
                        'messageId': message
                }
            }

            request = r.post(url, json=data, headers=headers)
            response = request.json()
            distribution_id = response['result']['id']
            return distribution_id
        except:
            print(f"\nServerError:\nQualtricsAPI Error Code: {response['meta']['error']['errorCode']}\nQualtricsAPI Error Message: {response['meta']['error']['errorMessage']}")
        return

    def create_reminder(self, subject, reply_email, from_email, from_name, library, message, distribution, send_date=gmtime()):
        '''This method gives users the ability to create a reminder for a given distribution. In order to create a reminders you must have
        already created a distribution for a given mailing list and survey. Once created, you will pass the Distribution ID corresponding to
        the correct distribution to the distribution parameter and the reminder will be set to that specific distribution. Unlike the
        QualtricsAPI.Survey.Distribution.create_distribution() method, this method does not require you to specify the mailing list or survey
        because it will use the parameters defined when the associated distribution was set up.

        :param subject: The subject for the reminder email.
        :type subject: str
        :param reply_email: The reply email address.
        :type reply_email: str
        :param from_email: The email address that the reminder is sent from.
        :type from_email: str
        :param from_name: The name that shows up on the reminder.
        :type from_name: str
        :param library: The (Global or User) Library ID which the messages are located within.
        :type library: str
        :param message: The Message ID corresponding with the message that is to be sent.
        :type message: str
        :param distribution: The Distribution ID corresponding with the distribution that the reminder is to be attached to.
        :type distribution: str
        :param send_date: The date that the reminder is supposed to be sent on. Default Behavior is the current time.
        :type send_date:
        '''

        assert len(distribution) == 19, 'Hey, the parameter for "distribution" that was passed is the wrong length. It should have 19 characters.'
        assert len(library) == 18, 'Hey, the parameter for "library" that was passed is the wrong length. It should have 18 characters.'
        assert len(message) == 18, 'Hey, the parameter for "message" that was passed is the wrong length. It should have 18 characters.'
        assert distribution[:4] == 'UMD_', 'Hey there! It looks like your distributionID is incorrect. You can find the distributionID by using the list_distributions method in this module. It will begin with "UMD_". Please try again.'
        assert message[:3] == 'MS_', 'Hey there! It looks like your MessageID is incorrect. You can find the MessageID by using the list messages method available in the Messages module of this Package. It will begin with "MS_". Please try again.'

        headers, base_url = self.header_setup(content_type=True, xm=False, path='distributions')
        url = base_url + f'/{distribution}/reminders'
        data = {
            'header': {
                'fromEmail': from_email,
                'fromName': from_name,
                'replyToEmail': reply_email,
                'subject': subject
            },
            'sendDate': strftime('%Y-%m-%dT%H:%M:%SZ', send_date),
            'message': {
                    'libraryId': library,
                    'messageId': message
            }
        }

        request = r.post(url, json=data, headers=headers)
        response = request.json()
        reminder_id = response['result']
        return reminder_id

    def create_thank_you(self, subject, reply_email, from_email, from_name, library, message, distribution, send_date=gmtime()):
        '''This method gives users the ability to create a thank you for a given distribution. In order to create thank you distributions,
         you must have already created a distribution for a given mailing list and survey. Once created, you will pass the Distribution ID
         corresponding to the correct distribution to the distribution parameter and the reminder will be set to that specific distribution.
         Unlike the  QualtricsAPI.Survey.Distribution.create_distribution() method, this method does not require you to specify the mailing
         list or survey because it will use the parameters defined when the associated distribution was set up.

        :param subject: The subject for the reminder email.
        :type subject: str
        :param reply_email: The reply email address.
        :type reply_email: str
        :param from_email: The email address that the reminder is sent from.
        :type from_email: str
        :param from_name: The name that shows up on the reminder.
        :type from_name: str
        :param library: The (Global or User) Library ID which the messages are located within.
        :type library: str
        :param message: The Message ID corresponding with the message that is to be sent.
        :type message: str
        :param distribution: The Distribution ID corresponding with the distribution that the reminder is to be attached to.
        :type distribution: str
        :param send_date: The date that the reminder is supposed to be sent on. Default Behavior is the current time.
        :type send_date:
        '''

        assert len(distribution) == 19, 'Hey, the parameter for "distribution" that was passed is the wrong length. It should have 19 characters.'
        assert len(library) == 18, 'Hey, the parameter for "library" that was passed is the wrong length. It should have 18 characters.'
        assert len(message) == 18, 'Hey, the parameter for "message" that was passed is the wrong length. It should have 18 characters.'
        assert distribution[:4] == 'UMD_', 'Hey there! It looks like your distributionID is incorrect. You can find the distributionID by using the list_distributions method in this module. It will begin with "UMD_". Please try again.'
        assert message[:3] == 'MS_', 'Hey there! It looks like your MessageID is incorrect. You can find the MessageID by using the list messages method available in the Messages module of this Package. It will begin with "MS_". Please try again.'

        headers, base_url = self.header_setup(content_type=True, xm=False, path='distributions')
        url = base_url + f'/{distribution}/thankyous'
        data = {
            'header': {
                'fromEmail': from_email,
                'fromName': from_name,
                'replyToEmail': reply_email,
                'subject': subject
            },
            'sendDate': strftime('%Y-%m-%dT%H:%M:%SZ', send_date),
            'message': {
                    'libraryId': library,
                    'messageId': message
            }
        }
        request = r.post(url, json=data, headers=headers)
        response = request.json()
        thanks_id = response['result']
        return thanks_id

    def list_distributions(self, survey):
        ''' This method will list all of the distributions corresponding with a given survey.

        :param survey: The Survey ID corresponding with the Survey that the distribution is to be sent to.
        :type survey: str
        '''
        headers, base_url = self.header_setup(xm=False, path='distributions')
        url = base_url + f'?surveyId={survey}'
        request = r.get(url, headers=headers)
        response = request.json()
        #Needs to convert to pandas DataFrame
        return response

    def get_distribution(self, survey, distribution):
        ''' This method gives users the ability to get a specific distribution corresponding with a given survey.

        :param survey: The Survey ID corresponding with the Survey that the distribution is to be sent to.
        :type survey: str
        :param distribution: A specific Distribution ID associated with the given survey.
        :type distribution: str
        '''

        headers, base_url = self.header_setup(xm=False, path='distributions')
        url = base_url + f'/{distribution}?surveyId={survey}'
        request = r.get(url, headers=headers)
        response = request.json()
        #Need to convert to Pandas DataFrame
        return response
