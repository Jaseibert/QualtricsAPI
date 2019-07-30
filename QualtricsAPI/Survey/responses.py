import requests as r
import zipfile
import json
import io
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Exceptions import ServerError

class Responses(Credentials):
    '''This is a child class to the credentials class that gathers the survey responses from Qualtrics surveys'''

    def __init__(self):
        return

    def setup_request(self, file_format='csv', survey_id=None):
        ''' This method sets up the request and handles the setup of the request for the survey.'''

        assert len(survey_id) == 18, 'Hey there! It looks like your survey ID is a the incorrect length. It needs to be 18 characters long. Please try again.'
        assert survey_id[:3] == 'SV_', 'Hey there! It looks like your survey ID is incorrect. You can find the survey ID on the Qualtrics site under your account settings. Please try again.'

        try:
            headers, url = self.header_setup(content_type=True, responses=False)
            payload = '{"format":"' + file_format + '","surveyId":"' + survey_id + '"}'
            request = r.request("POST", url, data=payload, headers=headers)
            response = request.json()
            progress_id = response['result']['id']
            return progress_id, url, headers
        except ServerError:
            print(f"ServerError:\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}", s.msg)

    def send_request(self, file_format='csv', survey_id=None):
        '''This method sends the request, and sets up the download request.'''
        try:
            file = None
            progress_id, url, headers = self.setup_request(file_format=file_format, survey_id=survey_id)
            check_progress = 0
            progress_status = "in progress"
            while check_progress < 100 and progress_status is not "complete" and file is None:
                check_url = url + progress_id
                check_response = r.request("GET", check_url, headers=headers)
                file = check_response.json()["result"]["file"]
                check_progress = check_response.json()["result"]["percentComplete"]
            download_url = url + progress_id + '/file'
            download_request = r.get(download_url, headers=headers, stream=True)
        except ServerError as s:
            print(f"ServerError:\nError Code: {content['meta']['error']['errorCode']}\nError Message: {content['meta']['error']['errorMessage']}", s.msg)
        return download_request

    def get_responses(self, survey_id=None):
        '''This function accepts the file format, and the survey id, and returns the responses associated with that survey.

        :param survey_id: the id associated with a given survey.
        :return: a Pandas DataFrame with the responses
        '''

        download_request = self.send_request(file_format='csv', survey_id=survey_id)
        with zipfile.ZipFile(io.BytesIO(download_request.content)) as survey_zip:
            for s in survey_zip.infolist():
                df = pd.read_csv(survey_zip.open(s.filename))
                return df


    def get_questions(self, survey_id=None):
        '''This method returns a DataFrame containing the Survey questions and the QuestionIDs.

        :param survey_id:
        :return: a DataFrame with the Surveys questions
        '''

        df = self.get_responses(survey_id=survey_id)
        questions = pd.DataFrame(df[:1].T)
        questions.columns = ['Questions']
        return questions


    #Method to List Surveys
