class Error(Exception):
    '''Primary class for handling server-side and HTTP errors.'''
    pass

class MailingListIDError(Error):
    '''This Exception handles errors associated with the Mailing List Ids.'''
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class ContactIDError(Error):
    '''This Exception handles errors associated with Contact Ids.'''
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class ServerError(Error):
    '''This Exception handles errors associated with the HTTP responses.'''
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
