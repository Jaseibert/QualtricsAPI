import requests as r
import json
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Exceptions import Qualtrics500Error, Qualtrics503Error, Qualtrics504Error, Qualtrics400Error, Qualtrics401Error, Qualtrics403Error

class Surveys(Credentials):
    '''This is a child class to the credentials class that handles survey functionality for the authenticated user.'''

    def __init__(self):
        return

    def list_user_surveys(self):
        '''This method provides functionality to share a survey within a given brand/organization.

        :return: a Pandas DataFrame with the user's available surveys.
        '''
        surveys = pd.DataFrame(columns=['id', 'name', 'ownerId', 'lastModified', 'creationDate', 'isActive', 'nextPage'])
        headers, url = self.header_setup(content_type=False, xm=False, path='surveys')
      
        def extract_page(surveys=surveys, url=url):
            ''' This method is a nested method that extracts a single page of surveys. '''
            try:
                request = r.get(url, headers=headers)
                response = request.json()
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
            except (Qualtrics500Error, Qualtrics503Error):
                t.sleep(0.25)
                extract_page(surveys=surveys, url=url)
            except Qualtrics504Error:
                t.sleep(5)
                extract_page(surveys=surveys, url=url)
            except (Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
                print(e)
            except:
                t.sleep(10)
                extract_page(surveys=surveys, url=url)
            else:
                keys = ['id', 'name', 'ownerId', 'lastModified', 'creationDate', 'isActive']
                lists = Parser().json_parser(response=response, keys=keys, arr=False)
                single_page = pd.DataFrame(lists).transpose()
                single_page.columns = keys
                surveys = pd.concat([surveys, single_page]).reset_index(drop=True)
                next_page = response['result']['nextPage']
                return surveys, next_page

        surveys, next_page = extract_page(surveys=surveys, url=url)

        if next_page is None:
              return surveys
        else:
            while next_page is not None:
              surveys, next_page = extract_page(surveys=surveys, url=next_page)
            return surveys

    def share_user_surveys(self, survey=None, recipient_id=None, permissions={}):
        '''This method provides functionality to share a survey within a given brand/organization.

        :param survey: the name of the list to be created.
        :param recipient_id: the group/user qualtrics id
        :param permissions: an object of permission properties.
        :return: A message on HTTP-200 Success
        '''
        
        assert survey != None, 'Hey there! The survey parameter cannot be None.'
        assert isinstance(survey, str) == True, 'Hey there! The survey parameter must be of type string.'
        assert recipient_id != None, 'Hey there! The recipient parameter cannot be None.'
        assert isinstance(recipient_id, str) == True, 'Hey there! The recipient parameter must be of type string.'
        assert permissions != None, 'Hey there! The permissions parameter cannot be None.'
        assert isinstance(permissions, dict) == True, 'Hey there! The permissions parameter must be of type dict.'

        headers, url = self.header_setup(content_type=False, xm=False, path=f'surveys/{survey}/permissions/collaborations')
        data = {
          'recipientId': recipient_id, 
          'permissions': permissions
        }
        try:
            request = r.post(url, json=data, headers=headers)
            response = request.json()
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
        except (Qualtrics500Error, Qualtrics503Error, Qualtrics504Error) as e:
            # Recursive call to handle Internal Server Errors
            return self.share_user_surveys(survey=survey, recipient_id=recipient_id, permissions=permissions)
        except (Qualtrics400Error, Qualtrics401Error, Qualtrics403Error) as e:
            # Handle Authorization/Bad Request Errors
            return print(e)
        else:
            return f'The survey "{survey}" was shared with the user/group "{recipient_id}"'