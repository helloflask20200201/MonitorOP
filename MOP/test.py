#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################
# Python API for Zabbix v1.0
#
# Author: huweihua @VIPS, Shanghai, China
# Email:  fbi7934@sina.com
# Date:   20210424
################################################

from MOP.utilities.zabbix.hostgroup import hostgroup_find,hostgroupid_find
from MOP.utilities.zabbix.template import template_find,templateid_find
from MOP.utilities.zabbix.host import host_find
import logging

logger = logging.getLogger("MOP.Zabbix.test")

def hostgroup_test(zapi):
    names = ['Test4','Test5','Test6']
    groupid = hostgroupid_find(zapi,names)
    logger.info("groupid：{0}".format(groupid))
    name = 'Test1'
    groupid = hostgroupid_find(zapi,name)
    logger.info("groupid：{0}".format(groupid))


def template_test(zapi):
    hosts = ['Template OS Linux','Template OS Windows']

    templateid = templateid_find(zapi,hosts)
    logger.info("templateid：{0}".format(templateid))

def host_test(zapi):
    ip = '192.168.0.9'
    hostgroups = ['Test2','Test5']
    hostname = 'zabbix-mysql'
    host_find(zapi,ip,hostgroups,hostname=hostname)