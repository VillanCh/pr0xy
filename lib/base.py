#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Base Class
  Created: 2016/12/6
"""

import unittest
import abc
import types

########################################################################
class PluginBaseClass(object):
    """"""

    __metaclass__ = abc.ABCMeta

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
    
        
    #----------------------------------------------------------------------
    @abc.abstractproperty
    def name(self):
        """"""
        return '...'

    #----------------------------------------------------------------------
    @abc.abstractproperty    
    def description(self):
        """"""
        return '...'
    
    #----------------------------------------------------------------------
    @abc.abstractmethod    
    def _work(self, *args, **kwargs):
        """"""
        return '...'
        
    #----------------------------------------------------------------------
    @abc.abstractmethod    
    def _parse_result(self, result):
        """"""
        return "..."

    #----------------------------------------------------------------------
    def start(self, *args, **kwargs):
        """"""
        #print 'cl'
        ret = self._work(*args, **kwargs)
        #SOMETHING IF NEEDED
        return self._parse_result(ret)

#abc.ABCMeta.register(PluginBaseClass)
########################################################################
class Demo(PluginBaseClass):
    """"""

    pass
    
    

########################################################################
class BaseClassTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def runTest(self):
        """"""
        print 'sss'
        BaseClassTest()
        Demo()
    
    

if __name__ == '__main__':
    unittest.main()