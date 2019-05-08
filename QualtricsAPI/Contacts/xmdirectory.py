import time as t
import io
import json
import requests as r
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser

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
        response = r.post(url, json=contact_data, headers=headers)
        content = response.json()
        contact_id = content['result']['id']
        return contact_id

    def delete_contact(self,contact_id=None):
        '''This function will delete a user from IQDirectory.

        :param contact_id: The unique id associated with each contact in the XM Directory.
        :return: nothing, but prints if successful, and if there was an error.
        '''
        headers, base_url = self.header_setup()
        url = base_url + f"/contacts/{contact_id}"
        response = r.delete(url, headers=headers)
        content = response.json()
        if content['meta']['httpStatus'] == '200 - OK':
            print(f'Your XM Contact"{contact_id}" has been deleted from the XM Directory.')
        else:
            raise ValueError(f"ServerError:{content['meta']['error']['errorCode']}, {content['meta']['error']['errorMessage']}")
        return

    def list_contacts_in_directory(self, page_size=100, offset=0, to_df=True):
        '''This function lists the contacts in the XM Directory.

        :param page_size: determines the start number within the directory for the call.
        :return:
        '''
        headers, base_url = self.header_setup()
        url = base_url + f"/contacts?pageSize={page_size}&offset={offset}"
        response = r.get(url, headers=headers)
        contacts = response.json()
        contact_list = Parser().json_parser(response=contacts,keys=['contactId','firstName', 'lastName', 'email', 'phone', 'unsubscribed', 'language', 'extRef'])
        col_names = ['contact_id','first_name','last_name','email','phone','unsubscribed','language','external_ref']
        if to_df is True:
            contact_list = pd.DataFrame(contact_list, columns=col_names)
            return contact_list
        else:
            return contact_list

    def get_contact(self, contact_id=None):
        ''' This method returns the primary information associated with a single contact.

        :param contact_id: a given Contact's ID
        :return: a DataFrame
        '''
        headers, base_url = self.header_setup()
        url = base_url + f'/contacts/{str(contact_id)}'
        response = r.get(url, headers=headers)
        contact = response.json()
        primary = pd.DataFrame.from_dict(contact['result'], orient='index').transpose()
        primary['creationDate'] = pd.to_datetime(primary['creationDate'],unit='ms')
        primary['lastModified'] = pd.to_datetime(primary['lastModified'],unit='ms')
        return primary

    def get_contact_additional_info(self, contact_id=None, content=None):
        ''' This method returns the additional information associated with a contact (mailinglistmembership, stats, and embeddedData)

        :param contact_id: a given Contact's ID
        :param content: a string representing either 'mailingListMembership', 'stats', 'embeddedData'
        :return: a DataFrame
        '''
        primary = self.get_contact(contact_id=contact_id)
        keys = Parser().extract_keys(primary[content][0])
        data = pd.DataFrame.from_dict(primary[content][0], orient='index').transpose()
        return data
