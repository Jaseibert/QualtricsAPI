import requests as r
import zipfile
import io
import json
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Exceptions import Qualtrics500Error, Qualtrics503Error, Qualtrics504Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error

class Responses(Credentials):
    '''This is a child class to the credentials class that gathers the survey responses from Qualtrics surveys'''

    def __init__(self):
        return

    def setup_request(self, file_format='csv', survey=None):
        ''' This method sets up the request and handles the setup of the request for the survey.'''

        assert survey != None, 'Hey There! The survey parameter cannot be None. You need to pass in a survey ID as a string into the survey parameter.'
        assert isinstance(survey, str) == True, 'Hey There! The survey parameter must be of type string.'
        assert len(survey) == 18, 'Hey there! It looks like your survey ID is a the incorrect length. It needs to be 18 characters long. Please try again.'
        assert survey[:3] == 'SV_', 'Hey there! It looks like your survey ID is incorrect. You can find the survey ID on the Qualtrics site under your account settings. Please try again.'

        headers, url = self.header_setup(content_type=True, xm=False, path='responseexports/')
        payload = {"format":" + file_format + '","surveyId":"' + survey +'"}
        request = r.request("POST", url, data=payload, headers=headers)
        response = request.json()
        try:
            progress_id = response['result']['id']
            return progress_id, url, headers
        except:
            print(f"ServerError:\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}")

    def send_request(self, file_format='csv', survey=None):
        '''This method sends the request, and sets up the download request.'''
        file = None
        progress_id, url, headers = self.setup_request(file_format=file_format, survey=survey)
        check_progress = 0
        progress_status = "in progress"
        while check_progress < 100 and (progress_status != "complete") and (file is None):
            check_url = url + progress_id
            check_response = r.request("GET", check_url, headers=headers)
            file = check_response.json()["result"]["file"]
            check_progress = check_response.json()["result"]["percentComplete"]
        download_url = url + progress_id + '/file'
        download_request = r.get(download_url, headers=headers, stream=True)
        return download_request

    def get_responses(self, survey=None):
        '''This function accepts the survey id, and returns the survey responses associated with that survey.

        :param survey: This is the id associated with a given survey.
        :return: a Pandas DataFrame
        '''
        download_request = self.send_request(file_format='csv', survey=survey)
        with zipfile.ZipFile(io.BytesIO(download_request.content)) as survey_zip:
            for s in survey_zip.infolist():
                df = pd.read_csv(survey_zip.open(s.filename))
                return df

    def get_questions(self, survey=None):
        '''This method returns a DataFrame containing the survey questions and the Question IDs.

        :param survey: This is the id associated with a given survey.
        :return: a Pandas DataFrame
        '''
        df = self.get_responses(survey=survey)
        questions = pd.DataFrame(df[:1].T)
        questions.columns = ['Questions']
        return questions

    def setup_request_v3(self, survey=None, payload=None):
        ''' This method sets up the request and handles the setup of the request for the survey.'''

        assert survey != None, 'Hey There! The survey parameter cannot be None. You need to pass in a survey ID as a string into the survey parameter.'
        assert isinstance(survey, str) == True, 'Hey There! The survey parameter must be of type string.'
        assert len(survey) == 18, 'Hey there! It looks like your survey ID is a the incorrect length. It needs to be 18 characters long. Please try again.'
        assert survey[:3] == 'SV_', 'Hey there! It looks like your survey ID is incorrect. You can find the survey ID on the Qualtrics site under your account settings. Please try again.'

        headers, url = self.header_setup(content_type=True, xm=False, path=f'surveys/{survey}/export-responses/')
        request = r.request("POST", url, data=json.dumps(payload), headers=headers)
        response = request.json()
        try:
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
        except (Qualtrics500Error, Qualtrics503Error, Qualtrics504Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            return print(e)
        else: 
            progress_id = response['result']['progressId']
            return progress_id, url, headers
        
            
    def send_request_v3(self, survey=None, payload=None):
        '''This method sends the request, and sets up the download request.'''
        is_file = None
        progress_id, url, headers = self.setup_request_v3(survey=survey, payload=payload)
        progress_status = "in progress"
        while progress_status != "complete" and progress_status != "failed" and is_file is None:
            check_url = url + progress_id
            check_request = r.request("GET", check_url, headers=headers)
            check_response = check_request.json()
            try:
                is_file = check_response["result"]["fileId"]
            except KeyError:
                pass
            progress_status = check_response["result"]["status"]
        try:
            if check_response['meta']['httpStatus'] == '500 - Internal Server Error':
                raise Qualtrics500Error('500 - Internal Server Error')
            elif check_response['meta']['httpStatus'] == '503 - Temporary Internal Server Error':
                raise Qualtrics503Error('503 - Temporary Internal Server Error')
            elif check_response['meta']['httpStatus'] == '504 - Gateway Timeout':
                raise Qualtrics504Error('504 - Gateway Timeout')
            elif check_response['meta']['httpStatus'] == '400 - Bad Request':
                raise Qualtrics400Error('Qualtrics Error\n(Http Error: 400 - Bad Request): There was something invalid about the request.')
            elif check_response['meta']['httpStatus'] == '401 - Unauthorized':
                raise Qualtrics401Error('Qualtrics Error\n(Http Error: 401 - Unauthorized): The Qualtrics API user could not be authenticated or does not have authorization to access the requested resource.')
            elif check_response['meta']['httpStatus'] == '403 - Forbidden':
                raise Qualtrics403Error('Qualtrics Error\n(Http Error: 403 - Forbidden): The Qualtrics API user was authenticated and made a valid request, but is not authorized to access this requested resource.')
        except (Qualtrics500Error, Qualtrics503Error, Qualtrics504Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            return print(e)
        else: 
            download_url = url + is_file + '/file'
            download_request = r.get(download_url, headers=headers, stream=True)
            return download_request

    def get_survey_responses(self, survey=None, **kwargs):
        '''This function accepts the survey id, and returns the survey responses associated with that survey.
        
        :param survey: This is the id associated with a given survey.
        :return: a Pandas DataFrame
        '''
        dynamic_payload = {"format": 'csv'}
        for key in list(kwargs.keys()):
            assert key in ['useLabels', 'includeLabelColumns', 'exportResponsesInProgress', 'limit', 'seenUnansweredRecode', 'multiselectSeenUnansweredRecode', 'includeDisplayOrder'], "Hey there! You can only pass in parameters with names in the list, ['useLabels', 'includeLabelColumns', 'exportResponsesInProgress', 'limit', 'seenUnansweredRecode', 'multiselectSeenUnansweredRecode', 'includeDisplayOrder']"
            if key == 'useLabels':
                assert kwargs['includeLabelColumns'] is None, 'Hey there, you cannot pass both the "includeLabelColumns" and the "useLabels" parameters. Please pass just one and try again.'
                assert isinstance(kwargs['useLabels'], bool), 'Hey there, your "useLabels" parameter needs to be of type "bool"!'
                dynamic_payload.update({'useLabels': kwargs[(key)]})
            elif key == 'exportResponsesInProgress':
                assert isinstance(kwargs['exportResponsesInProgress'], bool), 'Hey there, your "exportResponsesInProgress" parameter needs to be of type "bool"!'
                dynamic_payload.update({'exportResponsesInProgress': kwargs[(key)]})
            elif key == 'limit':
                assert isinstance(kwargs['limit'], int), 'Hey there, your "limit" parameter needs to be of type "int"!'
                dynamic_payload.update({'limit': kwargs[(key)]})
            elif key == 'seenUnansweredRecode':
                assert isinstance(kwargs['seenUnansweredRecode'], str), 'Hey there, your "seenUnansweredRecode" parameter needs to be of type "str"!'
                dynamic_payload.update({'seenUnansweredRecode': kwargs[(key)]})
            elif key == 'multiselectSeenUnansweredRecode':
                assert isinstance(kwargs['multiselectSeenUnansweredRecode'], str), 'Hey there, your "multiselectSeenUnansweredRecode" parameter needs to be of type "str"!'
                dynamic_payload.update({'multiselectSeenUnansweredRecode': kwargs[(key)]})
            elif key == 'includeLabelColumns':
                assert isinstance(kwargs['includeLabelColumns'], bool), 'Hey there, your "includeLabelColumns" parameter needs to be of type "bool"!'
                assert kwargs['useLabels'] is None, 'Hey there, you cannot pass both the "includeLabelColumns" and the "useLabels" parameters. Please pass just one and try again.'
                dynamic_payload.update({'includeLabelColumns': kwargs[(key)]})
        print(dynamic_payload)
        download_request = self.send_request_v3(survey=survey, payload=dynamic_payload)
        with zipfile.ZipFile(io.BytesIO(download_request.content)) as survey_zip:
            for s in survey_zip.infolist():
                df = pd.read_csv(survey_zip.open(s.filename))
                return df

    def get_survey_questions(self, survey=None):
        '''This method returns a DataFrame containing the survey questions and the Question IDs.

        :param survey: This is the id associated with a given survey.
        :return: a Pandas DataFrame
        '''
        df = self.get_survey_responses(survey=survey, limit=2)
        questions = pd.DataFrame(df[:1].T)
        questions.columns = ['Questions']
        return questions

