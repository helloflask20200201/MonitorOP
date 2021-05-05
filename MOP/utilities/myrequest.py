#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################
# Python API for Zabbix v1.0
#
# Author: huweihua @VIPS, Shanghai, China
# Email:  fbi7934@sina.com
# Date:   20210424
################################################
# Python3 version by huweihua
# Email: fbi7934@sina.com
# Date: 20210424
################################################

def create_object(object_name, *args, **kwargs):
        return object_name(*args, **kwargs)

def Host(name):
    print(name)

def A():
    print('222')

if __name__ == "__main__":
    create_object(object_name=Host,name=111)
    create_object(object_name=A)

