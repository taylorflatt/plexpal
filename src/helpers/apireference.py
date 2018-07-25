#!/usr/bin/env python3
import os
import sys
import uuid

from src.helpers import errors
from src.helpers.errors import get_exception
from src.helpers.config import Config

# API Types
PLEX = "plex"
SONARR = "sonarr"
RADARR = "radarr"


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
        abs_dir_path = os.path.split(os.path.abspath(__file__))[0]
        computed_path = os.path.join(abs_dir_path, self.__config_path__)
        conf = Config(computed_path)
        self.reference = conf.get_dict()
        if self.reference == conf.BAD_PATH:
            raise errors.Missing_Config("Error - {0}: {1}".format(conf.BAD_PATH, self.__config_path__))

        # iterates configuration values and assigns them as object attributes
        for k, v in self.reference.get(api_type).items():
            if "<UUID>" in v:
                setattr(self, k, v.replace("<UUID>", uuid.uuid4()))
            else:
                setattr(self, k, v)
        try:
            if type(self.headers) is dict:
                for k, v in self.headers.items():
                    if "<UUID>" in v:
                        self.headers.update({k: uuid.uuid4()})
        except AttributeError:
            pass
        except Exception:
            raise errors.Unhandled("{0}".format(errors.get_exception(trace=True)))
