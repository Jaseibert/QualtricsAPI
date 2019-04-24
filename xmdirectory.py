import requests as r
import pandas as pd
import time as t
import io
import json


class Credentials(object):

    def __init__(self, token=None, survey_id=None, directory_id=None,file_format=None,
                 data_center=None, export_type='LegacyV3'):
        self.token = token
        self.data_center = data_center
        self.directory_id = directory_id
        self.survey_id = survey_id
        self.file_format = file_format
        self.export_type = export_type
        return

    def header_setup(self,content_type=False):
        '''This function accepts the argument content_type and returns the correct header, and base url.

        :param content_type: use to return json response.
        :return: a HTML header and base url.
        '''
        header = {"x-api-token": str(self.token)}
        base_url = f"https://{str(self.data_center)}.qualtrics.com/API/v3/directories/{str(self.directory_id)}/"
        if content_type is not False:
            header["Content-Type"] = "application/json"
        else:
            pass
        return header, base_url

class MailingList(Credentials):

    def __init__(self):
        super().__init__(token=self.token, data_center=self.col, directory_id=self.directory_id)
        return

    def create_list(self, list_name=None):
        '''This function creates a mailing list in the XM Directory for the specified user token.

        :param list_name: the name of the list to be created.
        :return: set containing the list_name and the list's new id
        '''
        headers, url = self.header_setup(content_type=True)
        url = url + "/mailinglists"
        data = {"name": f"{str(list_name)}"}
        response = r.post(url, json=data, headers=headers)
        content = response.json()
        list_id = content['result']['id']
        list_params = tuple([list_name, list_id])
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
        response = r.get(url, headers=headers)
        lists = response.json()
        list_ids = [lists['result']['elements'][i]['mailingListId'] for i in range(0,len(lists['result']['elements']))]
        list_names = [lists['result']['elements'][i]['name'] for i in range(0,len(lists['result']['elements']))]
        owner_ids = [lists['result']['elements'][i]['ownerId'] for i in range(0,len(lists['result']['elements']))]
        contact_count = [lists['result']['elements'][i]['contactCount'] for i in range(0,len(lists['result']['elements']))]
        last_modified = [lists['result']['elements'][i]['lastModifiedDate'] for i in range(0,len(lists['result']['elements']))]
        creation_date = [lists['result']['elements'][i]['creationDate'] for i in range(0,len(lists['result']['elements']))]
        mailing_lists = list(zip(list_ids,list_names,owner_ids,contact_count,last_modified,creation_date))
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
            #This could be refactored
            contact_id = [lists['result']['elements'][i]['contactId'] for i in range(0,len(lists['result']['elements']))]
            first_name = [lists['result']['elements'][i]['firstName'] for i in range(0,len(lists['result']['elements']))]
            last_name = [lists['result']['elements'][i]['lastName'] for i in range(0,len(lists['result']['elements']))]
            email = [lists['result']['elements'][i]['email'] for i in range(0,len(lists['result']['elements']))]
            phone = [lists['result']['elements'][i]['phone'] for i in range(0,len(lists['result']['elements']))]
            external_ref = [lists['result']['elements'][i]['extRef'] for i in range(0,len(lists['result']['elements']))]
            language = [lists['result']['elements'][i]['phone'] for i in range(0,len(lists['result']['elements']))]
            unsubscribed = [lists['result']['elements'][i]['extRef'] for i in range(0,len(lists['result']['elements']))]
            contact_list = list(zip(contact_id,first_name,last_name,email,phone,unsubscribed,language,external_ref))
            contact_list_ = pd.DataFrame(contact_list,columns=['contact_id','first_name','last_name','email','phone',
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
        return contact_list.info()

    def create_contact_in_list(self,mailing_list, first_name=None, last_name=None, email=None,
                             phone=None, external_ref=None, unsubscribed=False,language="en",metadata={}):
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

class XMDirectory(Credentials):

    def __init__(self):
        super().__init__(token=self.token, data_center=self.col, directory_id=self.directory_id)

    def create_contact_in_XM(self, first_name=None, last_name=None, email=None,
                             phone=None, language="en", metadata={}):
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
            "firstName": str(first_name),
            "lastName": str(last_name),
            "email": str(email),
            "phone": str(phone),
            "language": str(language),
            "embeddedData": metadata,
        }
        headers, base_url = self.header_setup(content_type=True)
        url = base_url + "/contacts"
        response = r.post(url, json=contact_data, headers=headers)
        content = response.json()
        contact_id = content['result']['id']
        return contact_id

    def delete_contact(self,contact_id):
        '''This function will delete a user from IQDirectory.

        :param contact_id: The unique id associated with each contact in the XM Directory.
        :return: nothing, but prints if successful, and if there was an error.
        '''
        headers, base_url = self.header_setup()
        url = base_url + f"/contacts/{str(contact_id)}"
        response = r.delete(url, headers=headers)
        content = response.json()
        if content['meta']['httpStatus'] == '200 - OK':
            print(f'Your XM Contact"{str(mailing_list)}" has been deleted from the XM Directory.')
        else:
            raise ValueError(f"ServerError:{content['meta']['error']['errorCode']}, {content['meta']['error']['errorMessage']}")
        return

    def list_contacts_in_directory(self, page_size=100, offset=0, to_df=True):
        '''This function lists the contacts in the XM Directory.

        :param page_size: determines the number of contacts to return per call.
        :param offset: the offset sets the start number within the directory for the call.
        '''
        headers, base_url = self.header_setup()
        url = base_url + f"/contacts?pageSize={page_size}&offset={offset}"
        response = r.get(url, headers=headers)
        contacts = response.json()
        contact_id = [contacts['result']['elements'][i]['contactId'] for i in range(0,len(contacts['result']['elements']))]
        email = [str(contacts['result']['elements'][i]['email']).lower() for i in range(0,len(contacts['result']['elements']))]
        length_of_addresses = [len(email[i]) for i in range(0,len(email))]
        if to_df is False:
            contact_list = list(zip(length_of_addresses,email,contact_id))
        else:
            contact_list = pd.DataFrame(list(zip(contact_id, email)),columns=['cid','email'])
        return contact_list

class QualtricsSurveyResponses(Credentials):

    def __init__(self):
        super().__init__(token=self.token, data_center=self.col, directory_id=self.directory_id)
        return

    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
    }

    def url_and_payload_setup(self):
        ''''''
        #Add Logic
        headers, base_url = self.header_setup()
        url = "https://{0}.qualtrics.com/API/v3/responseexports/".format(self.data_center)
        request_payload = '{"format":"' + self.file_format + '","surveyId":"' + self.survey_id + '"}'
        return url, request_payload

    def setup_request(self):
        ''''''
        url, request_payload = self.url_and_payload_setup()
        request_response = r.request("POST", url, data=request_payload, headers=self.headers)
        print(request_response.text)
        progress_id = request_response.json()["result"]["id"]
        return progress_id, url

    def send_request(self):
        file = None
        progress_id, url = self.setup_request()
        check_progress = 0
        progress_status = "In Progress"
        while check_progress < 100 and progress_status is not "complete" and file is None:
            check_url = url + progress_id
            check_response = r.request("GET", check_url, headers=self.headers)
            file = (check_response.json()["result"]["file"])
            if file is None:
                print ("file not ready")
            else:
                print ("file created:", check_response.json()["result"]["file"])
            check_progress = check_response.json()["result"]["percentComplete"]
            print("Download is " + str(check_progress) + " complete")
            download_url = url + progress_id + '/file'
            download_request = r.request("GET", download_url, headers=self.headers, stream=True)
        return

    def get_responses(self):
        download_request = self.download_responses()
        folder_name = str(input("What is the Folder Name for the Download?: "))
        zipfile.ZipFile(io.BytesIO(download_request.content)).extractall(f'{folder_name}')
        print('The folder "{0}" has been created with your survey responses stored inside.'.format(folder_name))
