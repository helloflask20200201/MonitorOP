#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################
# Python API for Zabbix v1.0
#
# Author: frankyao @VIPS, Shanghai, China
# Email:  baniu.yao@gmail.com
# Date:   24, May, 2012
################################################
# Python3 version by 0312birdzhang
# Email: 0312birdzhang@gmail.com
# Date: 3,Nov,2015
################################################
try:
    import simplejson as json
except ImportError:
    import json

import requests
import subprocess
import logging

logger = logging.getLogger("MOP.Zabbix.API")

class ZabbixAPIException(Exception):
    pass

class ZabbixAPI(object):
    __auth = ''
    __id = 0
    _state = {}

    def __init__(self, url, user, password):
        self.__url = url.rstrip('/') + '/api_jsonrpc.php'
        self.__user = user
        self.__password = password
        self._zabbix_api_object_list = ('Action', 'Alert', 'APIInfo', 'Application', 'DCheck', 'DHost', 'DRule',
                'DService', 'Event', 'Graph', 'Graphitem', 'History', 'Host', 'Hostgroup', 'Hostinterface','Hostprototype','Httptest','Image', 'Item',
                'Maintenance', 'Map', 'Mediatype', 'Proxy', 'Screen', 'Script', 'Template', 'Trigger', 'User',
                'Usergroup', 'Usermacro', 'Usermedia')

    def __getattr__(self, name):
        '''
        判断对象是否正确
        实例化对象
        :param name: 操作对象名
        :return:
        '''
        if name not in self._zabbix_api_object_list:
            raise ZabbixAPIException('No such API object: %s' % name)
        if name not in self.__dict__:
            self.__dict__[name] = ZabbixAPIObjectFactory(self, name)
        return self.__dict__[name]

    def login(self):
        user_info = {'user': self.__user,
                     'password': self.__password}
        obj = self.json_obj('user.login', user_info)
        try:
            content = self.post_request(obj.encode(encoding='utf_8'))
        except requests.RequestException as e:
            logger.error("Zabbix URL Error")
            raise ZabbixAPIException("Zabbix URL Error")
        try:
            self.__auth = content['result']
        except KeyError as e:
            e = content['error']['data']
            logger.error(e)
            raise ZabbixAPIException(e)

    def is_login(self):
        return self.__auth != ''

    def __checkAuth__(self):
        if not self.is_login():
            raise ZabbixAPIException("NOT logged in")

    def json_obj(self, method, params):
        obj = {'jsonrpc': '2.0',
                'method': method,
                'params': params,
                'id': self.__id}
        if method != 'user.login':
            obj['auth'] = self.__auth

        logger.debug("####### obj start #######: \n{0} \n####### obj end #######".format(json.dumps(obj,indent=4)))
        return json.dumps(obj)

    def post_request(self, json_obj):
        headers = {'Content-Type': 'application/json-rpc',
                   'User-Agent': 'python/zabbix_api'}
        req = requests.post(url=self.__url, data=json_obj, headers=headers)
        content = json.loads(req.content)
        self.__id += 1
        return content

    '''
    /usr/local/zabbix/bin/zabbix_get is the default path to zabbix_get, it depends on the 'prefix' while install zabbix.
    plus, the ip(computer run this script) must be put into the conf of agent.
    '''
    @staticmethod
    def zabbix_get(ip, key):
        zabbix_get_command = subprocess.Popen('/usr/local/zabbix/bin/zabbix_get -s %s -k %s' % (ip, key),
                                              shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, err = zabbix_get_command.communicate()
        if err:
            return 'ERROR'
        return result.strip()

    def create_object(self, object_name, *args, **kwargs):
        return object_name(self, *args, **kwargs)

    def get_host_by_hostid(self, hostids):
        if not isinstance(hostids,list):
            hostids = [hostids]
        return [d['host'] for d in self.host.get({'hostids': hostids, 'output': 'extend'})]

#################################################
#    Decorate Method
#################################################


def check_auth(func):
    def ret(self, *args):
        self.__checkAuth__()
        return func(self, args)
    return ret


def post_json(method_name):
    def decorator(func):
        def wrapper(self, params):
            try:
                content = self.post_request(self.json_obj(method_name, params).encode("utf-8"))
                return content['result']
            except KeyError as e:
                e = content['error']['data']
                raise ZabbixAPIException(e)
        return wrapper
    return decorator


def zabbix_api_object_method(func):
    def wrapper(self, method_name, params):
        try:
            content = self.post_request(self.json_obj(method_name, params).encode(encoding="utf-8"))
            logger.debug("\ncontent:{0}".format(content))
            return content['result']
        except KeyError as e:
            e = content['error']['data']
            raise ZabbixAPIException(e)
    return wrapper

#################################################
#    Zabbix API Object (host, item...)
#################################################


class ZabbixAPIObjectFactory(object):
    def __init__(self, zapi, object_name=''):
        self.__zapi = zapi
        self.__object_name = object_name

    def __checkAuth__(self):
        self.__zapi.__checkAuth__()

    def post_request(self, json_obj):
        return self.__zapi.post_request(json_obj)

    def json_obj(self, method, param):
        return self.__zapi.json_obj(method, param)

    def __getattr__(self, method_name):
        def method(params):
            return self.proxy_method('%s.%s' % (self.__object_name,method_name), params)
        return method

    # 'find' method is a wrapper of get.
    # Difference between 'get' and 'find' is that 'find' can create object you want while it doesn't exist
    def find(self, params, attr_name=None, to_create=False):
        filtered_list = []
        #logger.debug("params: {0}".format(params))
        result = self.proxy_method('%s.get' % self.__object_name, {'output': 'extend', 'filter': params})
        if to_create and len(result) == 0:
            result = self.proxy_method('%s.create' % self.__object_name, params)
            logger.info("{0}.create: {1} ".format(self.__object_name,result))
            return list(result.values())[0]
        if attr_name is not None:
            for element in result:
                filtered_list.append(element[attr_name])
            logger.info("{0}.get attr_name: {1} ".format(self.__object_name,filtered_list))
            return filtered_list
        else:
            return result


    @zabbix_api_object_method
    @check_auth
    def proxy_method(self, method_name, params):
        pass

