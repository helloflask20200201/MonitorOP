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

logger = logging.getLogger("MOP.Zabbix.Template")

def template_find(zapi,host):
    params = {
            "host": host
        }
    #zapi.Template.find(params, attr_name=None, to_create=True)
    return zapi.Template.find(params, attr_name=None, to_create=True)

def templateid_find(zapi,host):
    params = {
            "host": host
        }
    #zapi.Template.find(params, attr_name=None, to_create=True)
    return zapi.Template.find(params, attr_name='templateid', to_create=False)