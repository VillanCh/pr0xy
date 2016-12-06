#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Parse Target
  Created: 2016/11/11
"""

import unittest
import re
import IPy
from IPy import IP
PORTS = ['80', '8080', '8123', '3128', '82']


#----------------------------------------------------------------------
def generate_target(IPs, ports):
    """Generate the target for scanning HTTP proxy"""
    
    gen = None
    if '-' in IPs:
        pairs = IPs.split('-')
        start = pairs[0]
        end = pairs[1]
        gen = int2ips(IP(start).int(), IP(end).int())
    else:
        gen = IP(IPs)
        
    for i in gen:
        for port in ports:
            if isinstance(port, int):
                port = str(port)
            yield ':'.join([i.__str__(), port])
        
#----------------------------------------------------------------------
def int2ips(start, end):
    """"""
    for i in xrange(int(start), int(end)):
        yield IPy.intToIp(i, version=4)
    
    


########################################################################
class ParseTargetTest(unittest.case.TestCase):
    """Test Parse Target"""

    #--------------------------------------------------------------
    def runTest(self):
        IPs_1 = '123.1.2.0/24'
        IPs_2 = '123.1.2.3-123.1.3.5'
        ip_gen = generate_target(IPs_1, PORTS)
        for i in ip_gen:
            ip_port = i.split(':')
            print ip_port
            try:
                IPy.IP(ip_port[0])
            except ValueError:
                pass
            
        ip_gen = generate_target(IPs_2, PORTS)
        for i in ip_gen:
            ip_port = i.split(':')
            print ip_port
            try:
                IPy.IP(ip_port[0])
            except ValueError:
                pass        
    

if __name__ == '__main__':
    unittest.main()