import os, sys
from config import Config
import uuid

import errors

# API Types
PLEX    = "plex"
SONARR  = "sonarr"
RADARR  = "radarr"

class API(object):
    '''
     @ClassDesc: reference class for API parameters
    '''

    __config_path__ = "./config/api.conf"

    def __init__(self, api_type):
        '''
         @Desc:     API constructor
         @Params:   api_type - one of the provided api types, or string indicator
                    assigns class attributes based on configuration key-value pairs 
        '''
        conf = Config(self.__config_path__)
        self.reference = conf.get_dict()
        if self.reference == conf.BAD_PATH:
            raise errors.Missing_Config(
                "Error - {0}: {1}".format(conf.BAD_PATH, self.__config_path__)
            )

        # iterates configuration values and assigns them as object attributes
        for k, v in self.reference.items():
            if "<UUID>" in v:
                setattr(self, k, v.replace("<UUID>", uuid.uuid4()))
            else:
                setattr(self, k, v)
        try:
            if type(self.headers) is dict:
                for k, v in self.headers.items():
                    if "<UUID>" in v:
                        setattr(self, k, v.replace("<UUID>", uuid.uuid4()))
        except AttributeError:
            pass
        except Exception:
            raise errors.Unhandled(
                "{0}".format(errors.get_exception(trace=True))
            )