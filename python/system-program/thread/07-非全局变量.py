#coding=utf-8

import threading
import time

def work():
	num = 0
	num += 1
	time.sleep(1)
	print("%s num:%s" %(threading.current_thread(), num))
	
	
t1 = threading.Thread(target=work)
t2 = threading.Thread(target=work)
t1.start()
time.sleep(2)
t2.start()

#非全局变量各个线程各自独立存在，互不影响
