#!/usr/bin/env python3
class _BUILDENUM(object):
    '''
     @ClassDesc: class to create attribute-holding object from key-value pairs
    '''

    def __init__(self, **kwargs):
        '''
         @Desc: _BUILDENUM constructor
         @Params: **kwargs - series of key-value pairs | double-pointer dictionary object
        '''
        for k, v in kwargs.items():
            setattr(self, k, v)

    def addattr(self, name, value):
        '''
         @Desc: function to add additional attributes to object
         @Params: name - attribute retrieval key, value - attribute value 
        '''
        setattr(self, name, value)


class ENUM(_BUILDENUM):
    '''
     @ClassDesc:    class to create attribute-holding object from dictionary
                    inherits from _BUILDENUM class
    '''

    def __init__(self, attributes):
        '''
         @Desc: ENUM constructor
         @Params: attributes - dictionary object
        '''
        _BUILDENUM.__init__(self, **attributes)
