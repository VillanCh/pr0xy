#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Pr0xy Main
  Created: 2016/12/6
"""

import types
import time
import json
import os
import sys
import unittest
import argparse
import traceback
from Queue import Empty
from pprint import pprint
 

from lib.utils import Pool
from lib import parse_target
from lib.check_proxy import CheckProxy, CheckProxyPlugin


SCAN_TYPE_TABLE = {
    'proxy': {'module':'lib.check_proxy',
              'plugin_class':'CheckProxyPlugin'}
}

#----------------------------------------------------------------------
def parse_args():
    """"""
    parser = argparse.ArgumentParser(description='Pr0xy Scan and collect proxy info')
    parser.add_argument('IP', 
                        help='''The IP you want to check: \nINPUT format:\ 1.2.3.4-1.2.5.6 or 45.67.89.0/24 or 
                        45.78.1.48''')
    parser.add_argument('--ports', dest='ports',
                        help='The ports you want to check, Plz input single port\
                        or with a format like: 82,80 or 100-105')
    parser.add_argument('--type', dest='type',
                        help='Type of scan [Now Just Support proxy]')

    args = parser.parse_args()
    args.IP
    #print args.ports
    #pprint(args)
    PORTS = []
    raw_ports = args.ports
    if '-' in raw_ports:
        _ = raw_ports.split('-')
        _min = _[0]
        _max = _[1]
        PORTS = range(_min, _max)
    elif ',' in raw_ports:
        _list = raw_ports.split(',')
        for _ in _list:
            if _.isdigit():
                PORTS.append(int(_))
            else:
                pass
        #PORTS.append(object)
        if PORTS == []:
            PORTS = parse_target.PORTS
    else:
        if raw_ports.isdigit():
            PORTS.append(int(raw_ports))
        else:
            PORTS = parse_target.PORTS

    #pprint(args.IP)
    #pprint(PORTS)  
    return (args.IP, PORTS, args.type)


#----------------------------------------------------------------------
def process_result(results):
    """"""
    if isinstance(results, types.GeneratorType):
        for result in results:
            #pprint('')
            if result['result']:
                pprint('Success! %s' % result['from'] )
                os.system('echo %s >> success.txt' % json.dumps(result['proxy']))
            else:
                pprint('Failed!  %s' % result['from'] )
                os.system('echo %s >> failed.txt' % result['from'])
    else:
        result = results
        if result['result']:
            pprint('Success! %s' % result['from'] )
            os.system('echo %s >> success.txt' % json.dumps(result['proxy']))
        else:
            pprint('Failed!  %s' % result['from'] )
            os.system('echo %s >> failed.txt' % result['from'])        


#----------------------------------------------------------------------
def get_pluginclass(type_name):
    """"""
    try:
        try:
            plugin_class_path = SCAN_TYPE_TABLE[type_name]
        except KeyError:
            pprint('[!] No Such Type')
            exit()
        module_name = plugin_class_path['module']
        plugin_class_name = plugin_class_path['plugin_class']
        module_tmp = __import__(module_name, fromlist=plugin_class_name)
        ret = getattr(module_tmp, plugin_class_name)
        return ret
    except Exception, E:
        traceback.format_exc()
        exit()


#----------------------------------------------------------------------
def main():
    """Pr0xy main"""
    params = parse_args()
    IP = params[0]
    PORTS = params[1]
    pool = Pool()
    
    plugin_class = get_pluginclass(params[2])
    
    for target in parse_target.generate_target(IP, PORTS):
        _ = plugin_class(target)
        pool.add_task(_.start)
    
    result_queue = pool.run()
    while True:
        try:
            ret = result_queue.get(timeout=0.3)
            process_result(ret)
        except Empty:
            pass
        except KeyboardInterrupt:
            pprint('ByeByeBye')

if __name__ == '__main__':
    main()