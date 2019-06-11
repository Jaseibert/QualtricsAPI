import time as t
import io
import json
import requests as r
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser

class MailingList(Credentials):

    def __init__(self, token=None, directory_id=None, data_center=None):
        self.token = token
        self.data_center = data_center
        self.directory_id = directory_id
        return

    def create_list(self, name=None):
        '''This function creates a mailing list in the XM Directory for the specified user token.

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
        '''This function lists all the mailing lists in the directory for the specified user token.

        :param page_size: the number of contacts per call.
        :param offset: the offset from the order of contacts.
        :param to_df: if True, returns the mailing lists and their member objects in a pandas DataFrame.
        :return: either a pandas DataFrame or a list of tuples, containing lists and their respective member objects.
        '''

        headers, base_url = self.header_setup()
        url = base_url + f"/mailinglists?pageSize={page_size}&offset={offset}"
        request = r.get(url, headers=headers)
        response = request.json()
        keys = Parser().extract_keys(response)[2:-4]
        mailing_lists = Parser().json_parser(response=response, keys=keys, arr=False)
        if to_df is True:
            mailing_list = pd.DataFrame(mailing_lists).transpose()
            mailing_list.columns = keys
            #mailing_list['creationDate'] = pd.to_datetime(mailing_list['creationDate'],unit='ms')
            #mailing_list['lastModified'] = pd.to_datetime(mailing_list['lastModified'],unit='ms')
            return mailing_list
        return mailing_lists

    def get_list(self, mailing_list=None):
        '''This function gets the list specfied by the mailing list param and returns the list members.

        :param mailing_list: the mailing list id.
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
                        "list_id": response['result']['mailingListId'],
                        "list_name": response['result']['name'],
                        "owner_id": response['result']['ownerId'],
                        "contact_count": response['result']['contactCount'],
                        "last_modified": t.ctime(response['result']['lastModifiedDate']*0.001),
                        "creation_date": t.ctime(response['result']['creationDate']*0.001)
            }
            #Return a DataFrame?
        except MailingListIDError:
            print('Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.')
        return list_info

    def rename_list(self, mailing_list=None, name=None):
        '''This function takes an existing mailing list name and updates it to reflect the name defined in this function.

        :param mailing_list: the mailing list id.
        :param name: the new name for the mailing list.
        :return: nothing, but prints a if successful.
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
                print(f'Your mailing list "{mailing_list}" has been renamed in the XM Directory')
        except MailingListIDError:
            print('Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.')
        return

    def delete_list(self,mailing_list=None):
        '''This function deletes a mailing list from the XM Directory.

        :param mailing_list: the mailing list id
        :return: nothing, but prints a if successful and errors if unsuccessful.
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
                print(f'Your mailing list "{mailing_list}" has been deleted from the XM Directory')
        except MailingListIDError:
            print('Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.')
        return

    def list_contacts(self, mailing_list=None):
        '''This function lists the contacts within the defined mailing list.

        :param mailing_list: the mailing list id
        :return: a pandas DataFrame containing the contact information.
        '''
        assert len(mailing_list) == 18, 'Hey, the parameter for "mailing_list" that was passed is the wrong length. It should have 18 characters.'
        assert mailing_list[:3] == 'CG_', 'Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. Please try again.'

        try:
            headers, base_url = self.header_setup()
            url = base_url + f"/mailinglists/{mailing_list}/contacts"
            response = r.get(url, headers=headers)
            lists = response.json()
            contact_lists = []
            i=0
            while lists['result']['nextPage'] is not None:
                contact_list = Parser().json_parser(lists,'results','contactId','firstName', 'lastName', 'email', 'phone', 'extRef', 'language', 'unsubscribed')
                contact_list_ = pd.DataFrame(contact_list, columns=['contact_id','first_name','last_name','email','phone','unsbscribed','language','external_ref'])
                contact_list_['mailing_list'] = mailing_list
                contact_lists.append(contact_list_)
                url = lists['result']['nextPage']
                response = r.get(url, headers=headers)
                lists = response.json()
                i+=1
            contact_list = pd.concat(contact_lists).reset_index(drop=True)
        except MailingListIDError:
            print('Hey there! It looks like your Mailing List ID is incorrect. You can find the Mailing List ID on the Qualtrics site under your account settings. It will begin with "CG_". Please try again.')
        return contact_list

    def create_contact_in_list(self, mailing_list=None, first_name=None, last_name=None, email=None, phone=None, external_ref=None, unsubscribed=False,language="en",metadata={}):
        '''This function creates contacts in a specified mailing list.

        :param mailing_list: the mailing list id.
        :param first_name: the contacts first name.
        :param last_name: the contacts last name.
        :param email: the contacts email.
        :param phone: the contacts phone number.
        :param external_ref: the contacts external reference.
        :param unsubscribed: denotes whether the contact is unsubscribed.
        :param language: the native language of the contact (Default: English)
        :param metadata: any relevant contact metadata.
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
