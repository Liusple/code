#coding utf-8

import threading
import time

class MyThread(threading.Thread):
	def __init__(self):
		#不能缺少调用父类的__init__
		#threading.Thread.__init__(self)
		super().__init__()
		
	def run(self):
		for i in range(3):
			print("%s start" %self.name)
			time.sleep(2)

#线程执行顺序由操作系统调用
for i in range(5):		
	t = MyThread()
	t.start()

	
	
