class Qualtrics500Error(Exception):
    '''This Exception handles errors associated with the HTTP 500 (BRE_0.2) responses.'''
    def __init__(self, msg):
        super().__init__(msg)
