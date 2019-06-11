import time as t
import io
import json
import requests as r
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Exceptions import ContactIDError

class XMDirectory(Credentials):

    def __init__(self, token=None, directory_id=None, data_center=None):
        self.token = token
        self.data_center = data_center
        self.directory_id = directory_id

    def create_contact_in_XM(self, first_name=None, last_name=None, email=None, phone=None, language="en", metadata={}):
        '''This function creates a contact in the XM Directory.

        :param first_name: the contacts first name.
        :param last_name: the contacts last name.
        :param email: the contacts email.
        :param phone: the contacts phone number.
        :param language: the native language of the contact. (Default: English)
        :param metadata: any relevant contact metadata.
        :type metadata: dict
        :return: the contact id (contact_id) in XMDirectory.
        '''
        try:
            contact_data = {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "phone": phone,
                "language": language,
                "embeddedData": metadata,
            }
            headers, base_url = self.header_setup(content_type=True)
            url = base_url + "/contacts"
            request = r.post(url, json=contact_data, headers=headers)
            response = request.json()
            contact_id = response['result']['id']
        except ServerError:
            print(f"ServerError:\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}", s.msg)
        return contact_id

    def delete_contact(self, contact_id=None):
        '''This function will delete a user from XMDirectory.

        :param contact_id: The unique id associated with each contact in the XM Directory.
        :return: nothing, but prints if successful, and if there was an error.
        '''
        assert len(contact_id) == 19, 'Hey, the parameter for "contact_id" that was passed is the wrong length. It should have 19 characters.'
        assert contact_id[:4] == 'CID_', 'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'

        try:
            headers, base_url = self.header_setup()
            url = base_url + f"/contacts/{contact_id}"
            request = r.delete(url, headers=headers)
            response = request.json()
            if content['meta']['httpStatus'] == '200 - OK':
                print(f'Your XM Contact"{contact_id}" has been deleted from the XM Directory.')
        except ContactIDError:
            'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'
        return

    def list_contacts_in_directory(self, page_size=100, offset=0, to_df=True):
        '''This function lists the contacts in the XM Directory.

        :param page_size: determines the start number within the directory for the call.
        :return:
        '''
        try:
            headers, base_url = self.header_setup()
            url = base_url + f"/contacts?pageSize={page_size}&offset={offset}"
            request = r.get(url, headers=headers)
            response = request.json()
            #extract_keys
            contact_list = Parser().json_parser(response=response,keys=['contactId','firstName', 'lastName', 'email', 'phone', 'unsubscribed', 'language', 'extRef'])
            col_names = ['contact_id','first_name','last_name','email','phone','unsubscribed','language','external_ref']
            if to_df is True:
                contact_list = pd.DataFrame(contact_list, columns=col_names)
                return contact_list
        except ServerError:
            print(f"ServerError:\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}", s.msg)
        return contact_list

    def get_contact(self, contact_id=None):
        ''' This method returns the primary information associated with a single contact.

        :param contact_id: a given Contact's ID
        :return: a DataFrame
        '''
        assert len(contact_id) == 19, 'Hey, the parameter for "contact_id" that was passed is the wrong length. It should have 19 characters.'
        assert contact_id[:4] == 'CID_', 'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'

        try:
            headers, base_url = self.header_setup()
            url = base_url + f'/contacts/{str(contact_id)}'
            request = r.get(url, headers=headers)
            response = request.json()
            primary = pd.DataFrame.from_dict(response['result'], orient='index').transpose()
            primary['creationDate'] = pd.to_datetime(primary['creationDate'],unit='ms')
            primary['lastModified'] = pd.to_datetime(primary['lastModified'],unit='ms')
        except ContactIDError:
            'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'
        return primary

    def get_contact_additional_info(self, contact_id=None, content=None):
        ''' This method returns the additional information associated with a contact (mailinglistmembership, stats, and embeddedData)

        :param contact_id: a given Contact's ID
        :param content: a string representing either 'mailingListMembership', 'stats', 'embeddedData'
        :return: a DataFrame
        '''

        assert len(contact_id) == 19, 'Hey, the parameter for "contact_id" that was passed is the wrong length. It should have 19 characters.'
        assert contact_id[:4] == 'CID_', 'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'
        assert content is not None, 'Hey there, you need to pass an argument ("embeddedData", or "mailingListMembership") to the "content" parameter.'

        try:
            primary = self.get_contact(contact_id=contact_id)
            keys = Parser().extract_keys(primary[content][0])
            data = pd.DataFrame.from_dict(primary[content][0], orient='index').transpose()
        except ContactIDError:
            'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'
        return data
