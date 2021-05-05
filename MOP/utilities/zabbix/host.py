#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################
# Python API for Zabbix v1.0
#
# Author: huweihua @VIPS, Hangzhou, China
# Email:  fbi7934@sina.com
# Date:   20210424
################################################
from MOP.utilities.zabbix.hostgroup import hostgroup_find,hostgroupid_find
import logging

logger = logging.getLogger("MOP.Zabbix.Host")

def host_find(zapi,ip,hostgroups,hostname=''):
    if hostname:
        name = ip + '_' + hostname
    else:
        name = ip
    groupids = hostgroupid_find(zapi,hostgroups)
    if not groupids:
        logger.info("Host.create failure,groups not exist")
        return False
    groups = list()
    for groupid in groupids:
        groups.append({"groupid": groupid})
    params = {
        "host": ip,
        "name": name,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": groups
    }
    #zapi.Template.find(params, attr_name=None, to_create=True)
    return zapi.Host.find(params, attr_name=None, to_create=True)


def hostid_find(zapi,ip,hostgroups,hostname=''):
    if hostname:
        name = ip + '_' + hostname
    else:
        name = ip
    groupids = hostgroupid_find(zapi,hostgroups)
    groups = list()
    for groupid in groupids:
        groups.append({"groupid": groupid})
    params = {
        "host": ip,
        "name": name,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": groups
    }
    return zapi.Host.find(params, attr_name='hostids', to_create=False)