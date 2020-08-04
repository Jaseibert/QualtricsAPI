import time as t
import io
import json
import requests as r
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Exceptions import Qualtrics500Error, Qualtrics503Error, Qualtrics504Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error

class XMDirectory(Credentials):
    ''' This class contains methods that give users the ability to work with their contact data within the
    XMDirectory.'''

    def __init__(self, token=None, directory_id=None, data_center=None):
        self.token = token
        self.data_center = data_center
        self.directory_id = directory_id

    def create_contact_in_XM(self, dynamic_payload={}, **kwargs):
        '''This function gives you the ability to create a contact in your XM Directory. This method does re-list not each
        element that you just created. It returns the XMDirectory "Contact ID" associated with the newly created XM directory
        contact.
        
        :param dynamic_payload: A dictionary containing the correct key-value pairs.
        :type dynamic_payload: dict
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
        
        if len(dynamic_payload) == 0:
            for key in list(kwargs.keys()):
                assert key in ['first_name', 'last_name', 'email', 'unsubscribed', 'language', 'external_ref', 'metadata', 'phone'], "Hey there! You can only pass in parameters with names in the list, ['first_name', 'last_name', 'email', 'unsubscribed', 'language', 'external_ref', 'metadata']"
                if key == 'first_name':
                    dynamic_payload.update({'firstName': kwargs[str(key)]})
                elif key == 'last_name':
                    dynamic_payload.update({'lastName': kwargs[str(key)]})
                elif key == 'email':
                    dynamic_payload.update({'email': kwargs[str(key)]})
                elif key == 'phone':
                    dynamic_payload.update({'phone': kwargs[str(key)]})
                elif key == 'language':
                    dynamic_payload.update({'language': kwargs[str(key)]})
                elif key == 'external_ref':
                    dynamic_payload.update({'extRef': kwargs[str(key)]})
                elif key == 'unsubscribed':
                    dynamic_payload.update({'unsubscribed': kwargs[str(key)]})
                elif key == 'phone':
                    dynamic_payload.update({'phone': kwargs[str(key)]})
                elif key == 'metadata':
                    assert isinstance(kwargs['metadata'], dict), 'Hey there, your metadata parameter needs to be of type "dict"!'
                    dynamic_payload.update({'embeddedData': kwargs[str(key)]})

        headers, base_url = self.header_setup(content_type=True, xm=True)
        url = f"{base_url}/contacts"
        request = r.post(url, json=dynamic_payload, headers=headers)
        try:
            response = request.json()
            if response['meta']['httpStatus'] == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            elif response['meta']['httpStatus'] == '503 - Temporary Internal Server Error':
                raise Qualtrics503Error('503 - Temporary Internal Server Error')
            elif response['meta']['httpStatus'] == '504 - Gateway Timeout':
                raise Qualtrics504Error('504 - Gateway Timeout')
            elif response['meta']['httpStatus'] == '400 - Bad Request':
                raise Qualtrics400Error('Qualtrics Error\n(Http Error: 400 - Bad Request): There was something invalid about the request.')
            elif response['meta']['httpStatus'] == '401 - Unauthorized':
                raise Qualtrics401Error('Qualtrics Error\n(Http Error: 401 - Unauthorized): The Qualtrics API user could not be authenticated or does not have authorization to access the requested resource.')
            elif response['meta']['httpStatus'] == '403 - Forbidden':
                raise Qualtrics403Error('Qualtrics Error\n(Http Error: 403 - Forbidden): The Qualtrics API user was authenticated and made a valid request, but is not authorized to access this requested resource.')
        except (Qualtrics500Error, Qualtrics503Error, Qualtrics504Error) as e:
            # Recursive call to handle Internal Server Errors
            return create_contact_in_XM(dynamic_payload=dynamic_payload)
        except (Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            # Handle Authorization/Bad Request Errors
            return print(e)
        else:
            return response['result']['id']

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

    def update_contact(self, contact_id=None, dynamic_payload={}, **kwargs):
        '''This method will update a contact from your XMDirectory.

        :param contact_id: The unique id associated with each contact in the XM Directory.
        :type contact_id: str
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
        :return: A string indicating the success or failure of the method call.
        '''
        assert contact_id != None, 'Hey, the contact_id parameter cannot be None. You need to pass in a XM Directory Contact ID as a string into the contact_id parameter.'
        assert isinstance(contact_id, str) == True, 'Hey there, the contact_id parameter must be of type string.'
        assert len(contact_id) == 19, 'Hey, the parameter for "contact_id" that was passed is the wrong length. It should have 19 characters.'
        assert contact_id[:4] == 'CID_', 'Hey there! It looks like the Contact ID that was entered is incorrect. It should begin with "CID_". Please try again.'

        if len(dynamic_payload) == 0:
            for key in list(kwargs.keys()):
                assert key in ['first_name', 'last_name', 'email', 'unsubscribed', 'language', 'external_ref', 'metadata', 'phone'], "Hey there! You can only pass in parameters with names in the list, ['first_name', 'last_name', 'email', 'unsubscribed', 'language', 'external_ref', 'metadata']"
                if key == 'first_name':
                    dynamic_payload.update({'firstName': kwargs[str(key)]})
                elif key == 'last_name':
                    dynamic_payload.update({'lastName': kwargs[str(key)]})
                elif key == 'email':
                    dynamic_payload.update({'email': kwargs[str(key)]})
                elif key == 'phone':
                    dynamic_payload.update({'phone': kwargs[str(key)]})
                elif key == 'language':
                    dynamic_payload.update({'language': kwargs[str(key)]})
                elif key == 'external_ref':
                    dynamic_payload.update({'extRef': kwargs[str(key)]})
                elif key == 'unsubscribed':
                    dynamic_payload.update({'unsubscribed': kwargs[str(key)]})
                elif key == 'phone':
                    dynamic_payload.update({'phone': kwargs[str(key)]})
                elif key == 'metadata':
                    assert isinstance(kwargs['metadata'], dict), 'Hey there, your metadata parameter needs to be of type "dict"!'
                    dynamic_payload.update({'embeddedData': kwargs[str(key)]})
        
        headers, base_url = self.header_setup(xm=True)
        url = f"{base_url}/contacts/{contact_id}"
        request = r.put(url, json=dynamic_payload, headers=headers)
        try:
            response = request.json()
            if response['meta']['httpStatus'] == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            elif response['meta']['httpStatus'] == '503 - Temporary Internal Server Error':
                raise Qualtrics503Error('503 - Temporary Internal Server Error')
            elif response['meta']['httpStatus'] == '504 - Gateway Timeout':
                raise Qualtrics504Error('504 - Gateway Timeout')
            elif response['meta']['httpStatus'] == '400 - Bad Request':
                raise Qualtrics400Error('Qualtrics Error\n(Http Error: 400 - Bad Request): There was something invalid about the request.')
            elif response['meta']['httpStatus'] == '401 - Unauthorized':
                raise Qualtrics401Error('Qualtrics Error\n(Http Error: 401 - Unauthorized): The Qualtrics API user could not be authenticated or does not have authorization to access the requested resource.')
            elif response['meta']['httpStatus'] == '403 - Forbidden':
                raise Qualtrics403Error('Qualtrics Error\n(Http Error: 403 - Forbidden): The Qualtrics API user was authenticated and made a valid request, but is not authorized to access this requested resource.')
        except (Qualtrics500Error, Qualtrics503Error, Qualtrics504Error) as e:
            return update_contact(contact_id=contact_id, dynamic_payload=dynamic_payload)
        except (Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            return print(e)
        else:
            return f'The contact ({contact_id}) was updated in the XM Directory.'

    def list_contacts_in_directory(self):
        '''This method will list the top-level information about the contacts in your XM Directory. As a word of caution,
        this method may take a while to complete depending on the size of your XM Directory. There exists some latency
        with between

        :return: A Pandas DataFrame
        '''

        page_size=1000
        master = pd.DataFrame(columns=['contactId','firstName', 'lastName', 'email', 'phone','unsubscribed', 'language', 'extRef'])
        headers, base_url = self.header_setup(xm=True)
        url = base_url + f"/contacts?pageSize={page_size}&useNewPaginationScheme=true"

        def extract_page(url=url, master=master, page_size=page_size):
            ''' This is a method that extracts a single page of contacts in a mailing list.'''
            request = r.get(url, headers=headers)
            try:
                response = request.json()
                if response['meta']['httpStatus'] == '500 - Internal Server Error':
                    raise Qualtrics500Error('500 - Internal Server Error')
                elif response['meta']['httpStatus'] == '503 - Temporary Internal Server Error':
                    raise Qualtrics503Error('503 - Temporary Internal Server Error')
                elif response['meta']['httpStatus'] == '504 - Gateway Timeout':
                    raise Qualtrics504Error('504 - Gateway Timeout')
            except (Qualtrics500Error, Qualtrics503Error):
                t.sleep(0.25)
                extract_page(url=url, master=master)
            except Qualtrics504Error:
                t.sleep(5)
                extract_page(url=url, master=master)
            else:
                keys = ['contactId','firstName', 'lastName', 'email', 'phone','unsubscribed', 'language', 'extRef']
                contact_lists = Parser().json_parser(response=response, keys=keys, arr=False)
                next_page = response['result']['nextPage']
                single_contact_list = pd.DataFrame(contact_lists).transpose()
                single_contact_list.columns = keys
                master = pd.concat([master, single_contact_list]).reset_index(drop=True)
                return master, next_page

        master, next_page = extract_page()
        if next_page == None:
            return master
        else:
          while next_page != None:
              master, next_page = extract_page(url=next_page, master=master)
          return master

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
