import os, sys
import json
import errors

class Config(object):
    '''
     @ClassDesc: Configuration loader
    '''

    # static class variables
    BAD_PATH = "bad_path"
    NO_SUCH_KEY = "no_such_key"


    def __init__(self, config_path):
        '''
         @Desc: Config constructor
         @Params: config_path - string path to configuration file
        '''
        self.path = config_path if os.path.isfile(config_path) else self.BAD_PATH
        self.config = dict()
        with open(self.path, 'r') as jc:
            self.config = json.loads(jc.read())

    def get(self, key):
        '''
         @Desc: function to retrieve configuration value from key
         @Params: key - configuration retrieval key
         @Return: configuration value
        '''
        try:
            return self.config.get(key)
        except (KeyError, IndexError):
            return self.NO_SUCH_KEY
        except Exception:
            errors.get_exception(errors.UNKNOWN, trace=True)
        

    def get_dict(self,):
        '''
         @Desc: function to retrieve full configuration dictionary
         @Return: configuration dictionary
        '''
        if self.path == self.BAD_PATH:
            return self.BAD_PATH
        return self.config
