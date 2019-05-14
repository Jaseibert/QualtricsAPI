class Error(Exception):
    '''Primary class for handling server-side and HTTP errors.'''
    pass

class ServerError(Error):
    '''This Exception handles errors associated with the HTTP responses.'''
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
