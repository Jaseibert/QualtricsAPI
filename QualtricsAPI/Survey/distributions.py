import requests as r
import pandas as pd
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Exceptions import Qualtrics500Error, Qualtrics503Error, Qualtrics504Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error
from time import sleep


class Distributions(Credentials):
    '''This is a child class to the credentials class and gathers information about  Qualtric's Distributions.'''

    def __init__(self, token=None, directory_id=None, data_center=None):
        self.token = token
        self.data_center = data_center
        self.directory_id = directory_id
        return

    def set_send_date(self, weeks=0, days=0, hours=0, minutes=0, seconds=0):
        '''This method is a helper function to format the send date arguments for several methods in the Distribution Module.
        The send_date parameter must be in the format ""%Y-%m-%dT%H:%M:%SZ" in order for the API to properly parse the send date.
        Thus, this method defines the offset for the send_date, and formats it properly. An example would be if you wanted to send
        a reminder one week from now, simply pass "1" as an argument in to the "weeks" parameter. The default behaviour is for the
        send_date to be now, thus all params are set to zero offset.

        :param weeks: The week offset for the send_date. [Default = 0]
        :type weeks: int
        :param days: The day offset for the send_date. [Default = 0]
        :type days: int
        :param hours: The hour offset for the send_date. [Default = 0]
        :type hours: int
        :param minutes: The minute offset for the send_date. [Default = 0]
        :type minutes: int
        :param seconds: The second offset for the send_date. [Default = 0]
        :type seconds: int
        :return: The formatted DateTime. (str)
        '''
        send_date = datetime.now() + timedelta(weeks=weeks, days=days,
                                               hours=hours, minutes=minutes, seconds=seconds)
        return date.strftime(send_date, '%Y-%m-%dT%H:%M:%SZ')

    def create_distribution(self, subject, reply_email, from_email, from_name, mailing_list, library, survey, message, send_date, link_type='Individual'):
        '''This method gives users the ability to create a distribution for a given mailing list and survey. In order to use this method you
        must already have access to pre-defined Messages and their MessageID's existing within a User-Defined (starts with UR)
        or Global (starts with GR) Library. You can list the messages and their MessageID's(starts with MS)  that are available to your user
        account by using the "QualtricsAPI.Library.Messages.list_messages()" method. As a final note, this method gives users the ability to
        define the different types of messages.

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
        :param send_date: The date that the distribution is supposed to be sent on. Pass gmtime() for immediate distribution or use the set_send_date() method to format properly.
        :type send_date: str
        :param link_type: This parameter refers to the type of link that is to be sent within the distribution.
        :type link_type: str
        :return: The Distribution ID. (str)
        '''

        assert len(mailing_list) == 18, 'Hey, the parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert len(
            library) == 18, 'Hey, the parameter for "library" that was passed is the wrong length. It should have 18 characters.'
        assert len(
            survey) == 18, 'Hey, the parameter for "survey" that was passed is the wrong length. It should have 18 characters.'
        assert len(
            message) == 18, 'Hey, the parameter for "message" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.'
        assert survey[:3] == 'SV_', 'Hey there! It looks like your SurveyID is incorrect. You can find the SurveyID on the Qualtrics site under your account settings. It will begin with "SV_". Please try again.'
        assert message[:3] == 'MS_', 'Hey there! It looks like your MessageID is incorrect. You can find the MessageID by using the list messages method available in the Messages module of this Package. It will begin with "MS_". Please try again.'
        assert library[:3] == 'UR_' or library[:3] == 'GR_', 'Hey there! It looks like your Library ID is incorrect. You can find the Library ID on the Qualtrics site under your account settings. It will begin with "UR_" or "GR_". Please try again.'

        headers, url = self.header_setup(
            content_type=True, xm=False, path='distributions')
        data = {
            'header': {
                'fromEmail': from_email,
                'fromName': from_name,
                'replyToEmail': reply_email,
                'subject': subject
            },
            'surveyLink': {
                'surveyId': survey,
                'type': link_type
            },
            'recipients': {
                'mailingListId': mailing_list
            },
            'sendDate': send_date,
            'message': {
                'libraryId': library,
                'messageId': message
            }
        }

        request = r.post(url, json=data, headers=headers)
        response = request.json()
        try:
            distribution_id = response['result']['id']
            return distribution_id
        except:
            print(
                f"\nServerError: QualtricsAPI Error Code: {response['meta']['error']['errorCode']}\nQualtricsAPI Error Message: {response['meta']['error']['errorMessage']}")
        return

    def create_reminder(self, subject, reply_email, from_email, from_name, library, message, distribution, send_date):
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
        :param send_date: The date that the reminder is supposed to be sent on. Pass gmtime() for immediate distribution or use the set_send_date() method to format properly.
        :type send_date: str
        :return: The "Reminder" Distribution ID. (str)
        '''

        assert len(distribution) == 19, 'Hey, the parameter for "distribution" that was passed is the wrong length. It should have 19 characters.'
        assert len(
            library) == 18, 'Hey, the parameter for "library" that was passed is the wrong length. It should have 18 characters.'
        assert len(
            message) == 18, 'Hey, the parameter for "message" that was passed is the wrong length. It should have 18 characters.'
        assert distribution[:4] == 'EMD_', 'Hey there! It looks like your distributionID is incorrect. You can find the distributionID by using the list_distributions method in this module. It will begin with "UMD_". Please try again.'
        assert message[:3] == 'MS_', 'Hey there! It looks like your MessageID is incorrect. You can find the MessageID by using the list messages method available in the Messages module of this Package. It will begin with "MS_". Please try again.'
        assert library[:3] == 'UR_' or library[:3] == 'GR_', 'Hey there! It looks like your Library ID is incorrect. You can find the Library ID on the Qualtrics site under your account settings. It will begin with "UR_" or "GR_". Please try again.'

        headers, base_url = self.header_setup(
            content_type=True, xm=False, path='distributions')
        url = f'{base_url}/{distribution}/reminders'
        data = {
            'header': {
                'fromEmail': from_email,
                'fromName': from_name,
                'replyToEmail': reply_email,
                'subject': subject
            },
            'sendDate': send_date,
            'message': {
                'libraryId': library,
                'messageId': message
            }
        }

        request = r.post(url, json=data, headers=headers)
        response = request.json()
        try:
            reminder_id = response['result']
            return reminder_id
        except:
            print(
                f"\nServerError: QualtricsAPI Error Code: {response['meta']['error']['errorCode']}\nQualtricsAPI Error Message: {response['meta']['error']['errorMessage']}")
        return

    def create_thank_you(self, subject, reply_email, from_email, from_name, library, message, distribution, send_date):
        '''This method gives users the ability to create a thank you for a given distribution. In order to create thank you distributions you
        must have already created a distribution for a given mailing list and survey. Once created, you will pass the Distribution ID
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
        :param send_date: The date that the reminder is supposed to be sent on. Pass gmtime() for immediate distribution or use the set_send_date() method to format properly.
        :type send_date: str
        :return: The "Thank You" Distribution ID. (str)
        '''

        assert len(distribution) == 19, 'Hey, the parameter for "distribution" that was passed is the wrong length. It should have 19 characters.'
        assert len(
            library) == 18, 'Hey, the parameter for "library" that was passed is the wrong length. It should have 18 characters.'
        assert len(
            message) == 18, 'Hey, the parameter for "message" that was passed is the wrong length. It should have 18 characters.'
        assert distribution[:4] == 'EMD_', 'Hey there! It looks like your distributionID is incorrect. You can find the distributionID by using the list_distributions method in this module. It will begin with "UMD_". Please try again.'
        assert message[:3] == 'MS_', 'Hey there! It looks like your MessageID is incorrect. You can find the MessageID by using the list messages method available in the Messages module of this Package. It will begin with "MS_". Please try again.'
        assert library[:3] == 'UR_' or library[:3] == 'GR_', 'Hey there! It looks like your Library ID is incorrect. You can find the Library ID on the Qualtrics site under your account settings. It will begin with "UR_" or "GR_". Please try again.'

        headers, base_url = self.header_setup(
            content_type=True, xm=False, path='distributions')
        url = f'{base_url}/{distribution}/thankyous'
        data = {
            'header': {
                'fromEmail': from_email,
                'fromName': from_name,
                'replyToEmail': reply_email,
                'subject': subject
            },
            'sendDate': send_date,
            'message': {
                'libraryId': library,
                'messageId': message
            }
        }
        request = r.post(url, json=data, headers=headers)
        response = request.json()
        try:
            thanks_id = response['result']
            return thanks_id
        except:
            print(
                f"\nServerError: QualtricsAPI Error Code: {response['meta']['error']['errorCode']}\nQualtricsAPI Error Message: {response['meta']['error']['errorMessage']}")
        return

    def list_distributions(self, survey):
        ''' This method will list all of the distributions corresponding with a given survey. Given that distributions are
        specific to individual surveys, we must pass the SurveyID as an arguement into the survey parameter for this method
        to work appropriately. This method will return a Pandas DataFrame filled with a list of the distributions associated
        with the specific SurveyID passed to the survey parameter.

        :param survey: The Survey ID corresponding with the Survey that the distribution is to be sent to.
        :type survey: str
        :return: A Pandas DataFrame
        '''

        assert survey[:3] == 'SV_', 'Hey there! It looks like your SurveyID is incorrect. You can find the SurveyID on the Qualtrics site under your account settings. It will begin with "SV_". Please try again.'
        assert len(
            survey) == 18, 'Hey, the parameter for "survey" that was passed is the wrong length. It should have 18 characters.'

        headers, base_url = self.header_setup(xm=False, path='distributions')
        url = f'{base_url}?surveyId={survey}'
        columns = ['id', 'parentDistributionId', 'ownerId', 'organizationId', 'requestStatus', 'requestType',
                   'sendDate', 'createdDate', 'modifiedDate', 'headers', 'fromEmail', 'replyToEmail', 'fromName',
                   'subject', 'recipients', 'mailingListId', 'contactId', 'sampleId', 'message', 'messageId',
                   'messageText', 'surveyLink', 'surveyId', 'expirationDate', 'linkType', 'stats', 'sent', 'failed',
                   'started', 'bounced', 'opened', 'skipped', 'finished', 'complaints', 'blocked', 'mailing_list_library_id', 'message_library_id']
        master = pd.DataFrame(columns=columns)

        def extract_distributions(url=url, master=master):
            request = r.get(url, headers=headers)
            response = request.json()
            if response['meta']['httpStatus'] == '200 - OK':
                keys = columns[:-2]
                dists = Parser().json_parser(response=response, keys=keys, arr=False)
                dist_df = pd.DataFrame(dists).transpose()
                dist_df.columns = keys
                library_ids = Parser().json_parser(
                    response=response, keys=['libraryId'], arr=False)
                dist_df['mailing_list_library_id'] = library_ids[0][:len(
                    dist_df)]
                dist_df['message_library_id'] = library_ids[0][len(dist_df):]
                master = pd.concat([master, dist_df],
                                   sort=False).reset_index(drop=True)
                next_page = response['result']['nextPage']
                return master, next_page
            else:
                print(response['meta'])
                master, next_page = extract_distributions(
                    url=url, master=master)

        master, next_page = extract_distributions()
        if next_page == None:
            return master
        else:
            while next_page != None:
                master, next_page = extract_distributions(
                    url=next_page, master=master)
            return master

    def get_distribution(self, survey, distribution):
        ''' This method gives users the ability to get a specific distribution corresponding with a given survey. Given that
        distributions are specific to individual surveys, we must pass the SurveyID as an arguement into the survey parameter for
        this method to work appropriately. This method will return a Pandas DataFrame consisting of multiple variables associated
        with the specified distirbution.

        :param survey: The Survey ID corresponding with the Survey that the distribution is to be sent to.
        :type survey: str
        :param distribution: A specific Distribution ID associated with the given survey.
        :type distribution: str
        :return: A Pandas DataFrame
        '''

        assert survey[:3] == 'SV_', 'Hey there! It looks like your SurveyID is incorrect. You can find the SurveyID on the Qualtrics site under your account settings. It will begin with "SV_". Please try again.'
        assert len(
            survey) == 18, 'Hey, the parameter for "survey" that was passed is the wrong length. It should have 18 characters.'
        assert len(distribution) == 19, 'Hey, the parameter for "distribution" that was passed is the wrong length. It should have 19 characters.'
        assert distribution[:4] == 'EMD_', 'Hey there! It looks like your distributionID is incorrect. You can find the distributionID by using the list_distributions method in this module. It will begin with "UMD_". Please try again.'

        headers, base_url = self.header_setup(xm=False, path='distributions')
        url = f'{base_url}/{distribution}?surveyId={survey}'
        request = r.get(url, headers=headers)
        try:
            response = request.json()
            keys = ['id', 'parentDistributionId', 'ownerId', 'organizationId', 'requestStatus', 'requestType',
                    'sendDate', 'createdDate', 'modifiedDate', 'headers', 'fromEmail', 'replyToEmail', 'fromName',
                    'subject', 'recipients', 'mailingListId', 'contactId', 'sampleId', 'message', 'messageId',
                    'messageText', 'surveyLink', 'surveyId', 'expirationDate', 'linkType', 'stats', 'sent', 'failed',
                    'started', 'bounced', 'opened', 'skipped', 'finished', 'complaints', 'blocked']
            dists = Parser().json_parser(response=response, keys=keys, arr=False)
            dist_df = pd.DataFrame(dists)
            dist_df.index = keys
            library_ids = Parser().json_parser(
                response=response, keys=['libraryId'], arr=False)
            lib = pd.DataFrame(library_ids[0], index=[
                               'mailing_list_library_id', 'message_library_id'])
            dist_df = dist_df.append(lib)
            return dist_df
        except:
            print(
                f"\nServerError: QualtricsAPI Error Code: {response['meta']['error']['errorCode']}\nQualtricsAPI Error Message: {response['meta']['error']['errorMessage']}")

    def create_sms_distribution(self, dist_name, mailing_list, library, survey, message, send_date, parentDistributionId=None, method='Invite'):
        '''This method gives users the ability to create a SMS distribution for a given mailing list and survey. In order to use this method you
        must already have access to pre-defined Messages and their MessageID's existing within a User-Defined (starts with UR)
        or Global (starts with GR) Library. You can list the messages and their MessageID's(starts with MS)  that are available to your user
        account by using the "QualtricsAPI.Library.Messages.list_messages()" method. 

        :param dist_name: The name that shows up for the distribution.
        :type dist_name: str
        :param library: The (Global or User) Library ID which the messages are located within.
        :type library: str
        :param message: The Message ID corresponding with the message that is to be sent.
        :type message: str
        :param mailing_list: The Mailing List ID corresponding with the Mailing List that the distribution is to be sent to.
        :type mailing_list: str
        :param survey: The Survey ID corresponding with the Survey that the distribution is to be sent to.
        :type survey: str
        :param send_date: The date that the distribution is supposed to be sent on. Pass gmtime() for immediate distribution or use the set_send_date() method to format properly.
        :type send_date: str
        :param method: This parameter refers to the type of distribution that is to be sent out to the mailing list.
        :type method: str
        :return: The Distribution ID. (str)
        '''

        assert len(mailing_list) == 18, 'Hey, the parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert len(
            library) == 18, 'Hey, the parameter for "library" that was passed is the wrong length. It should have 18 characters.'
        assert len(
            survey) == 18, 'Hey, the parameter for "survey" that was passed is the wrong length. It should have 18 characters.'
        assert len(
            message) == 18, 'Hey, the parameter for "message" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.'
        assert survey[:3] == 'SV_', 'Hey there! It looks like your SurveyID is incorrect. You can find the SurveyID on the Qualtrics site under your account settings. It will begin with "SV_". Please try again.'
        assert message[:3] == 'MS_', 'Hey there! It looks like your MessageID is incorrect. You can find the MessageID by using the list messages method available in the Messages module of this Package. It will begin with "MS_". Please try again.'
        assert library[:3] == 'UR_' or library[:3] == 'GR_', 'Hey there! It looks like your Library ID is incorrect. You can find the Library ID on the Qualtrics site under your account settings. It will begin with "UR_" or "GR_". Please try again.'

        headers, url = self.header_setup(
            content_type=True, xm=False, path='distributions/sms')
        data = {
            'sendDate': send_date,
            'surveyId': survey,
            'method': method,
            'recipients': {
                'mailingListId': mailing_list
            },
            'name': dist_name,
            'message': {
                'libraryId': library,
                'messageId': message
            }
        }

        if parentDistributionId != None:
            data['parentDistributionId'] = parentDistributionId

        request = r.post(url, json=data, headers=headers)
        response = request.json()
        try:
            distribution_id = response['result']['id']
            return distribution_id
        except:
            print(
                f"\nServerError: QualtricsAPI Error Code: {response['meta']['error']['errorCode']}\nQualtricsAPI Error Message: {response['meta']['error']['errorMessage']}")
        return

    def create_transaction_batch(self, transaction_ids=[]):
        # Create Transaction Batch
        create_tx_batch_headers, create_tx_batch_url = self.header_setup(
            content_type=True, xm=True, path=f'transactionbatches')
        create_tx_batch_payload = {
            "transactionIds": transaction_ids,
            "creationDate": datetime.now().strftime('%Y-%m-%dT%I:%M:%SZ')
        }
        create_tx_batch_request = r.post(
            create_tx_batch_url, json=create_tx_batch_payload, headers=create_tx_batch_headers)
        create_tx_batch_response = create_tx_batch_request.json()
        create_tx_batch_data = self._handle_response(create_tx_batch_response)
        tx_batch_id = create_tx_batch_data['id']
        return tx_batch_id

    def generate_individual_survey_link(self, survey=None, mailing_list=None, contact=None, embedded_data=None, transactional_data=None, expiration=1):
        '''This function takes in a single contact and a survey and returns a unique link for that contact to take that survey

        '''
        if embedded_data == None:
            embedded_data = {}
        if transactional_data == None:
            transactional_data = {}

        assert len(
            survey) == 18, 'Hey, the parameter for "survey" that was passed is the wrong length. It should have 18 characters.'
        assert survey[:3] == 'SV_', 'Hey there! It looks like your SurveyID is incorrect. You can find the SurveyID on the Qualtrics site under your account settings. It will begin with "SV_". Please try again.'
        assert len(mailing_list) == 18, 'Hey, the parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.'
        self._validate_contact_data(contact)
        self._validate_embedded_data(embedded_data)
        self._validate_embedded_data(transactional_data)
        assert isinstance(expiration, int), "Expiration must be an integer."
        assert expiration > 0, "Expiration must be greater than 0."

        # Create contact in mailing list
        create_contact_headers, create_contact_url = self.header_setup(
            content_type=True, xm=True, path=f"mailinglists/{mailing_list}/contacts")
        if embedded_data != None:
            contact['embeddedData'] = embedded_data
        create_contact_request = r.post(
            create_contact_url, json=contact, headers=create_contact_headers)
        create_contact_response = create_contact_request.json()
        cc_result = self._handle_response(create_contact_response)
        contact_id = cc_result['id']
        print("Contact Created in mailing list.", contact_id)
        # Create Transaction
        create_tx_headers, create_tx_url = self.header_setup(
            content_type=True, xm=True, path=f'transactions')
        date_time_now = datetime.now().strftime('%Y-%m-%d %I:%M:%S')
        tx_payload = {
            "single_link_transaction": {
                "contactId": contact_id,
                "mailingListId": mailing_list,
                "transactionDate": date_time_now,
                "data": transactional_data
            }
        }
        create_tx_request = r.post(
            create_tx_url, headers=create_tx_headers, json=tx_payload)
        create_tx_response = create_tx_request.json()
        create_tx_data = self._handle_response(create_tx_response)
        transaction_id = create_tx_data['createdTransactions']['single_link_transaction']['id']
        print("Created Transaction.", transaction_id)
        # Create Transaction Batch
        tx_batch_id = self.create_transaction_batch([transaction_id])
        print("Created Transaction Batch:", tx_batch_id)
        link_elements = self.generate_links_from_tx_batch(
            survey, mailing_list, tx_batch_id, expiration)
        return link_elements[0]['link']

    def generate_links_from_dataframe(self, survey=None, mailing_list=None, df=None, embedded_fields=[], transactional_fields=[], expiration=1):
        '''This method takes in a pandas dataframe and generates links for the contacts in the dataframe.

        :param survey: Survey ID 
        :type survey: str (18 characters long, starts with "SV_")
        :param mailing_list: Mailing list ID
        :type mailing_list: str (18 characters long, starts with "CG_")
        :param df: DataFrame containing contact information with at least 1 row of data. 
                   Must contain at least one of the following columns: 'firstName', 'lastName', 'email', 'extRef', or 'language'.
        :type df: pd.DataFrame
        :param embedded_fields: List of strings where each string is a column name in df that should be embedded.
        :type embedded_fields: list of str
        :param transactional_fields: List of strings where each string is a column name in df that should be included as transactional fields.
        :type transactional_fields: list of str
        :param expiration: Expiration time in days.
        :type expiration: int (must be greater or equal to 1)
        '''

        # Validate inputs
        assert isinstance(survey, str) and len(survey) == 18 and survey.startswith(
            "SV_"), "Survey must be a string of 18 characters starting with 'SV_'"
        assert isinstance(mailing_list, str) and len(mailing_list) == 18 and mailing_list.startswith(
            "CG_"), "Mailing list must be a string of 18 characters starting with 'CG_'"
        assert isinstance(df, pd.DataFrame) and len(
            df) > 0, "df must be a pandas DataFrame with at least 1 row"
        assert {'firstName', 'lastName', 'email', 'extRef', 'language'}.intersection(
            df.columns), "df must contain at least one of the following columns: 'firstName', 'lastName', 'email', 'extRef', or 'language'"
        assert isinstance(embedded_fields, list) and all(isinstance(field, str)
                                                         for field in embedded_fields), "Embedded fields must be a list of strings"
        assert all(
            field in df.columns for field in embedded_fields), f"All embedded fields must match columns in df. Provided: {embedded_fields}"
        assert isinstance(transactional_fields, list) and all(isinstance(field, str)
                                                              for field in transactional_fields), "Transactional fields must be a list of strings"
        assert all(
            field in df.columns for field in transactional_fields), f"All transactional fields must match columns in df. Provided: {transactional_fields}"
        assert isinstance(
            expiration, int) and expiration >= 1, "Expiration must be an integer greater or equal to 1"

        # Create TX Batch (empty)
        tx_batch_id = self.create_transaction_batch([])
        # Loop through the dataframe and accumulate the contacts in a list
        contacts = []
        for idx, row in df.iterrows():
            contact = self._series_to_contact_object(
                row, embedded_fields, transactional_fields)
            # print(contact)
            contacts.append(contact)
        print("number of contacts:", len(contacts))
        contact_import_payload = {
            "transactionMeta": {
                "batchId": tx_batch_id
            },
            "contacts": contacts
        }
        if len(transactional_fields) > 0:
            contact_import_payload['transactionMeta']['fields'] = transactional_fields
        contact_headers, contact_url = self.header_setup(
            content_type=True, accept=True, xm=True, path=f'mailinglists/{mailing_list}/transactioncontacts')
        contact_request = r.post(
            contact_url, headers=contact_headers, json=contact_import_payload)
        contact_response = contact_request.json()
        contact_result = self._handle_response(contact_response)
        tracking_url = contact_result['tracking']['url']
        import_id = contact_result['id']
        # print("Tracking URL:", tracking_url)
        print("import ID:", import_id)
        processing_contacts = True
        last_console_update = ""
        while processing_contacts:
            processing_request = r.get(tracking_url, headers=contact_headers)
            processing_response = processing_request.json()
            processing_result = self._handle_response(processing_response)
            msg = "Processing contacts: "+str(
                processing_result['percentComplete'])+"% complete"
            if last_console_update != msg:
                print(msg)
                last_console_update = msg
            if processing_result['percentComplete'] >= 100:
                print("added", processing_result['contacts']['count']['added'])
                print(
                    "updated", processing_result['contacts']['count']['updated'])
                print(
                    "failed", processing_result['contacts']['count']['failed'])
                processing_contacts = False
            sleep(1.5)
        # Generate links
        links = self.generate_links_from_tx_batch(
            survey=survey, mailing_list=mailing_list, tx_batch_id=tx_batch_id, expiration=expiration)
        links_df = pd.DataFrame(links)
        links_df.set_index('contactId', inplace=True)
        return links_df

    def generate_links_from_tx_batch(self, survey=None, mailing_list=None, tx_batch_id=None, expiration=2):
        '''This method takes in a survey and transaction batch and generates links for all contacts in that batch

        '''
        # Generate Distribution Links for TX batch
        gen_dist_headers, gen_dist_url = self.header_setup(
            content_type=True, xm=False, accept=False, path=f'distributions')
        gen_dist_payload = {
            "surveyId": survey,
            "linkType": "Individual",
            "description": "distribution "+datetime.now().strftime('%Y-%m-%d %I:%M:%S'),
            "action": "CreateTransactionBatchdistribution",
            "transactionBatchId": tx_batch_id,
            "expirationDate": (datetime.now() + relativedelta(months=+expiration)).strftime('%Y-%m-%d %I:%M:%S'),
            "mailingListId": mailing_list
        }
        gen_dist_request = r.post(
            gen_dist_url, json=gen_dist_payload, headers=gen_dist_headers)
        gen_dist_response = gen_dist_request.json()
        gen_dist_data = self._handle_response(gen_dist_response)
        distribution_id = gen_dist_data['id']
        print("Created distribution:", distribution_id)
        # Fetch Distribution links
        fetch_link_headers, fetch_link_url = self.header_setup(
            content_type=True, xm=False, accept=False, path=f'distributions/{distribution_id}/links?surveyId={survey}')
        fetch_link_request = r.get(fetch_link_url, headers=fetch_link_headers)
        fetch_link_response = fetch_link_request.json()
        fetch_link_data = self._handle_response(fetch_link_response)
        # print(fetch_link_data['elements'][0])
        elements = fetch_link_data['elements']
        # print("Links Created.", elements)
        return elements

    ## Private utility methods below here ##

    def _handle_response(self, response: dict):
        try:
            http_status = response['meta']['httpStatus']

            if http_status == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            elif http_status == '503 - Temporary Internal Server Error':
                raise Qualtrics503Error(
                    '503 - Temporary Internal Server Error')
            elif http_status == '504 - Gateway Timeout':
                raise Qualtrics504Error('504 - Gateway Timeout')
            elif http_status == '400 - Bad Request':
                raise Qualtrics400Error(
                    'Qualtrics Error\n(Http Error: 400 - Bad Request): There was something invalid about the request.')
            elif http_status == '401 - Unauthorized':
                raise Qualtrics401Error(
                    'Qualtrics Error\n(Http Error: 401 - Unauthorized): The Qualtrics API user could not be authenticated or does not have authorization to access the requested resource.')
            elif http_status == '403 - Forbidden':
                raise Qualtrics403Error(
                    'Qualtrics Error\n(Http Error: 403 - Forbidden): The Qualtrics API user was authenticated and made a valid request, but is not authorized to access this requested resource.')

        except (Qualtrics503Error, Qualtrics504Error):
            # Recursive call to handle Internal Server Errors can be placed here
            # Example: return self.get_survey_response(response=response)
            pass  # Placeholder for recursive call logic
        except (Qualtrics500Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            # Handle Authorization/Bad Request Errors
            print(e)
        else:
            # Return the successful response result
            if 'result' in response:
                return response['result']
            else:
                return response['meta']

    def _validate_contact_data(self, contact_data):
        # Ensure payload is a dictionary
        assert isinstance(contact_data, dict), "Payload must be a dictionary."

        # Ensure payload is not empty
        assert contact_data, "Payload must have at least one field."

        valid_fields = {"firstName", "lastName",
                        "email", "phone", "extRef", "unsubscribed"}
        for key, value in contact_data.items():
            # Ensure each field is a valid field
            assert key in valid_fields, f"Invalid field '{key}' in payload."

            # Ensure 'unsubscribed' is a boolean if it exists
            if key == "unsubscribed":
                assert isinstance(
                    value, bool) or value is None, "Field 'unsubscribed' must be a boolean."
            else:
                # Ensure all other fields are strings or null
                assert isinstance(
                    value, str) or value is None, f"Field '{key}' must be a string or null."

        # Ensure there is at least one non-null field
        assert any(value is not None for value in contact_data.values()
                   ), "Payload must have at least one non-null field."

        return True

    def _validate_embedded_data(self, embedded_data):
        # Ensure payload is a dictionary
        assert isinstance(embedded_data, dict), "Payload must be a dictionary."

        if embedded_data:
            for key, value in embedded_data.items():
                # Ensure all keys are strings
                assert isinstance(key, str), f"Key '{key}' must be a string."

                # Ensure all values are either strings or numbers
                assert isinstance(
                    value, (str, int, float)), f"Value '{value}' for key '{key}' must be a string or a number."

        return True

    def _series_to_contact_object(self, row, embedded_data_columns, transaction_data_columns):
        # Initialize the contact object with requisite keys.
        contact = {}

        # Root fields for the contact object
        root_fields = ['firstName', 'lastName', 'email', 'extRef', 'language']

        # Update the contact object with values from the row for root fields
        for field in root_fields:
            if field in row:
                contact[field] = row[field]

        # Add 'embeddedData' field
        embedded_data = {}
        for field in embedded_data_columns:
            if field in row:
                if row[field] != '':
                    embedded_data[field] = row[field]
        contact["embeddedData"] = embedded_data

        # Add 'transactionData' field
        transaction_data = {}
        for field in transaction_data_columns:
            if field in row:
                transaction_data[field] = row[field]
        contact["transactionData"] = transaction_data
        contact['unsubscribed'] = False

        return contact
