'''
These HTTP Errors are defined by Qualtrics. Documentation can be found 
(https://api.qualtrics.com/instructions/docs/Instructions/responses.md)

'''

class Qualtrics400Error(Exception):
    '''This Exception handles errors associated with the HTTP 400 (Bad Request) responses.'''
    def __init__(self, msg):
        super().__init__(msg)

class Qualtrics401Error(Exception):
    '''This Exception handles errors associated with the HTTP 401 (Unauthorized) responses.'''
    def __init__(self, msg):
        super().__init__(msg)

class Qualtrics403Error(Exception):
    '''This Exception handles errors associated with the HTTP 403 (Forbidden) responses.'''
    def __init__(self, msg):
        super().__init__(msg)

class Qualtrics429Error(Exception):
    '''This Exception handles errors associated with the HTTP 429 (Too Many Requests) responses.'''
    def __init__(self, msg):
        super().__init__(msg)

class Qualtrics500Error(Exception):
    '''This Exception handles errors associated with the HTTP 500 (Internal Server Error) responses.'''
    def __init__(self, msg):
        super().__init__(msg)

class Qualtrics503Error(Exception):
    '''This Exception handles errors associated with the HTTP 503 (Temporary Internal Server Error) responses.'''
    def __init__(self, msg):
        super().__init__(msg)

class Qualtrics504Error(Exception):
    '''This Exception handles errors associated with the HTTP 504 (Gateway Timeout) responses.'''
    def __init__(self, msg):
        super().__init__(msg)