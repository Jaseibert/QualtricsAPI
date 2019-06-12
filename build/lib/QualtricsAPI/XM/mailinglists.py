import time as t
import io
import json
import requests as r
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Exceptions import MailingListIDError

class MailingList(Credentials):
    ''' This class contains methods that give users the ability to work with their users Mailing list's and
    their users Mailing Lists contact data within the XMDirectory.'''

    def __init__(self, token=None, directory_id=None, data_center=None):
        self.token = token
        self.data_center = data_center
        self.directory_id = directory_id
        return

    def create_list(self, name=None):
        '''This method will create a mailing list in the XM Directory for the your specified user's account.

        :param list_name: the name of the list to be created.
        :return: set containing the list_name and the list's new id
        '''

        try:
            headers, url = self.header_setup(content_type=True)
            url = url + "/mailinglists"
            data = {"name": "{0}".format(name)}
            request = r.post(url, json=data, headers=headers)
            response = request.json()
            list_id = Parser().json_parser(response=response, keys=['id'], arr=False)[0][0]
            list_params = tuple([name, list_id])
        except ServerError:
            print(f"ServerError:\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}", s.msg)
        return list_params

    def list_lists(self, page_size=100, offset=0, to_df=True):
        '''This method lists all the mailing lists in the directory for the specified user token. Use the page_size and offset
        parameters to dictate the size and position of the list that is returned. Page_size is defaulted at 100, and offset is
        defaulted to start at the beginning (i.e. offset=0).

        :param page_size: The number of mailing lists to return per call.
        :type page_size: int
        :param offset: The index offset that you would like to apply in you call.
        :type offset: int
        :param to_df: if True, returns the mailing lists and their member objects in a pandas DataFrame.
        :return: Either a pandas DataFrame or a list of tuples, containing lists and their respective member objects.
        '''

        headers, base_url = self.header_setup()
        url = base_url + f"/mailinglists?pageSize={page_size}&offset={offset}"
        request = r.get(url, headers=headers)
        response = request.json()
        keys = ['mailingListId', 'name', 'ownerId', 'lastModifiedDate', 'creationDate','contactCount']
        mailing_lists = Parser().json_parser(response=response, keys=keys, arr=False)
        if to_df is True:
            mailing_list = pd.DataFrame(mailing_lists).transpose()
            mailing_list.columns = keys
            mailing_list['creationDate'] = pd.to_datetime(mailing_list['creationDate'], unit='ms')
            mailing_list['lastModifiedDate'] = pd.to_datetime(mailing_list['lastModifiedDate'], unit='ms')
            return mailing_list
        return mailing_lists

    def get_list(self, mailing_list=None):
        '''This function gets the list specfied by the mailing list param and returns the list members.

        :param mailing_list: Your mailing list id that you are interested in getting information on.
        :type mailing_list: str
        :return: a dictionary containing the mailing list member objects.
        '''

        assert len(mailing_list) == 18, 'Hey, the parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.'

        try:
            headers, base_url = self.header_setup()
            url = base_url + f"/mailinglists/{mailing_list}"
            request = r.get(url, headers=headers)
            response = request.json()
            list_info = {
                        "mailingListId": response['result']['mailingListId'],
                        "name": response['result']['name'],
                        "ownerId": response['result']['ownerId'],
                        "lastModifiedDate": response['result']['lastModifiedDate'],
                        "creationDate": response['result']['creationDate'],
                        "contactCount": response['result']['contactCount']
            }
            df = pd.DataFrame.from_dict(list_info, orient='index').transpose()
            df['creationDate'] = pd.to_datetime(df['creationDate'], unit='ms')
            df['lastModifiedDate'] = pd.to_datetime(df['lastModifiedDate'], unit='ms')
        except MailingListIDError:
            print('Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.')
        return df

    def rename_list(self, mailing_list=None, name=None):
        '''This method takes an existing mailing list name and updates it to reflect the name defined in the name method.

        :param mailing_list: Your mailing list id that you are interested in renaming.
        :type mailing_list: str
        :param name: The new name for the mailing list.
        :type name: str
        :return: A string confirming that you successfully renamed the list.
        '''

        assert len(mailing_list) == 18, 'Hey there! The parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. Please try again.'

        try:
            data = {"name": f"{name}"}
            headers, base_url = self.header_setup(content_type=True)
            url = base_url + f"/mailinglists/{mailing_list}"
            request = r.put(url, json=data, headers=headers)
            response = request.json()
            if response['meta']['httpStatus'] == '200 - OK':
                print(f'Your mailing list "{mailing_list}" has been renamed to {name} in the XM Directory.')
        except MailingListIDError:
            print('Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.')
        return

    def delete_list(self,mailing_list=None):
        '''This method will delete the specified mailing list from the given users XM Directory.

        :param mailing_list: Your mailing list id that you are interested in deleting.
        :type mailing_list: str
        :return: A string confirming that you successfully deleted the list.
        '''
        assert len(mailing_list) == 18, 'Hey there! The parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. Please try again.'

        try:
            data = {"name": f"{mailing_list}"}
            headers, base_url = self.header_setup()
            url = base_url + f"/mailinglists/{mailing_list}"
            request = r.delete(url, json=data, headers=headers)
            response = request.json()
            if content['meta']['httpStatus'] == '200 - OK':
                print(f'Your mailing list "{mailing_list}" has been deleted from the XM Directory.')
        except MailingListIDError:
            print('Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.')
        return

    def list_contacts(self, mailing_list=None, page_size=100, offset=0, to_df=True):
        '''This method creates a pandas DataFrame of all the contacts information within the defined mailing list.

        :param mailing_list: the mailing list id
        :type mailing_list: str
        :param page_size: The number of contacts in the mailing list to return per call.
        :type page_size: int
        :param offset: The index offset that you would like to apply in you call.
        :type offset: int
        :param to_df: if True, returns the contacts in the mailing list and their member objects in a pandas DataFrame.
        :return: a pandas DataFrame, or a dictionary containing the contacts information.
        '''
        assert len(mailing_list) == 18, 'Hey, the parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. Please try again.'

        try:
            headers, base_url = self.header_setup()
            url = base_url + f"/mailinglists/{mailing_list}/contacts?pageSize={page_size}&offset={offset}"
            request = r.get(url, headers=headers)
            response = request.json()
            keys = ['contactId','firstName', 'lastName', 'email', 'phone', 'extRef', 'language', 'unsubscribed']
            contact_list = Parser().json_parser(response=response, keys=keys, arr=False)
            if to_df is True:
                contact_list = pd.DataFrame(contact_list).transpose()
                contact_list.columns = keys
                contact_list['mailing_list'] = mailing_list

            #contact_list = []
            #while lists['result']['nextPage'] is not None:
                #contact_list = Parser().json_parser(lists, keys=keys arr=False)
                #contact_df = pd.DataFrame(contact_list).transpose()
                #contact_df.columns = keys
                #contact_df['mailing_list'] = mailing_list
                #contact_lists.append(contact_df)
                #url = lists['result']['nextPage']
                #response = r.get(url, headers=headers)
                #lists = response.json()
            #contact_df = pd.concat(contact_lists).reset_index(drop=True)

        except MailingListIDError:
            print('Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.')
        return contact_list

    def create_contact_in_list(self, mailing_list=None, first_name=None, last_name=None, email=None, phone=None, external_ref=None, unsubscribed=False,language="en",metadata={}):
        '''This method creates contacts in the specified mailing list. It is important to remember here that whenever you create a contact in
        a mailing list, you are also creating that contact in the XMDirectory. Once created 2 seperate IDs are created for the contact. The ContactID
        is the reference for the contact in the XMDirectory, and the Contact Lookup ID is the reference of the contact in the Mailing List.

        :param mailing_list: The mailing list id for the list that you want to add the contact too.
        :type mailing_list: str
        :param first_name: The new contact's first name.
        :type first_name: str
        :param last_name: The new contact's last name.
        :type last_name: str
        :param email: The new contact's email.
        :type email: str
        :param phone: The new contact's phone number.
        :tyoe phone: str
        :param external_ref: The new contact's external reference.
        :type external_ref: str
        :param unsubscribed: This parameter denotes whether the new contact is unsubscribed from surveys (Default: False).
        :type unsbscribed: str
        :param language: The language prefered by the new contact (Default: English)
        :type language: str
        :param metadata: Any relevant contact metadata.
        :type metadata: dict
        :return: the contact id (contact_id) in XMDirectory, and the contact id (contact_list_id) in the mailing list.
        '''
        assert len(mailing_list) == 18, 'Hey there! The parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. Please try again.'

        try:
            data = {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "phone": phone,
                "embeddedData": metadata,
                "language": language,
                "extRef": external_ref,
                "unsubscribed": unsubscribed
            }

            headers, base_url = self.header_setup(content_type=True)
            url = base_url + f"/mailinglists/{mailing_list}/contacts"
            request = r.post(url, json=data, headers=headers)
            response = request.json()
            contact_id = response['result']['id']
            contact_list_id = response['result']['contactLookupId']
        except MailingListIDError:
            print('Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.')
        return contact_id, contact_list_id
