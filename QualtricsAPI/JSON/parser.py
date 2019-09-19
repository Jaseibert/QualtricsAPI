import numpy as np

class Parser(object):

    def __init__(self):
        return

    def extract_values(self, obj=None, key=None):
        ''' This outer method  a specific value from a nested dictionary.

        :param obj: a dictionary object.
        :param key: The Specific Key that the value is associated with.
        :return: the value associated with the given key
        '''
        values = []
        def extract(obj, values, key):
            '''This inner method recursively searches for the given key in a nested dictionary. (Not a User-Facing Method)

            :param obj: a dictionary object.
            :param values: a list that will house the values of the given key.
            :param key: The Specific Key that the value is associated with.
            :return: the value associated with the given key
            '''
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, values, key)
                    elif k == key:
                        values.append(v)
            elif isinstance(obj, list):
                for j in obj:
                    extract(j, values, key)
            return values
        results = extract(obj, values, key)
        return results

    def extract_keys(self, obj):
        '''This outer method extracts all of the keys from a nested dictionary.

        :param obj: a dictionary object.
        :return: a list of keys within a given dictonary.
        '''
        keys = []

        def extract(obj, keys):
            '''This inner method recursively locates each of the keys within a nested dictionary.

            :param obj: a dictionary object.
            :param keys: a list of previously identified keys
            :return: a list of keys within a given recursion of the inner method.
            '''
            if isinstance(obj, dict):
                for k,v in obj.items():
                    if isinstance(v, (dict, list)):
                        keys.append(k)
                        extract(v, keys)
                    else:
                        keys.append(k)
            elif isinstance(obj, list):
                for element in obj:
                    extract(element, keys)
            return keys
        obj_keys =  extract(obj, keys)
        return obj_keys

    def json_parser(self, response=None, keys=[], arr=True):
        '''This method itterates over the all of the keys within a keys list.'''

        #Improvement: Include the Extract keys method in this method.
        elements  = [self.extract_values(response, item) for item in keys]
        if arr == True:
            return np.array(elements).T
        else:
            return elements
