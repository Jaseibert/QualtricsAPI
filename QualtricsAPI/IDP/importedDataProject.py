import requests as r
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.Exceptions import Qualtrics500Error, Qualtrics503Error, Qualtrics504Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error
import zipfile
import io
import json


class ImportedDataProject(Credentials):

    def __init__(self, idp_source_id=None):
        self.idp_source_id = idp_source_id
        return

    def get_idp_schema(self, idp_id=None):
        ''' This method returns a dictionary object containing the schema of the idp
        '''
        assert idp_id != None or self.idp_source_id != None, 'Hey There! You need to set an ID when you instantiate the class, or pass one when you make this call.'

        # Reset the idp ID from whichever source is set - These are not standardized, so we can't check if they're good
        if idp_id == None:
            idp_id = self.idp_source_id
        elif self.idp_source_id == None:
            self.idp_source_id = idp_id

        headers, url = self.header_setup(
            content_type=False, accept=True, xm=False, path=f'imported-data-projects/{self.idp_source_id}')
        request = r.get(url, headers=headers)
        response = request.json()

        try:
            if response['meta']['httpStatus'] == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            elif response['meta']['httpStatus'] == '503 - Temporary Internal Server Error':
                raise Qualtrics503Error(
                    '503 - Temporary Internal Server Error')
            elif response['meta']['httpStatus'] == '504 - Gateway Timeout':
                raise Qualtrics504Error('504 - Gateway Timeout')
            elif response['meta']['httpStatus'] == '400 - Bad Request':
                raise Qualtrics400Error(
                    'Qualtrics Error\n(Http Error: 400 - Bad Request): There was something invalid about the request.')
            elif response['meta']['httpStatus'] == '401 - Unauthorized':
                raise Qualtrics401Error(
                    'Qualtrics Error\n(Http Error: 401 - Unauthorized): The Qualtrics API user could not be authenticated or does not have authorization to access the requested resource.')
            elif response['meta']['httpStatus'] == '403 - Forbidden':
                raise Qualtrics403Error(
                    'Qualtrics Error\n(Http Error: 403 - Forbidden): The Qualtrics API user was authenticated and made a valid request, but is not authorized to access this requested resource.')
        except (Qualtrics503Error, Qualtrics504Error) as e:
            # Recursive call to handle Internal Server Errors
            return self.get_idp_schema(idp_id=self.idp_source_id)
        except (Qualtrics500Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            # Handle Authorization/Bad Request Errors
            return print(e, response['meta'])
        else:

            return response['meta'], response['result']

    def add_columns_to_idp(self, idp_id=None, fields=None):
        ''''''
        assert idp_id != None or self.idp_source_id != None, 'Hey There! You need to set an ID when you instantiate the class, or pass one when you make this call.'
        self._validate_fields(fields)
        # Reset the idp ID from whichever source is set - These are not standardized, so we can't check if they're good
        if idp_id == None:
            idp_id = self.idp_source_id
        elif self.idp_source_id == None:
            self.idp_source_id = idp_id

        headers, url = self.header_setup(
            content_type=True, accept=True, xm=False, path=f'imported-data-projects/{self.idp_source_id}')
        payload = {"fields": fields}
        request = r.post(url, json=payload, headers=headers)
        response = request.json()

        try:
            if response['meta']['httpStatus'] == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            elif response['meta']['httpStatus'] == '503 - Temporary Internal Server Error':
                raise Qualtrics503Error(
                    '503 - Temporary Internal Server Error')
            elif response['meta']['httpStatus'] == '504 - Gateway Timeout':
                raise Qualtrics504Error('504 - Gateway Timeout')
            elif response['meta']['httpStatus'] == '400 - Bad Request':
                raise Qualtrics400Error(
                    'Qualtrics Error\n(Http Error: 400 - Bad Request): There was something invalid about the request.')
            elif response['meta']['httpStatus'] == '401 - Unauthorized':
                raise Qualtrics401Error(
                    'Qualtrics Error\n(Http Error: 401 - Unauthorized): The Qualtrics API user could not be authenticated or does not have authorization to access the requested resource.')
            elif response['meta']['httpStatus'] == '403 - Forbidden':
                raise Qualtrics403Error(
                    'Qualtrics Error\n(Http Error: 403 - Forbidden): The Qualtrics API user was authenticated and made a valid request, but is not authorized to access this requested resource.')
        except (Qualtrics503Error, Qualtrics504Error) as e:
            # Recursive call to handle Internal Server Errors
            return self.add_columns_to_idp(idp_id=idp_id, fields=fields)
        except (Qualtrics500Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            # Handle Authorization/Bad Request Errors
            return print(e, response['meta'])
        else:
            print(
                f"Successfully added columns to idp: {', '.join([field['name'] for field in fields])}")
            return response['meta']

    def add_single_record(self, idp_id=None, record=None):
        ''' This method adds a single record to an IDP

        :param record: a dictionary containing key-value pairs for the data of the record to be created
        :return: the result of the record creation HTTP request
        '''
        assert idp_id != None or self.idp_source_id != None, 'Hey There! You need to set an ID when you instantiate the class, or pass one when you make this call.'
        if record == None:
            record = {}
        self._validate_single_record(record)

        # Reset the idp ID from whichever source is set - These are not standardized, so we can't check if they're good
        if idp_id == None:
            idp_id = self.idp_source_id
        elif self.idp_source_id == None:
            self.idp_source_id = idp_id

        headers, url = self.header_setup(
            content_type=True, accept=True, xm=False, path=f'imported-data-projects/{self.idp_source_id}/record')
        request = r.post(url, json=record, headers=headers)
        response = request.json()

        try:
            if response['meta']['httpStatus'] == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            elif response['meta']['httpStatus'] == '503 - Temporary Internal Server Error':
                raise Qualtrics503Error(
                    '503 - Temporary Internal Server Error')
            elif response['meta']['httpStatus'] == '504 - Gateway Timeout':
                raise Qualtrics504Error('504 - Gateway Timeout')
            elif response['meta']['httpStatus'] == '400 - Bad Request':
                raise Qualtrics400Error(
                    'Qualtrics Error\n(Http Error: 400 - Bad Request): There was something invalid about the request.')
            elif response['meta']['httpStatus'] == '401 - Unauthorized':
                raise Qualtrics401Error(
                    'Qualtrics Error\n(Http Error: 401 - Unauthorized): The Qualtrics API user could not be authenticated or does not have authorization to access the requested resource.')
            elif response['meta']['httpStatus'] == '403 - Forbidden':
                raise Qualtrics403Error(
                    'Qualtrics Error\n(Http Error: 403 - Forbidden): The Qualtrics API user was authenticated and made a valid request, but is not authorized to access this requested resource.')
        except (Qualtrics503Error, Qualtrics504Error) as e:
            # Recursive call to handle Internal Server Errors
            return self.add_single_record(idp_id=idp_id, record=record)
        except (Qualtrics500Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            # Handle Authorization/Bad Request Errors
            return print(e, response['meta'])
        else:
            print(
                f"Successfully added record to idp: {record}")
            return response['meta']

    def get_single_record_from_idp(self, idp_id=None, unique_field=None):
        ''' Get a single record from an IDP

        '''
        assert idp_id != None or self.idp_source_id != None, 'Hey There! You need to set an ID when you instantiate the class, or pass one when you make this call.'
        assert unique_field != None, "Hey there! Unique fields must not be none"

        if idp_id == None:
            idp_id = self.idp_source_id
        elif self.idp_source_id == None:
            self.idp_source_id = idp_id

        headers, url = self.header_setup(content_type=False, accept=True, xm=False,
                                         path=f'imported-data-projects/{self.idp_source_id}/records/{unique_field}')
        request = r.get(url, headers=headers)
        response = request.json()

        try:
            if response['meta']['httpStatus'] == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            elif response['meta']['httpStatus'] == '503 - Temporary Internal Server Error':
                raise Qualtrics503Error(
                    '503 - Temporary Internal Server Error')
            elif response['meta']['httpStatus'] == '504 - Gateway Timeout':
                raise Qualtrics504Error('504 - Gateway Timeout')
            elif response['meta']['httpStatus'] == '400 - Bad Request':
                raise Qualtrics400Error(
                    'Qualtrics Error\n(Http Error: 400 - Bad Request): There was something invalid about the request.')
            elif response['meta']['httpStatus'] == '401 - Unauthorized':
                raise Qualtrics401Error(
                    'Qualtrics Error\n(Http Error: 401 - Unauthorized): The Qualtrics API user could not be authenticated or does not have authorization to access the requested resource.')
            elif response['meta']['httpStatus'] == '403 - Forbidden':
                raise Qualtrics403Error(
                    'Qualtrics Error\n(Http Error: 403 - Forbidden): The Qualtrics API user was authenticated and made a valid request, but is not authorized to access this requested resource.')
        except (Qualtrics503Error, Qualtrics504Error) as e:
            # Recursive call to handle Internal Server Errors
            return self.get_single_record_from_idp(idp_id=idp_id, unique_field=unique_field)
        except (Qualtrics500Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            # Handle Authorization/Bad Request Errors
            return print(e, response['meta'])
        else:
            print(
                f"Successfully fetched record to idp: {unique_field}")
            return response['result']

    def delete_record_from_idp(self, idp_id=None, unique_field=None):
        ''' This method takes in the key field of the IDP record to be deleted and calls the delete command

        :param unique_field: the key identifier of the record to be deleted
        :return: HTTP status of response
        '''
        assert idp_id != None or self.idp_source_id != None, 'Hey There! You need to set an ID when you instantiate the class, or pass one when you make this call.'
        assert unique_field != None, "Hey there! Unique fields must not be none"

        if idp_id == None:
            idp_id = self.idp_source_id
        elif self.idp_source_id == None:
            self.idp_source_id = idp_id

        headers, url = self.header_setup(content_type=False, accept=True, xm=False,
                                         path=f'imported-data-projects/{self.idp_source_id}/records/{unique_field}')
        request = r.delete(url, headers=headers)
        response = request.json()

        try:
            if response['meta']['httpStatus'] == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            elif response['meta']['httpStatus'] == '503 - Temporary Internal Server Error':
                raise Qualtrics503Error(
                    '503 - Temporary Internal Server Error')
            elif response['meta']['httpStatus'] == '504 - Gateway Timeout':
                raise Qualtrics504Error('504 - Gateway Timeout')
            elif response['meta']['httpStatus'] == '400 - Bad Request':
                raise Qualtrics400Error(
                    'Qualtrics Error\n(Http Error: 400 - Bad Request): There was something invalid about the request.')
            elif response['meta']['httpStatus'] == '401 - Unauthorized':
                raise Qualtrics401Error(
                    'Qualtrics Error\n(Http Error: 401 - Unauthorized): The Qualtrics API user could not be authenticated or does not have authorization to access the requested resource.')
            elif response['meta']['httpStatus'] == '403 - Forbidden':
                raise Qualtrics403Error(
                    'Qualtrics Error\n(Http Error: 403 - Forbidden): The Qualtrics API user was authenticated and made a valid request, but is not authorized to access this requested resource.')
        except (Qualtrics503Error, Qualtrics504Error) as e:
            # Recursive call to handle Internal Server Errors
            return self.delete_record_from_idp(idp_id=idp_id, unique_field=unique_field)
        except (Qualtrics500Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            # Handle Authorization/Bad Request Errors
            return print(e, response['meta'])
        else:
            print(
                f"Successfully deleted record from idp: {unique_field}")
            return response['meta']

    def add_many_records(self, idp_id=None, records=None):
        '''

        '''
        assert idp_id != None or self.idp_source_id != None, 'Hey There! You need to set an ID when you instantiate the class, or pass one when you make this call.'
        if records == None:
            records = [{}]
        for record in records:
            self._validate_single_record(record)

        # Reset the idp ID from whichever source is set - These are not standardized, so we can't check if they're good
        if idp_id == None:
            idp_id = self.idp_source_id
        elif self.idp_source_id == None:
            self.idp_source_id = idp_id

        headers, url = self.header_setup(
            content_type=True, accept=True, xm=False, path=f'imported-data-projects/{self.idp_source_id}/records')
        payload = {"records": records}
        request = r.post(url, json=payload, headers=headers)
        response = request.json()

        try:
            if response['meta']['httpStatus'] == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            elif response['meta']['httpStatus'] == '503 - Temporary Internal Server Error':
                raise Qualtrics503Error(
                    '503 - Temporary Internal Server Error')
            elif response['meta']['httpStatus'] == '504 - Gateway Timeout':
                raise Qualtrics504Error('504 - Gateway Timeout')
            elif response['meta']['httpStatus'] == '400 - Bad Request':
                raise Qualtrics400Error(
                    'Qualtrics Error\n(Http Error: 400 - Bad Request): There was something invalid about the request.')
            elif response['meta']['httpStatus'] == '401 - Unauthorized':
                raise Qualtrics401Error(
                    'Qualtrics Error\n(Http Error: 401 - Unauthorized): The Qualtrics API user could not be authenticated or does not have authorization to access the requested resource.')
            elif response['meta']['httpStatus'] == '403 - Forbidden':
                raise Qualtrics403Error(
                    'Qualtrics Error\n(Http Error: 403 - Forbidden): The Qualtrics API user was authenticated and made a valid request, but is not authorized to access this requested resource.')
        except (Qualtrics503Error, Qualtrics504Error) as e:
            # Recursive call to handle Internal Server Errors
            return self.add_many_records(idp_id=idp_id, records=records)
        except (Qualtrics500Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            # Handle Authorization/Bad Request Errors
            return print(e, response['meta'])
        else:
            print(
                f"Successfully added records to idp: {len(records)}")
            return response['meta']

    def setup_get_file_request(self, idp_id=None, payload=None):
        ''' This method makes the initial request and returns the progress id for the file download'''
        assert idp_id != None or self.idp_source_id != None, 'Hey There! You need to set an ID when you instantiate the class, or pass one when you make this call.'

        if idp_id == None:
            idp_id = self.idp_source_id
        elif self.idp_source_id == None:
            self.idp_source_id = idp_id
        # make the reqest
        headers, url = self.header_setup(
            content_type=True, accept=True, xm=False, path=f'imported-data-projects/{idp_id}/exports')
        request = r.post(url, data=json.dumps(payload), headers=headers)
        response = request.json()
        print('job start response:', response)
        try:
            if response['meta']['httpStatus'] == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            elif response['meta']['httpStatus'] == '503 - Temporary Internal Server Error':
                raise Qualtrics503Error(
                    '503 - Temporary Internal Server Error')
            elif response['meta']['httpStatus'] == '504 - Gateway Timeout':
                raise Qualtrics504Error('504 - Gateway Timeout')
            elif response['meta']['httpStatus'] == '400 - Bad Request':
                raise Qualtrics400Error(
                    'Qualtrics Error\n(Http Error: 400 - Bad Request): There was something invalid about the request.')
            elif response['meta']['httpStatus'] == '401 - Unauthorized':
                raise Qualtrics401Error(
                    'Qualtrics Error\n(Http Error: 401 - Unauthorized): The Qualtrics API user could not be authenticated or does not have authorization to access the requested resource.')
            elif response['meta']['httpStatus'] == '403 - Forbidden':
                raise Qualtrics403Error(
                    'Qualtrics Error\n(Http Error: 403 - Forbidden): The Qualtrics API user was authenticated and made a valid request, but is not authorized to access this requested resource.')
        except (Qualtrics500Error, Qualtrics503Error, Qualtrics504Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            return print(e)
        else:
            print("START RESPONSE", response)
            job_id = response['result']['jobId']
            return job_id, url+"/"+job_id, headers

    def send_get_file_request(self, idp_id=None, payload=None):
        '''This method starts the request to download the IDP data'''
        is_file = None
        job_id, url, headers = self.setup_get_file_request(
            idp_id=idp_id, payload=payload)
        progress_status = "in progress"
        print("jobid:", job_id)
        print("url chekin", url)
        while progress_status != "complete" and progress_status != "failed" and is_file is None:
            check_request = r.get(url, headers=headers)
            check_response = check_request.json()
            print("check_response", check_response)
            try:
                is_file = check_response['result']['fileId']
            except KeyError:
                pass
            progress_status = check_response['result']['status']
        try:
            if check_response['meta']['httpStatus'] == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            elif check_response['meta']['httpStatus'] == '503 - Temporary Internal Server Error':
                raise Qualtrics503Error(
                    '503 - Temporary Internal Server Error')
            elif check_response['meta']['httpStatus'] == '504 - Gateway Timeout':
                raise Qualtrics504Error('504 - Gateway Timeout')
            elif check_response['meta']['httpStatus'] == '400 - Bad Request':
                raise Qualtrics400Error(
                    'Qualtrics Error\n(Http Error: 400 - Bad Request): There was something invalid about the request.')
            elif check_response['meta']['httpStatus'] == '401 - Unauthorized':
                raise Qualtrics401Error(
                    'Qualtrics Error\n(Http Error: 401 - Unauthorized): The Qualtrics API user could not be authenticated or does not have authorization to access the requested resource.')
            elif check_response['meta']['httpStatus'] == '403 - Forbidden':
                raise Qualtrics403Error(
                    'Qualtrics Error\n(Http Error: 403 - Forbidden): The Qualtrics API user was authenticated and made a valid request, but is not authorized to access this requested resource.')
        except (Qualtrics500Error, Qualtrics503Error, Qualtrics504Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            return print(e)
        else:
            download_headers, download_url = self.header_setup(
                content_type=True, xm=False, accept=False, path=f"imported-data-projects/{idp_id}/exports/{is_file}/file")
            download_headers['Accept'] = "application/octet-stream, application/json"
            print("headers:", download_headers)
            download_request = r.get(
                download_url, headers=download_headers, stream=True)
            print("download_request", download_request)
            return download_request

    def get_idp_data(self, idp_id=None, **kwargs):
        '''This function takes in the IDP ID and returns a CSV of all of the data within the IDP'''
        assert idp_id != None or self.idp_source_id != None, 'Hey There! You need to set an ID when you instantiate the class, or pass one when you make this call.'

        if idp_id == None:
            idp_id = self.idp_source_id
        elif self.idp_source_id == None:
            self.idp_source_id = idp_id

        dynamic_payload = {"format": 'csv'}
        valid_keys = [
            'formatDecimalAsComma',
            'limit',
            'newlineReplacement',
            'timeZone',
            'useLabels',
            'startDate',
            'endDate',
            'sortByLastModifiedDate',
            'fields'
        ]

        for key in list(kwargs.keys()):
            assert key in valid_keys, "Hey There! You can only send valid parameters: ['formatDecimalAsComma', 'limit', 'newlineReplacement', 'timeZone', 'useLabels', 'startDate', 'endDate', 'sortByLastModifiedDate', 'fields' ]"
            if key == 'formatDecimalAsComma':
                assert isinstance(
                    kwargs['formatDecimalAsComma'], bool), "Hey there! formatDecimalAsComma must be a boolean"
                dynamic_payload.update({'formatDecimalAsComma': kwargs[(key)]})
            elif key == 'limit':
                assert isinstance(
                    kwargs[key], int), "Hey there! limit must be an integer"
                assert kwargs[key] > 0, "Hey there! limit must be greater than zero"
                dynamic_payload.update({'limit': kwargs[key]})

            elif key == 'newlineReplacement':
                assert isinstance(
                    kwargs[key], str), "Hey there! newlineReplacement must be a string"
                dynamic_payload.update({'newlineReplacement': kwargs[key]})

            elif key == 'timeZone':
                assert isinstance(
                    kwargs[key], str), "Hey there! timeZone must be a string"
                dynamic_payload.update({'timeZone': kwargs[key]})

            elif key == 'useLabels':
                assert isinstance(
                    kwargs[key], bool), "Hey there! useLabels must be a boolean"
                dynamic_payload.update({'useLabels': kwargs[key]})

            elif key == 'startDate' or key == 'endDate':
                import re
                date_pattern = re.compile(
                    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
                assert isinstance(
                    kwargs[key], str), f"Hey there! {key} must be a string"
                assert date_pattern.match(
                    kwargs[key]), f"Hey there! {key} must be a date-string formatted 'YYYY-MM-DDThh:mm:ssZ'"
                dynamic_payload.update({key: kwargs[key]})

            elif key == 'sortByLastModifiedDate':
                assert isinstance(
                    kwargs[key], bool), "Hey there! sortByLastModifiedDate must be a boolean"
                dynamic_payload.update({'sortByLastModifiedDate': kwargs[key]})

            elif key == 'fields':
                assert isinstance(
                    kwargs[key], list), "Hey there! fields must be a list of strings"
                assert all(isinstance(
                    item, str) for item in kwargs[key]), "Hey there! all items in fields must be strings"
                dynamic_payload.update({'fields': kwargs[key]})

        download_request = self.send_get_file_request(
            idp_id=idp_id, payload=dynamic_payload)

        with zipfile.ZipFile(io.BytesIO(download_request.content)) as survey_zip:
            for s in survey_zip.infolist():
                df = pd.read_csv(survey_zip.open(s.filename))
                return df

## private functions below here ##

    def _validate_fields(self, fields):
        """
        Private method to validate the 'fields' parameter.

        :param fields: List of objects, each containing keys 'name' and 'type'.
        :type fields: list
        :raises AssertionError: If the fields are not valid.
        """
        valid_types = {"number", "number-set", "string",
                       "string-set", "open-text", "date-time", "multi-answer"}

        assert isinstance(fields, list), "fields must be a list."

        for field in fields:
            assert isinstance(
                field, dict), "Each element in fields must be a dictionary."
            assert set(field.keys()) == {
                "name", "type"}, "Each dictionary must contain exactly the keys: 'name' and 'type'."

            name = field.get("name")
            type_field = field.get("type")

            assert isinstance(
                name, str) and name, "name must be a non-empty string."
            assert isinstance(
                type_field, str) and type_field in valid_types, f"type must be one of {valid_types}."

    def _validate_single_record(self, record):
        assert isinstance(record, dict), "record must be a dictionary"

        for key, value in record.items():
            assert isinstance(key, str), "All keys must be strings"
            assert isinstance(value, (str, int, float)), (
                "All values must be either strings, integers, or floats"
            )
