# -*- coding: utf-8 -*-

import pycurl
import cStringIO

import sys
reload(sys)
sys.setdefaultencoding('utf8')


buf = cStringIO.StringIO()
 
c = pycurl.Curl()
c.setopt(c.URL, 'http://ent.sina.cn/xglm/ry/2014-07-30/detail-iawrnsfu0867728.d.html?pageAction=json&spage=1&vt=4')
c.setopt(c.WRITEFUNCTION,buf.write)
c.perform()

a = buf.getvalue()
print a
buf.close()