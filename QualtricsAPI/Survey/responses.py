import requests as r
import zipfile
import io
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser

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
        payload = '{"format":"' + file_format + '","surveyId":"' + survey +'"}'
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
