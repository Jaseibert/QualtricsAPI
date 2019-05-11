import requests as r
import zipfile
import json
import io
import pandas as pd
import glob
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Exceptions import ServerError

class Responses(Credentials):
    '''This is a child class to the credentials class that gathers the survey responses from Qualtrics surveys'''

    def __init__(self):
        return

    def setup_request(self, file_format='csv', survey_id=None):
        '''  '''
        try:
            headers, url = self.header_setup(content_type=True, responses=False)
            payload = '{"format":"' + file_format + '","surveyId":"' + survey_id + '"}'
            request = r.request("POST", url, data=payload, headers=headers)
            response = request.json()
            progress_id = response['result']['id']
            return progress_id, url, headers
        except ServerError as s:
            print(f"ServerError:\nError Code: {response['meta']['error']['errorCode']}\nError Message: {response['meta']['error']['errorMessage']}", s.msg)
        except KeyError:
            print(f"ServerError:\nError Message: {response['meta']['error']['errorMessage']}")

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
        #try:
        download_request = self.send_request(file_format='csv', survey_id=survey_id)
        with zipfile.ZipFile(io.BytesIO(download_request.content)) as survey_zip:
            for s in survey_zip.infolist():
                df = pd.read_csv(survey_zip.open(s.filename))
                return df
        #except AssertionError as a:
            #assert len(survey_id) ==

    def get_questions(self, survey_id=None):
        '''This method returns a DataFrame containing the Survey questions and the QuestionIDs.

        :param survey_id:
        :return:
        '''
        df = self.get_responses(survey_id=survey_id)
        questions = pd.DataFrame(df[:1].T)
        questions.columns = ['Questions']
        return questions


    #Method to List Surveys
