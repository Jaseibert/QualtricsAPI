import numpy as np

class Parser(object):

    def __init__(self):
        return

    def extract_values(self, obj, key):
        """Pull all values of specified key from nested JSON."""
        arr = []

        def extract(obj, arr, key):
            """Recursively search for values of key in JSON tree."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif k == key:
                        arr.append(v)
            elif isinstance(obj, list):
                for j in obj:
                    extract(j, arr, key)
            return arr
        results = extract(obj, arr, key)
        return results

    def json_parser(self, response, keys=[]):
        ''' '''
        elements  = [self.extract_values(response, item) for item in keys]
        return np.array(elements).T
