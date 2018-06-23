UNCAUGHT = "uncaught exception"
UNKNOWN = "unknown error occured"

class missing_config(Exception):
    def __init__(self, error_msg="missing_config"):
        Exception.__init__(self, error_msg)

def get_exception(msg="", trace=False):
    '''
     @Desc: function to retrieve and prettyprint errortype/ stacktrace
     @Params: msg - additional error message, trace - boolean to toggle stacktrace presence
     @Return: dictionary object containing relevant error information
    '''
    import sys, traceback
    exc_type, exc_val, exc_tb = sys.exc_info()
    tb = traceback.format_tb(exc_tb)
    _exception = {
        "exception": {
            "type": exc_type,
            "value": exc_val
        }
    }
    if msg:
        _exception.update({"description": msg})
    if trace:
        _exception.update({"traceback": tb})
    return _exception