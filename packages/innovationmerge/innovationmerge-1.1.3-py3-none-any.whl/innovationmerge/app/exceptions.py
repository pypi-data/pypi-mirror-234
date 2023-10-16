# -*- coding: utf-8 -*-
class innovationmergeException(Exception):
    """Base class for exceptions raised by innovationmerge  modules"""


class innovationmergeMethodException(Exception):
    """Base class for exceptions raised by innovationmerge  modules"""
    def __init__(self, message):
        super().__init__(str(message))