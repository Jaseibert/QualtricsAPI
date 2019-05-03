import numpy as np
import os

class Credentials(object):

    def __init__(self):
        return

    def qualtrics_api_credentials(self, token=None, data_center=None, directory_id=None):
        os.environ['token'] = token
        os.environ['data_center'] = data_center
        os.environ['directory_id'] = directory_id
        return

    def header_setup(self,content_type=False,responses=True):
        '''This function accepts the argument content_type and returns the correct header, and base url.

        :param content_type: use to return json response.
        :return: a HTML header and base url.
        '''
        header = {"x-api-token": os.environ['token']}
        path = 'directories/{0}/'.format(os.environ['directory_id']) if responses else 'responseexports/'
        base_url = f"https://{os.environ['data_center']}.qualtrics.com/API/v3/{path}"
        if content_type is True:
            header["Content-Type"] = "application/json"
        else:
            pass
        return header, base_url
