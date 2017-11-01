#coding=utf-8

import threading
import time

def work():
	name = threading.current_thread().name
	num = 0
	if name == "Thread-1":
		num += 1
	else:
		time.sleep(2)
	print("%s num:%s" %(name, num))
	
	
t1 = threading.Thread(target=work)
t2 = threading.Thread(target=work)
t1.start()
#time.sleep(2)
t2.start()

#非全局变量各个线程各自独立存在，互不影响
