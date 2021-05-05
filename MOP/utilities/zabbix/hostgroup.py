#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################
# Python API for Zabbix v1.0
#
# Author: huweihua @VIPS, Hangzhou, China
# Email:  fbi7934@sina.com
# Date:   20210424
################################################
import logging

logger = logging.getLogger("MOP.Zabbix.Hostgroup")

def hostgroup_find(zapi,name):
    params = {
            "name": name
        }
    zapi.Hostgroup.find(params, attr_name=None, to_create=True)

def hostgroupid_find(zapi,name):
    params = {
            "name": name
        }
    return zapi.Hostgroup.find(params, attr_name='groupid', to_create=False)