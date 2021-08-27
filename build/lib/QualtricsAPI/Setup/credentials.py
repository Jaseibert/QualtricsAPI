import numpy as np
import os

class Credentials(object):
    ''' This class handles the setup of credentials needed to setup the Qualtrics API Authorization. Use the
    qualtrics_api_credentials method to create enviornment variables that will automatically populate the correct
    HTTP headers for the request that you are making. '''

    def __init__(self):
        return

    def qualtrics_api_credentials(self, token, data_center, directory_id=None):
        '''This method creates enviornment variables for the users Qualtrics API token, data center, and their directory id.

        :param token: Your Qualtrics API Token
        :type token: str
        :param data_center: Your Qualtrics data center
        :type data_center: str
        :param directory_id: Your Qualtrics directory id (XM Directory Users-Only)
        :type directory_id: str
        :return: Nothing explicitly, However you just create enviornment variables that will populate you HTTP Headers.
        '''
        assert len(token) == 40, 'Hey there! It looks like your api token is a the incorrect length. It needs to be 40 characters long. Please try again.'
        if directory_id: 
            assert len(directory_id) == 20, 'Hey there! It looks like your api directory ID is a the incorrect length. It needs to be 20 characters long. Please try again.'
            assert directory_id[:5] == 'POOL_', 'Hey there! It looks like your directory ID is incorrect. You can find the directory ID on the Qualtrics site under your account settings. Please try again.'
            os.environ['directory_id'] = directory_id

        os.environ['token'] = token
        os.environ['data_center'] = data_center
        return

    def header_setup(self, content_type=False, xm=True, path=None):
        '''This method accepts the argument content_type and returns the correct header, and base url. (Not a User-Facing Method)

        response => path = 'responseexports/'
        distributions => path = 'distributions'

        :param content_type: use to return json response.
        :return: a HTML header and base url.
        '''
        if xm:
            assert os.environ['directory_id'], 'Hey there! This endpoint is only accessible for XM Directory Users . If you have access to the XM Directory, then be sure to include your directory_id when you use the qualtrics_api_credentials() method. '
            path = 'directories/{0}/'.format(os.environ['directory_id']) if xm else path

        header = {"x-api-token": os.environ['token']}
        base_url = f"https://{os.environ['data_center']}.qualtrics.com/API/v3/{path}"
        if content_type is True:
            header["Content-Type"] = "application/json"
        return header, base_url
