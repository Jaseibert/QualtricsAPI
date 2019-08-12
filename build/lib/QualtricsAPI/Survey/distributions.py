import requests as r
import zipfile
import json
import io
import pandas as pd
from QualtricsAPI.Setup import Credentials
from QualtricsAPI.JSON import Parser
from QualtricsAPI.Exceptions import ServerError

class Distributions(Credentials):
    '''This is a child class to the credentials class that gathers information about from Qualtrics Distributions.'''

    def __init__(self):
        return

    def get_distributions(self):
        return

    def list_distributions(self):
        return
