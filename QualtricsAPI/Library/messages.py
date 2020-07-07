import requests as r
import zipfile
import json
import io
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser

class Messages(Credentials):
    '''This is a child class to the Credentials class and it gathers information about Qualtric's Messages.'''

    def __init__(self, token=None, directory_id=None, data_center=None):
        self.token = token
        self.data_center = data_center
        self.directory_id = directory_id
        return

    def list_messages(self, library=None):
        '''This method gets the all of the messages available to a user in a given library. Messages are defined based on
        the library (User-Deifined or Global) that they exist within. Thus, in order to list the messages availble to your
        user account, you need to specify the library that the api must look within. There can exist several different
        categories of messages. These include, 'invite', 'inactiveSurvey', 'reminder', 'thankYou', 'smsInvite', 'validation',
        'emailSubject', 'general', 'lookAndFeel', and 'endOfSurvey'. This method returns all the types of these, if they exist.

        :param library: The (Global or User) Library ID which the messages are located within.
        :type library: str
        :return: A Pandas DataFrame
        '''

        assert len(library) == 18, 'Hey, the parameter for the Libary ID that was passed is the wrong length. It should have 18 characters.'
        assert library[:3] == 'UR_' or library[:3] == 'GR_', 'Hey there! It looks like your Library ID is incorrect. You can find the Library ID on the Qualtrics site under your account settings. It will begin with "UR_" or "GR_". Please try again.'


        # Need Recursion to handle nextPage Errors
        headers, base_url = self.header_setup(xm=False, path='libraries')
        url = base_url + f"/{library}/messages/"
        request = r.get(url, headers=headers)
        response = request.json()
        try:
            keys = ['id', 'description', 'category']
            messages = Parser().json_parser(response=response['result'], keys=keys, arr=False)
            msg_df = pd.DataFrame(messages).transpose()
            msg_df.columns = ['MessageID', 'MessageDescription', 'MessageCategory']
            msg_df['LibraryID'] = library
        except:
            print(f"\nServerError: QualtricsAPI Error Code: {response['meta']['error']['errorCode']}\nQualtricsAPI Error Message: {response['meta']['error']['errorMessage']}")
        return msg_df

    def get_message(self, library=None, message=None):
        '''This method gets the messages available to a user in a given library. Messages are defined based on the library
        (User-Deifined or Global) that they exist within. Thus, in order to query the correct message we must pass the
        associated libraryID into the library parameter, along with the MessageID into the message parameter. There can exist
        several different categories of messages. These include, 'invite', 'inactiveSurvey', 'reminder', 'thankYou', 'smsInvite',
        'validation', 'emailSubject', 'general', 'lookAndFeel', and 'endOfSurvey'. This method returns any type of these, if they
        exist.

        :param library: The (Global or User) Library ID which the messages are located within.
        :type library: str
        :param message: The Message ID corresponding specific message.
        :type message: str
        :return: A tuple containing the MessageID, MessageCategory, and MessageDescription
        '''

        assert len(library) == 18, 'Hey, the parameter for "library" that was passed is the wrong length. It should have 18 characters.'
        assert len(message) == 18, 'Hey, the parameter for "message" that was passed is the wrong length. It should have 18 characters.'
        assert message[:3] == 'MS_', 'Hey there! It looks like your MessageID is incorrect. You can find the MessageID by using the list messages method available in the Messages module of this Package. It will begin with "MS_". Please try again.'
        assert library[:3] == 'UR_' or library[:3] == 'GR_', 'Hey there! It looks like your Library ID is incorrect. You can find the Library ID on the Qualtrics site under your account settings. It will begin with "UR_" or "GR_". Please try again.'


        headers, base_url = self.header_setup(xm=False, path='libraries')
        url = base_url + f"/{library}/messages/{message}"
        request = r.get(url, headers=headers)
        response = request.json()
        try:
            msg_html = response['result']['messages']['en']
        except:
            print(f"\nServerError: QualtricsAPI Error Code: {response['meta']['error']['errorCode']}\nQualtricsAPI Error Message: {response['meta']['error']['errorMessage']}")
        return message, response['result']['category'], response['result']['description']
