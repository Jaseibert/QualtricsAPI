import requests as r
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.Exceptions import Qualtrics500Error, Qualtrics503Error, Qualtrics504Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error


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
