import time as t
import io
import json
import requests as r
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Exceptions import ContactIDError, ServerError

class XMDirectory(Credentials):
    ''' This class contains methods that give users the ability to work with their contact data within the
    XMDirectory.'''

    def __init__(self, token=None, directory_id=None, data_center=None):
        self.token = token
        self.data_center = data_center
        self.directory_id = directory_id

    def create_contact_in_XM(self, first_name=None, last_name=None, email=None, phone=None, language="en", metadata={}):
        '''This function gives you the ability to create a contact in your XM Directory. This method does not every item
        in that you just created, but it does return the XMDirectory contact id associated with the newly created contact.

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
        '''This method will delete a contact from your XMDirectory. (Caution this cannot be reversed once deleted!)

        :param contact_id: The unique id associated with each contact in the XM Directory.
        :type contact_id: str
        :return: Nothing, but prints if successful, and if there was an error.

        '''
        assert len(contact_id) == 19, 'Hey, the parameter for "contact_id" that was passed is the wrong length. It should have 19 characters.'
        assert contact_id[:4] == 'CID_', 'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'

        try:
            headers, base_url = self.header_setup()
            url = base_url + f"/contacts/{contact_id}"
            request = r.delete(url, headers=headers)
            response = request.json()
            if response['meta']['httpStatus'] == '200 - OK':
                print(f'Your XM Contact"{contact_id}" has been deleted from the XM Directory.')
        except ContactIDError:
            'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'
        return

    def update_contact(self, contact_id=None, **kwargs):
        '''This method will update a contact from your XMDirectory.

        :param contact_id: The unique id associated with each contact in the XM Directory.
        :type contact_id: str
        :return: Nothing
        '''
        assert len(contact_id) == 19, 'Hey, the parameter for "contact_id" that was passed is the wrong length. It should have 19 characters.'
        assert contact_id[:4] == 'CID_', 'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'

        try:
            headers, base_url = self.header_setup()
            url = base_url + f"/contacts/{contact_id}"
            contact_data = {}
            for key, value in kwargs.items():
                contact_data.update({key: str(value)})
            request = r.put(url, json=contact_data, headers=headers)
            response = request.json()
        except ContactIDError:
            'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'
        return

    def list_contacts_in_directory(self, page_size=1000, offset=0, url=None):
        '''This method will list the top-level information about the contacts in your XM Directory. Depending
        on the argument that you pass to the parameter 'to_df', the method will either return a Pandas DataFrame
        or a dictionary containing the contact data. Use the parameters 'page_size' and 'offset' to dictate the
        size and position of the slice that you are requesting from the XMDirectory. As an additional point, when
        itteratively calling this function you may experience some latency, so as a courtesy to Qualtrics and their
        Dev team I recommend calling time.sleep(3) between each request.

        :param page_size: This parameter sets chunk size of the number of contacts requested.
        :type page_size: int
        :param offset: This parameter specifies the where start index value of the call. (i.e offset = 300 means start the request at the 300th contact in the directory.)
        :type offset: int
        :param to_df: If True, the contacts will be returned in a Pandas DataFrame. If False, a Dictionary is returned.
        :type to_df: Boolean
        :return: A Pandas DataFrame, or Dictionary containing the top-level information regarding a contact in the XMDirectory.
        :type return: DataFrame, Dict
        '''
        try:
            contact_list = pd.DataFrame()
            def extract_page(url=url, contact_list=contact_list, offset=offset, page_size=page_size):
                ''' This is a method that extracts a single page of contacts in a mailing list.'''
                headers, base_url = self.header_setup()
                url = base_url + f"/contacts?pageSize={page_size}" if url == None else url
                request = r.get(url, headers=headers)
                response = request.json()
                keys = ['contactId','firstName', 'lastName', 'email', 'phone','unsubscribed', 'language', 'extRef', 'nextPage']
                contact_lists = Parser().json_parser(response=response, keys=keys, arr=False)
                next_page = contact_lists[-1][0] if len(contact_lists[0]) == page_size else None
                single_contact_list = pd.DataFrame(contact_lists[:-1]).transpose()
                single_contact_list.columns = keys[:-1]
                contact_list = pd.concat([contact_list, single_contact_list]).reset_index(drop=True)
                return contact_list, next_page
            contact_list, next_page = extract_page()
            while next_page != None:
                contact_list, next_page = extract_page(url=next_page, contact_list=contact_list)
        except ServerError:
            print(f"ServerError:\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}", s.msg)
        return response

    def get_contact(self, contact_id=None):
        ''' This method is similar to the 'list_contacts_in_directory' method, in that it will return a single contact's
        information.

        :param contact_id: The unique id associated with each contact in the XM Directory.
        :type contact_id: str
        :return: A Pandas DataFrame containing the contact's informaion
        :type return: DataFrame
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
        :type return: DataFrame
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
