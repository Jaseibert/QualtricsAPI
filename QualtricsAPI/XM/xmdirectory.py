import time as t
import io
import json
import requests as r
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser

class XMDirectory(Credentials):
    ''' This class contains methods that give users the ability to work with their contact data within the
    XMDirectory.'''

    def __init__(self, token=None, directory_id=None, data_center=None):
        self.token = token
        self.data_center = data_center
        self.directory_id = directory_id

    def create_contact_in_XM(self, first_name=None, last_name=None, email=None, phone=None, language="en", metadata={}):
        '''This function gives you the ability to create a contact in your XM Directory. This method does re-list not each
        element that you just created. It returns the XMDirectory "Contact id" associated with the newly created XM directory
        contact.

        :param first_name: The contacts first name.
        :type first_name: str
        :param last_name: The contacts last name.
        :type last_name: str
        :param email: the contacts email.
        :type email: str
        :param phone: the contacts phone number.
        :type phone: str
        :param language: the native language of the contact. (Default: English)
        :type language: str
        :param metadata: any relevant contact metadata.
        :type metadata: dict
        :return: The newly created contact id (CID) in XMDirectory.
        :type return: str
        '''
        assert isinstance(first_name, (str, type(None))) == True, 'The first_name parameter must be of type None, or a string.'
        assert isinstance(last_name, (str, type(None))) == True, 'The last_name parameter must be of type None, or a string.'
        assert isinstance(email, (str, type(None))) == True, 'The email_name parameter must be of type None, or a string.'
        assert isinstance(phone, (str, type(None))) == True, 'The phone parameter must be of type None, or a string.'
        assert isinstance(language, (str, type(None))) == True, 'The language parameter must be of type None, or a string.'
        assert isinstance(metadata, dict) == True, 'The metadata parameter must be of dict.'

        contact_data = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone,
            "language": language,
            "embeddedData": metadata,
        }
        headers, base_url = self.header_setup(content_type=True, xm=True)
        url = f"{base_url}/contacts"
        request = r.post(url, json=contact_data, headers=headers)
        response = request.json()
        try:
            return response['result']['id']
        except:
            print(f"ServerError:\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")


    def delete_contact(self, contact_id=None):
        '''This method will delete a contact from your XMDirectory. (Caution this cannot be reversed once deleted!)

        :param contact_id: The unique id associated with each contact in the XM Directory.
        :type contact_id: str
        :return:  A string indicating the success or failure of the method call.
        '''
        assert contact_id != None, 'Hey, the contact_id parameter cannot be None. You need to pass in a XM Directory Contact ID as a string into the contact_id parameter.'
        assert isinstance(contact_id, str) == True, 'Hey there, the contact_id parameter must be of type string.'
        assert len(contact_id) == 19, 'Hey, the parameter for "contact_id" that was passed is the wrong length. It should have 19 characters.'
        assert contact_id[:4] == 'CID_', 'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'

        headers, base_url = self.header_setup(xm=True)
        url = f"{base_url}/contacts/{contact_id}"
        request = r.delete(url, headers=headers)
        response = request.json()
        try:
            if response['meta']['httpStatus'] == '200 - OK':
                return f'Your XM Contact"{contact_id}" has been deleted from the XM Directory.'
        except:
            print(f"ServerError:\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")

    def update_contact(self, contact_id=None, **kwargs):
        '''This method will update a contact from your XMDirectory.

        :param contact_id: The unique id associated with each contact in the XM Directory.
        :type contact_id: str
        :return: A string indicating the success or failure of the method call.
        '''
        assert contact_id != None, 'Hey, the contact_id parameter cannot be None. You need to pass in a XM Directory Contact ID as a string into the contact_id parameter.'
        assert isinstance(contact_id, str) == True, 'Hey there, the contact_id parameter must be of type string.'
        assert len(contact_id) == 19, 'Hey, the parameter for "contact_id" that was passed is the wrong length. It should have 19 characters.'
        assert contact_id[:4] == 'CID_', 'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'

        headers, base_url = self.header_setup(xm=True)
        url = f"{base_url}/contacts/{contact_id}"
        contact_data = {}
        for key, value in kwargs.items():
            contact_data.update({key: str(value)})
        request = r.put(url, json=contact_data, headers=headers)
        response = request.json()
        try:
            if response['meta']['httpStatus'] == '200 - OK':
                return f'Your XM Contact"{contact_id}" has been updated in the XM Directory.'
        except:
            print(f"ServerError:\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")

    def list_contacts_in_directory(self):
        '''This method will list the top-level information about the contacts in your XM Directory. As a word of caution,
        this method may take a while to complete depending on the size of your XM Directory. There exists some latency
        with between

        :return: A Pandas DataFrame
        '''

        # Figure out a work around for the 500-error
        i=0
        url=None
        page_size=250
        contact_list = pd.DataFrame()

        def extract_page(url=url, contact_list=contact_list, page_size=page_size):
            ''' This is a method that extracts a single page of contacts in a mailing list.'''

            headers, base_url = self.header_setup(xm=True)
            url = base_url + f"/contacts?pageSize={page_size}" if url == None else url
            request = r.get(url, headers=headers)
            response = request.json()
            if response['meta']['httpStatus'] == '200 - OK':
                keys = ['contactId','firstName', 'lastName', 'email', 'phone','unsubscribed', 'language', 'extRef', 'nextPage']
                contact_lists = Parser().json_parser(response=response, keys=keys, arr=False)
                next_page = contact_lists[-1][0] if len(contact_lists[0]) == page_size else None
                single_contact_list = pd.DataFrame(contact_lists[:-1]).transpose()
                single_contact_list.columns = keys[:-1]
                contact_list = pd.concat([contact_list, single_contact_list]).reset_index(drop=True)
                return contact_list, next_page
            else:
                print(response['meta'])
                contact_list, next_page = extract_page()

        contact_list, next_page = extract_page()
        while next_page != None:
            i+=1
            contact_list, next_page = extract_page(url=next_page, contact_list=contact_list)
            print(i)
            print(len(contact_list))
            if i == 25:
                return contact_list

    def get_contact(self, contact_id=None):
        ''' This method is similar to the 'list_contacts_in_directory' method. Except it will just return a single contact's
        information.

        :param contact_id: The unique id associated with each contact in the XM Directory.
        :type contact_id: str
        :return: A Pandas DataFrame
        '''
        assert contact_id != None, 'Hey, the contact_id parameter cannot be None. You need to pass in a XM Directory Contact ID as a string into the contact_id parameter.'
        assert isinstance(contact_id, str) == True, 'Hey there, the contact_id parameter must be of type string.'
        assert len(contact_id) == 19, 'Hey, the parameter for "contact_id" that was passed is the wrong length. It should have 19 characters.'
        assert contact_id[:4] == 'CID_', 'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'

        headers, base_url = self.header_setup(xm=True)
        url = base_url + f'/contacts/{str(contact_id)}'
        request = r.get(url, headers=headers)
        response = request.json()
        try:
            primary = pd.DataFrame.from_dict(response['result'], orient='index').transpose()
            primary['creationDate'] = pd.to_datetime(primary['creationDate'],unit='ms')
            primary['lastModified'] = pd.to_datetime(primary['lastModified'],unit='ms')
            return primary
        except:
            print(f"ServerError:\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")

    def get_contact_additional_info(self, contact_id=None, content=None):
        ''' This method will return the additional "nested" information associated with a contact in the XMDirectory.
        To get these different nested pieces of infomation you can pass one of three arguements to the 'content' parameter. If you
        pass 'mailinglistmembership', you will return the different Mailing Lists that the contact is associated with in the form of a
        pandas DataFrame. If you pass 'stats', you will return the response statistics associated with the contact, again in the form
        of a Pandas DataFrame. Finally, if you pass the 'embeddedData' argument, you will return any emmbedded data associated with
        the given contact, and as you guessed it, in the form of a Pandas DataFrame.

        :param contact_id: The unique id associated with each contact in the XM Directory.
        :type contact_id: str
        :param content: A string representing either 'mailingListMembership', 'stats', 'embeddedData'
        :type content: str
        :return: A Pandas DataFrame
        '''
        assert contact_id != None, 'Hey, the contact_id parameter cannot be None. You need to pass in a XM Directory Contact ID as a string into the contact_id parameter.'
        assert isinstance(contact_id, str) == True, 'Hey there, the contact_id parameter must be of type string.'
        assert len(contact_id) == 19, 'Hey, the parameter for "contact_id" that was passed is the wrong length. It should have 19 characters.'
        assert contact_id[:4] == 'CID_', 'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'
        assert content != None, 'Hey there, you need to pass an argument ("embeddedData", or "mailingListMembership") to the "content" parameter.'

        try:
            primary = self.get_contact(contact_id=contact_id)
            keys = Parser().extract_keys(primary[content][0])
            data = pd.DataFrame.from_dict(primary[content][0], orient='index').transpose()
            return data
        except:
            print('Hey there! Something went wrong please try again.')
