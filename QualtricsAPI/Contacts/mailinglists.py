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

    def create_list(self, name):
        '''This function creates a mailing list in the XM Directory for the specified user token.

        :param list_name: the name of the list to be created.
        :return: set containing the list_name and the list's new id
        '''
        try:
            headers, url = self.header_setup(content_type=True)
            url = url + "/mailinglists"
            data = {"name": "{0}".format(name)}
            request = r.post(url, json=data, headers=headers)
            content = request.json()
            list_id = Parser().json_parser(response=content,keys=['id'], arr=False)[0][0]
            list_params = tuple([name, list_id])
            return list_params
        except:
            raise ValueError(f"ServerError:\nError Code: {content['meta']['error']['errorCode']}\nError Message: {content['meta']['error']['errorMessage']}")


    def list_lists(self, page_size=100, offset=0, to_df=True):
        '''This function lists all the mailing lists in the directory for the specified user token.

        :param page_size: the number of contacts per call.
        :param offset: the offset from the order of contacts.
        :param to_df: if True, returns the mailing lists and their member objects in a pandas DataFrame.
        :return: either a pandas DataFrame or a list of tuples, containing lists and their respective member objects.
        '''
        headers, base_url = self.header_setup()
        url = base_url + f"/mailinglists?pageSize={page_size}&offset={offset}"
        response = r.get(url, headers=headers)
        lists = response.json()
        mailing_lists = self.Parser(response=lists, keys=['results','mailingListId', 'name', 'ownerId', 'contactCount', 'lastModifiedDate', 'creationDate'])
        if to_df is True:
            mailing_lists = pd.DataFrame(mailing_lists,columns=['list_ids','list_names','owner_ids','contact_count','last_modified','creation_date'])
            mailing_lists['last_modified'] = pd.to_datetime(mailing_lists['last_modified'],unit='ms')
            mailing_lists['creation_date'] = pd.to_datetime(mailing_lists['creation_date'],unit='ms')
            return mailing_lists.head()
        return mailing_lists

    def get_list(self, mailing_list):
        '''This function gets the list specfied by the mailing list param and returns the list members.

        :param mailing_list: the mailing list id.
        :return: a dictionary containing the mailing list member objects.
        '''
        headers, base_url = self.header_setup()
        url = base_url + f"/mailinglists/{mailing_list}"
        response = r.get(url, headers=headers)
        content = response.json()
        list_info = {
                    "list_id": content['result']['mailingListId'],
                    "list_name": content['result']['name'],
                    "owner_id": content['result']['ownerId'],
                    "contact_count": content['result']['contactCount'],
                    "last_modified": t.ctime(content['result']['lastModifiedDate']*0.001),
                    "creation_date": t.ctime(content['result']['creationDate']*0.001)
        }
        assert len(mailing_list) == 18, "Check your arguement, the parameter (mailing_list) should have 17 characters."
        if content['meta']['httpStatus'] == '200 - OK':
            pass
        else:
            raise ValueError(f"ServerError:{content['meta']['error']['errorCode']}, {content['meta']['error']['errorMessage']}")
        return list_info

    def rename_list(self, mailing_list, name=None):
        '''This function takes an existing mailing list name and updates it to reflect the name defined in this function.

        :param mailing_list: the mailing list id.
        :param name: the new name for the mailing list.
        :return: nothing, but prints a if successful.
        '''
        data = {"name": f"{str(name)}"}
        headers, base_url = self.header_setup(content_type=True)
        url = base_url + f"/mailinglists/{str(mailing_list)}"
        response = r.put(url, json=data, headers=headers)
        content = response.json()
        assert len(mailing_list) == 18, "Check your arguement, the parameter (mailing_list) should have 17 characters."
        if content['meta']['httpStatus'] == '200 - OK':
            print(f'Your mailing list "{str(mailing_list)}" has been deleted from the XM Directory')
        else:
            raise ValueError(f"ServerError:{content['meta']['error']['errorCode']}, {content['meta']['error']['errorMessage']}")
        return

    def delete_list(self,mailing_list):
        '''This function deletes a mailing list from the XM Directory.

        :param mailing_list: the mailing list id
        :return: nothing, but prints a if successful and errors if unsuccessful.
        '''
        data = {"name": f"{str(mailing_list)}"}
        headers, base_url = self.header_setup()
        url = base_url + f"/mailinglists/{str(mailing_list)}"
        response = r.delete(url, json=data, headers=headers)
        content = response.json()
        assert len(mailing_list) == 18, "Check your arguement, the parameter (mailing_list) should have 17 characters."
        if content['meta']['httpStatus'] == '200 - OK':
            print(f'Your mailing list "{str(mailing_list)}" has been deleted from the XM Directory')
        else:
            raise ValueError(f"ServerError:{content['meta']['error']['errorCode']}, {content['meta']['error']['errorMessage']}")
        return

    def list_contacts(self, mailing_list):
        '''This function lists the contacts within the defined mailing list.

        :param mailing_list: the mailing list id
        :return: a pandas DataFrame containing the contact information.
        '''
        headers, base_url = self.header_setup()
        url = base_url + f"/mailinglists/{str(mailing_list)}/contacts"
        response = r.get(url, headers=headers)
        lists = response.json()
        contact_lists = []
        i=0
        while lists['result']['nextPage'] is not None:
            contact_list = self.json_parse(lists,'results','contactId','firstName', 'lastName', 'email', 'phone', 'extRef', 'language', 'unsubscribed')
            contact_list_ = pd.DataFrame(contact_list, columns=['contact_id','first_name','last_name','email','phone',
                                                               'unsbscribed','language','external_ref'])
            contact_list_['mailing_list'] = mailing_list
            contact_lists.append(contact_list_)
            url = lists['result']['nextPage']
            response = r.get(url, headers=headers)
            lists = response.json()
            if lists['result']['nextPage'] is not None:
                pass
            else:
                print('finished')
            i+=1
        contact_list = pd.concat(contact_lists).reset_index(drop=True)
        return contact_list

    def create_contact_in_list(self,mailing_list, first_name=None, last_name=None, email=None, phone=None, external_ref=None, unsubscribed=False,language="en",metadata={}):
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
        data = {
            "firstName": str(first_name),
            "lastName": str(last_name),
            "email": str(email),
            "phone": str(phone),
            "embeddedData": metadata,
            "language": str(language),
            "extRef": str(external_ref),
            "unsubscribed": str(unsubscribed)
        }

        headers, base_url = self.header_setup(content_type=True)
        url = base_url + f"/mailinglists/{str(mailing_list)}/contacts"
        response = r.post(url, json=data, headers=headers)
        content = response.json()
        contact_id = content['result']['id']
        contact_list_id = content['result']['contactLookupId']
        return contact_id, contact_list_id
