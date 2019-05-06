class Error(Exception):
    '''Primary class for handling server-side and HTTP errors.'''
    pass

class APITokenError(Error):
    '''This Exception handles errors associated with the QualtricsAPI Token.'''
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

     def __str__(self):
        return str(self.message)

class DirectoryIDError(Error):
    '''This Exception handles errors associated with the Qualtrics Directory Id.'''
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

     def __str__(self):
        return str(self.message)

class DataCenterError(Error):
    '''This Exception handles errors associated with the Qualtrics Data Center.'''
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
        
    def __str__(self):
        return str(self.message)
