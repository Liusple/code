#coding=utf-8

import gevent
import urllib2
from gevent import monkey

#有IO才做时需要这一句
monkey.patch_all()

def download(url):
	print url
	resp = urllib2.urlopen(url)
	data = resp.read()
	print('%d bytes received from %s.' % (len(data), url))
	

g1 = gevent.spawn(download, "http://www.sohu.com/")
g3 = gevent.spawn(download, 'http://www.itheima.com/')
g2 = gevent.spawn(download, "http://www.baidu.com/")
g4 = gevent.spawn(download, 'http://www.itcast.cn/')
g1.join()
g2.join()
g3.join()
g4.join()

