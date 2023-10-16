# -*- coding: utf-8 -*-

class TreeError(Exception):
    def __init__(self,value):
        self.value = 'Tree error: '+value
    def __str__(self):
        return repr(self.value)

class InvalidPattern(Exception):
    def __init__(self,value):
        self.value = 'Invalid pattern: '+value
    def __str__(self):
        return repr(self.value)
