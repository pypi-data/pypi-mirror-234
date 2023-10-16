#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
_CHARACTORS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+|'


# decorator of sigleton
def singleton(clsname):
    instances = {}
    def getinstance(*args,**kwargs):
        if clsname not in instances:
            instances[clsname] = clsname(*args,**kwargs)
        return instances[clsname]
    return getinstance

class Constant(object):
    class ConstError(TypeError) : pass
    
    def __setattr__(self, key, value):
        if hasattr(self, key):
            raise self.ConstError("Can't rebind const (%s)" % key)
        setattr(self, key, value)


def random_string(len = 16):
    return ''.join(random.sample(_CHARACTORS, len))