import numpy as np
import os

class Credentials(object):
    ''' This class handles the setup of credentials needed to setup the Qualtrics API Authorization.'''

    def __init__(self):
        return

    def qualtrics_api_credentials(self, token=None, data_center=None, directory_id=None):
        '''This method creates enviornment variables for the users Qualtrics API token, data center, and their directory id.

        :param token: your Qualtrics API Token
        :param data_center: your Qualtrics data center
        :param directory_id: your Qualtrics directory id
        :return: Nothing, but you've create enviornment variables for each parameter.
        '''
        #Add Length Logic for Token and Directory Id
        os.environ['token'] = token
        os.environ['data_center'] = data_center
        os.environ['directory_id'] = directory_id
        return

    def header_setup(self,content_type=False,responses=True):
        '''This method accepts the argument content_type and returns the correct header, and base url. (Not a User-Facing Method)

        :param content_type: use to return json response.
        :return: a HTML header and base url.
        '''
        header = {"x-api-token": os.environ['token']}
        path = 'directories/{0}/'.format(os.environ['directory_id']) if responses else 'responseexports/'
        base_url = f"https://{os.environ['data_center']}.qualtrics.com/API/v3/{path}"
        if content_type is True:
            header["Content-Type"] = "application/json"
        return header, base_url
