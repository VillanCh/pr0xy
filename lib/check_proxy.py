#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<VillanCH>
  Purpose: check proxy available
  Created: 2016/10/31
"""

import unittest
import requests
from pprint import pprint

from base import PluginBaseClass


########################################################################
class CheckProxyPlugin(PluginBaseClass):
    """"""
    
    _name = 'Check Proxy'
    _description = 'Check if the specific addr(IP:PORT) is a \
        HTTP(s) proxy'

    #----------------------------------------------------------------------
    def __init__(self, target):
        """"""
        self.target = target

    #----------------------------------------------------------------------
    @property    
    def name(self):
        """getter for self._name"""
        return self._name
    
    #----------------------------------------------------------------------
    @property    
    def description(self):
        """getter for self._description"""
        return self._description
    
    #----------------------------------------------------------------------
    def _work(self, *args, **kwargs):
        """"""
        #print 'called'
        ret = CheckProxy(self.target)
        return ret.test(timeout=int(kwargs['timeout']) if kwargs.has_key('timeout')
                       else 3)
        
    #----------------------------------------------------------------------    
    def _parse_result(self, result):
        """"""
        return result
        
        
    
    

########################################################################
class CheckProxy(object):
    """Check Proxy
    
    Attributes:
        target: A str, the target you want to check. 
                Example: 44.4.4.4:44"""

    #----------------------------------------------------------------------
    def __init__(self, target):
        """Constructor"""
        self.target = target
        self.ip = target.split(':')[0]
     
    #----------------------------------------------------------------------   
    def test(self, timeout=3):
        '''Test the self.target whether is a http proxy addr
        
        Returns:
            A dict: if the result is True:
            Example:
              {
                  'result':True,
                  'proxy':{
                      'http':'xxx.xxx.xxx.xx:port',
                      'https':'xxx.xxx.xxx.xx:port'
                   }
              }
            if the target isn' t the http proxy addr, 
            the result['proxy'] will be None
         '''
        result = {}
        result['result'] = False
        result['proxy'] = self._check_ip(timeout=timeout)
        result['from'] = self.target
        return result

    #----------------------------------------------------------------------
    def _check_ip(self, timeout):
        """Check IP return the proxy or None

        Returns:
            A dict or None: if the result is True(the addr can be a proxy)
                the result is the dict like {'http':'http://xx.xx.xx.xx:xx',
                                             'https':'https://xx.xx.xx.xx:xx'}
                And if the https proxy can't be used the key named 'https',
                Well, if the result is False(the addr can't be used as a proxy)
                the result is None"""

        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'

        check_ip_http = 'http://1212.ip138.com/ic.asp'
        check_ip_https = 'https://1212.ip138.com/ic.asp'

        addr_proxy = {}
        addr_proxy['http'] = 'http://' + self.target
        addr_proxy['https'] = 'https://' + self.target

        result = {}
        
        http_rsp = ''
        try:
            http_rsp = requests.get(check_ip_http, proxies=addr_proxy, timeout=timeout,
                                    headers=headers).text
        except:
            pass
        
        if self.ip in http_rsp:
            result['http'] = 'http://' + self.target
        
        https_rsp = ''
        try:
            https_rsp = requests.get(check_ip_https, proxies=addr_proxy,
                                     verify=False, timeout=timeout,
                                     headers=headers).text # close https verify
        except:
            pass
        
        if self.ip in https_rsp:
            result['https'] = 'https://' + self.target
            
        if result.has_key('http') or result.has_key('https'):
            return result
        else:
            return None

########################################################################
class CheckProxyTest(unittest.case.TestCase):
    """Test CheckProxy"""
    def test_check_ip(self):
        '''
        result should be
        {
	    'result':True,
	    'proxy':{
	        'http':'xxx.xxx.xxx.xx:port',
	        'https':'xxx.xxx.xxx.xx:port'
	    }
	}
        '''
        print 'API test'
        #创建想要测试的实例
        master = CheckProxy('78.6.5.45:8080')
        result = master.test(3)

        ##对结果进行测试
        #测试结果必须是个 dict 类型
        self.assertIsInstance(result, dict)
        #必须有一个 result 和 proxy 的键
        self.assertTrue(result.has_key('result'))
        self.assertTrue(result.has_key('proxy'))
        #result 键对应的值必须是一个 bool 类型
        self.assertIsInstance(result['result'], bool)        
        #断言测试 result['proxy'] 的类型
        if result['result']:
            self.assertIsInstance(result['proxy'], dict)
        else:
            self.assertIsNone(result['proxy'])
        print 'API test success!'

    def test_ip_check_function(self):
        '''test function'''
        print 'function test'
        
        #首先测试一个正确的实例（已知一定是个代理）
        addr = '122.96.59.105:82'
        master = CheckProxy(target=addr)
        result = master.test(timeout=3)

        #在前一个例子中我们验证了接口
        #那么在这里我们只需要验证一下
        #一定是完成了代理检测的，而且成功了
        proxy = result['proxy']
        #self.assertTrue(proxy.has_key('http'))
        
        print 'function test success!'
    def test_plugin_ins(self):
        ''''''
        pprint('Plugin Test')
        ret = CheckProxyPlugin()
        _result = ret.start('45.78.5.48:333')
        for _ in _result:
            pprint(ret.name)
            pprint(ret.description)
            pprint(_)
        
if __name__ == '__main__':
    unittest.main()
