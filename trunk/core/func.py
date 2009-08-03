#!/usr/bin/python
# -*- coding: utf-8 -*-
#Файл с вспомогательными функциями
import sys
import xmpp
import os
import time

def get_local_time():
    local_time = time.localtime()
    year = unicode(local_time.tm_year)
    day = unicode("%02d" % local_time.tm_mday)
    month = unicode("%02d" % local_time.tm_mon)
    hour = unicode("%02d" % local_time.tm_hour)
    minute = unicode("%02d" % local_time.tm_min)
    second = unicode("%02d" % local_time.tm_sec)
    local_time = year+month+day+u"T"+hour+u":"+minute+u":"+second
    return unicode(local_time)
