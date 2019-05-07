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
        '''This function accepts the argument content_type and returns the correct header, and base url.

        :param content_type: use to return json response.
        :return: a HTML header and base url.
        '''
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
        ''''''
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
            download_request = r.get(download_url, headers=headers, stream=True).content
        except ServerError as s:
            print(f"ServerError:\nError Code: {content['meta']['error']['errorCode']}\nError Message: {content['meta']['error']['errorMessage']}", s.msg)
        return download_request

    def get_responses(self, file_format='csv', survey_id=None, ):
        '''This function accepts the file format, and the survey id, and returns the responses associated with that survey.

        :param file_format: the file format to be returned
        :param survey_id: the id associated with a given survey.
        :return: a HTML header and base url.
        '''

        download_request = self.send_request(file_format=file_format, survey_id=survey_id)
        file_stream = io.BytesIO(download_request)
        file_stream.seek(0)
        df = pd.read_table(file_stream, sep=',', index_col=False, encoding='utf-8')
        return df.head()



    #Method to List Surveys
