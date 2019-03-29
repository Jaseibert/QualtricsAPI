import requests as r
import zipfile
import json
import io

class QualtricsSurveyResponses:

    def __init__(self, token=None, survey_id=None, file_format=None, data_center=None, export_type='LegacyV3'):
        self.token = str(token)
        self.survey_id = str(survey_id)
        self.file_format = str(file_format)
        self.data_center = str(data_center)
        self.export_type = str(export_type)
        return

    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
    }
    
    def url_and_payload_setup(self):
        ''''''
        if self.export_type == "LegacyV3":
            url = "https://{0}.qualtrics.com/API/v3/responseexports/".format(self.data_center)
            request_payload = '{"format":"' + self.file_format + '","surveyId":"' + self.survey_id + '"}'
        elif survey.export_type == "NewExport":
            url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(self.data_center, self.survey_id)
            request_payload = '{"format":"' + self.file_format + '"}'
        else:
            break
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
