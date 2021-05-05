#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################
# Python API for Zabbix v1.0
#
# Author: huweihua @VIPS, Shanghai, China
# Email:  fbi7934@sina.com
# Date:   20210424
################################################

from MOP.test import hostgroup_test,template_test,host_test
from MOP.utilities.zabbix.zabbix_api import ZabbixAPI

if __name__ == "__main__":
    zapi = ZabbixAPI(url='http://192.168.0.9', user='admin', password='zabbix')
    zapi.login()
    #hostgroup_test(zapi)
    #template_test(zapi)
    host_test(zapi)