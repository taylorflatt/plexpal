#!/usr/bin/env python3
class Missing_Config(Exception):

    def __init__(self, error_msg="missing_config"):
        Exception.__init__(self, error_msg)


class Unhandled(Exception):

    def __init__(self, error_msg="unknown error occured"):
        Exception.__init__(self, error_msg)


class Uncaught(Exception):

    def __init__(self, error_msg="uncaught exception"):
        Exception.__init__(self, error_msg)


def get_exception(msg="", trace=False, text=False):
    '''
     @Desc: function to retrieve and prettyprint errortype/ stacktrace
     @Params: msg - additional error message, trace - boolean to toggle stacktrace presence
     @Return: dictionary object containing relevant error information
    '''
    import sys, traceback
    exc_type, exc_val, exc_tb = sys.exc_info()
    _exception = {"exception": {"type": exc_type, "value": exc_val}}
    if msg:
        _exception.update({"description": msg})
    if trace:
        tb = traceback.format_tb(exc_tb)
        _exception.update({"traceback": tb})
    if text:
        output = "exception:"
        if msg:
            output += "\n\tdescription: {0}".format(msg)
        for k, v in _exception.get("exception").items():
            output += "\n\t{0}: {1}".format(k, v)
        if trace:
            output += "\n\ttraceback: {0}".format(_exception.get("traceback"))
        return output

    return _exception
