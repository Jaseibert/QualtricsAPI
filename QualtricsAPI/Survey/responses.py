import requests as r
import zipfile
import json
import io
import glob

class Responses(object):

    def __init__(self, token=None, survey_id=None, file_format=None, data_center=None, export_type='LegacyV3'):
        self.token = str(token)
        self.survey_id = str(survey_id)
        self.file_format = str(file_format)
        self.data_center = str(data_center)
        self.export_type = str(export_type)
        return

    def setup_request(self, file_format='csv', survey_id=None):
        '''This function accepts the argument content_type and returns the correct header, and base url.

        :param content_type: use to return json response.
        :return: a HTML header and base url.
        '''
        headers, url = self.header_setup(self,content_type=True,responses=True)
        payload = '{"format":"' + str(file_format) + '","surveyId":"' + str(survey_id) + '"}'
        response = r.request("POST", url, data=payload, headers=headers)
        progress_id = response.json()['result']['id']
        return progress_id, url, headers

    def send_request(self, file_format='csv', survey_id=None):
        ''''''
        file = None
        progress_id, url, headers = self.setup_request(file_format=file_format, survey_id=survey_id)
        check_progress = 0
        progress_status = "in progress"
        while check_progress < 100 and progress_status is not "complete" and file is None:
            check_url = url + progress_id
            check_response = r.request("GET", check_url, headers=headers)
            file = check_response.json()["result"]["file"]
            if file is None:
                print ("file not ready")
            else:
                print ("file created:", check_response.json()["result"]["file"])
            check_progress = check_response.json()["result"]["percentComplete"]
            print("Download is " + str(check_progress) + " complete")
        download_url = url + progress_id + '/file'
        download_request = r.request("GET", download_url, headers=headers, stream=True)
        return download_request

    def get_responses(self, file_format='csv', survey_id):
        ''''''
        download_request = self.send_request(file_format=file_format, survey_id=survey_id)
        zipfile.ZipFile(io.BytesIO(download_request.content)).extractall("SurveyResponses")
        print('The folder "{0}" has been created with your survey responses stored inside.'.format(folder_name))
        #Add Logic to open the file as a dataFrame
