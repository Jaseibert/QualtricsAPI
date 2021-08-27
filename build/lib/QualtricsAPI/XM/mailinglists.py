import time as t
import requests as r
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Exceptions import Qualtrics500Error

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
        :return: tuple containing the Mailing List's and the Mailing List's new id.
        '''
        assert name != None, 'Hey there! The name parameter cannot be None. You need to pass in a new Mailing List name as a string into the name parameter.'
        assert isinstance(name, str) == True, 'Hey there! The name parameter must be of type string.'

        headers, base_url = self.header_setup(content_type=True, xm=True)
        url = f"{base_url}/mailinglists"
        data = {"name": "{0}".format(name)}
        request = r.post(url, json=data, headers=headers)
        response = request.json()
        try:
            list_id = Parser().json_parser(response=response, keys=['id'], arr=False)[0][0]
            return name, list_id
        except:
            print(f"ServerError: {response['meta']['httpStatus']}\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")

    def list_lists(self, page_size=100):
        '''This method lists all the mailing lists in the directory for the specified user token. You won't typically need to adjust
        the pre-defined parameters.

        :param page_size: The number of mailing lists to return per call.
        :type page_size: int
        :return: A Pandas DataFrame
        '''
        assert page_size != 0, 'Hey there! You need to have a page size greater than 1'

        mailing_lists = pd.DataFrame()
        headers, base_url = self.header_setup(xm=True)
        url = base_url + f"/mailinglists/?pageSize={page_size}"
        try:
          def get_page(mailing_lists=mailing_lists, url=url):
            ''' This method is a nested method that extracts a single page of mailing lists. '''
            request = r.get(url, headers=headers)
            response = request.json()
            keys = ['mailingListId', 'name', 'ownerId', 'lastModifiedDate', 'creationDate','contactCount', 'nextPage']
            lists = Parser().json_parser(response=response, keys=keys, arr=False)
            single_page = pd.DataFrame(lists).transpose()
            single_page.columns = keys
            single_page['creationDate'] = pd.to_datetime(single_page['creationDate'], unit='ms')
            single_page['lastModifiedDate'] = pd.to_datetime(single_page['lastModifiedDate'], unit='ms')
            mailing_lists = pd.concat([mailing_lists, single_page]).reset_index(drop=True)
            next_page = str(response['result']['nextPage'])
            return mailing_lists, next_page, response
          mailing_lists, next_page, response = get_page(mailing_lists=mailing_lists, url=url)
          while next_page != 'None':
            mailing_lists, next_page, response = get_page(mailing_lists=mailing_lists, url=next_page)
          return mailing_lists
        except:
          print(f"ServerError: {response['meta']['httpStatus']}\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")

    def get_list(self, mailing_list=None):
        '''This function gets the list specfied by the mailing list param and returns the list members.

        :param mailing_list: Your mailing list id that you are interested in getting information on.
        :type mailing_list: str
        :return: A Pandas DataFrame
        '''
        assert mailing_list != None, 'Hey there! The mailing_list parameter cannot be None. You need to pass in a Mailing List ID as a string into the mailing_list parameter.'
        assert isinstance(mailing_list, str) == True, 'Hey there! The mailing_list parameter must be of type string.'
        assert len(mailing_list) == 18, 'Hey, the parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.'

        headers, base_url = self.header_setup(xm=True)
        url = f"{base_url}/mailinglists/{mailing_list}"
        request = r.get(url, headers=headers)
        response = request.json()
        try:
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
            return df
        except:
            print(f"ServerError: {response['meta']['httpStatus']}\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")

    def rename_list(self, mailing_list=None, name=None):
        '''This method takes an existing mailing list name and updates it to reflect the name defined in the name parameter.

        :param mailing_list: the mailing list that you want to rename.
        :type mailing_list: str
        :param name: The new name for the mailing list.
        :type name: str
        :return: A string indicating the success or failure of the method call.
        '''
        assert mailing_list != None, 'Hey there! The mailing_list parameter cannot be None. You need to pass in a Mailing List ID as a string into the mailing_list parameter.'
        assert isinstance(mailing_list, str) == True, 'Hey there! The mailing_list parameter must be of type string.'
        assert name != None, 'Hey there! The name parameter cannot be None. You need to pass in a new Mailing List name as a string into the name parameter.'
        assert isinstance(name, str) == True, 'Hey there! The name parameter must be of type string.'
        assert len(mailing_list) == 18, 'Hey there! The parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. Please try again.'

        data = {"name": f"{name}"}
        headers, base_url = self.header_setup(content_type=True, xm=True)
        url = f"{base_url}/mailinglists/{mailing_list}"
        request = r.put(url, json=data, headers=headers)
        response = request.json()
        try:
            if response['meta']['httpStatus'] == '200 - OK':
                print(f'Your mailing list "{mailing_list}" has been renamed to {name} in the XM Directory.')
        except:
            print(f"ServerError: {response['meta']['httpStatus']}\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")
        return

    def delete_list(self, mailing_list=None):
        '''This method will delete the specified mailing list from the given users XM Directory.

        :param mailing_list: Your mailing list id that you are interested in deleting.
        :type mailing_list: str
        :return: A string indicating the success or failure of the method call.
        '''

        assert mailing_list != None, 'Hey, the mailing_list parameter cannot be None. You need to pass in a Mailing List ID as a string into the mailing_list parameter.'
        assert isinstance(mailing_list, str) == True, 'Hey there, the mailing_list parameter must be of type string.'
        assert len(mailing_list) == 18, 'Hey there! The parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. Please try again.'

        data = {"name": f"{mailing_list}"}
        headers, base_url = self.header_setup(xm=True)
        url = f"{base_url}/mailinglists/{mailing_list}"
        request = r.delete(url, json=data, headers=headers)
        response = request.json()
        try:
            if response['meta']['httpStatus'] == '200 - OK':
                print(f'Your mailing list "{mailing_list}" has been deleted from the XM Directory.')
        except:
            print(f"ServerError: {response['meta']['httpStatus']}\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")
        return

    def list_contacts(self, mailing_list=None, page_size=100):
        '''This method creates a pandas DataFrame of all the contacts information within the defined mailing list.

        :param mailing_list: the mailing list id
        :type mailing_list: str
        :param page_size: The number of contacts in the mailing list to return per call. (typically this doesn't not need to be changed.)
        :type page_size: int
        :return: A Pandas DataFrame
        '''
        assert len(mailing_list) == 18, 'Hey, the parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. Please try again.'
        assert page_size != 0, 'Hey there! You need to have a page size greater than 1'
 
        contact_list = pd.DataFrame()
        headers, base_url = self.header_setup(xm=True)
        url = base_url + f"/mailinglists/{mailing_list}/contacts?pageSize={page_size}"
        try:
          def get_page(mailing_list=mailing_list, contact_list=contact_list, url=url):
            request = r.get(url, headers=headers)
            response = request.json()
            keys = ['contactId','firstName','lastName','email','phone','extRef','language','unsubscribed']
            contact_lists = Parser().json_parser(response=response, keys=keys, arr=False)
            single_page = pd.DataFrame(contact_lists).transpose()
            single_page.columns = keys
            single_page['mailing_list'] = mailing_list
            contact_list = pd.concat([contact_list, single_page]).reset_index(drop=True)
            next_page = str(response['result']['nextPage'])
            return contact_list, next_page, response
          contact_list, next_page, response = get_page(mailing_list=mailing_list, contact_list=contact_list, url=url)
          while next_page != 'None':
            contact_list, next_page, response = get_page(mailing_list=mailing_list, contact_list=contact_list, url=next_page)
          return contact_list
        except:
          print(f"ServerError: {response['meta']['httpStatus']}\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")

    def create_contact_in_list(self, mailing_list=None, **kwargs):
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

        dynamic_payload = {}
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
        url = base_url + f"/mailinglists/{mailing_list}/contacts"
        request = r.post(url, json=dynamic_payload, headers=headers)
        response = request.json()
        try:
            if response['meta']['httpStatus'] == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            contact_id = response['result']['id']
        except Qualtrics500Error:
            attempt = 0
            while attempt < 20:
                request = r.post(url, json=dynamic_payload, headers=headers)
                response = request.json()
                if response['meta']['httpStatus'] == '500 - Internal Server Error':
                    attempt+=1
                    t.sleep(0.25)
                    continue
                elif response['meta']['httpStatus'] == '200 - OK':
                    return response['result']['id'], response['result']['contactLookupId']
            return print(f"ServerError: {response['meta']['httpStatus']}\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")
        except Exception:
            print(f"ServerError: {response['meta']['httpStatus']}\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")
        else:
            contact_list_id = response['result']['contactLookupId']
            return contact_id, contact_list_id