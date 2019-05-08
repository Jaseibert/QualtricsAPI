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

    def extract_keys(self, obj):
        '''Extract all of the keys from a dictionary.'''
        keys = []

        def extract(obj, keys):
            '''Recursively identify each of the keys within a dictionary.'''
            if isinstance(obj, dict):
                for k,v in obj.items():
                    if isinstance(v, (dict)):
                        keys.append(k)
                        extract(v, keys)
                    else:
                        keys.append(k)
            return keys
        obj_keys = extract(obj, keys)
        return obj_keys

    def json_parser(self, response=None, keys=[], arr=True):
        '''This method returns the JSON as either a NumPy Array or the element itself.'''
        elements  = [self.extract_values(response, item) for item in keys]
        if arr == True:
            return np.array(elements).T
        else:
            return elements
