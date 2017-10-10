#coding=utf-8

from multiprocessing import Process
import time

class MyProcess(Process):
	def __init__(self, time):
		self.time = time
		Process.__init__(self)
	
	def run(self):
		c_start = time.time()
		print("child before sleep")
		time.sleep(self.time)
		c_end = time.time()
		print("child after sleep, child runs %s s" %(c_end-c_start))

f_start = time.time()
p = MyProcess(2)
print("father start child process")
p.start()
p.join()
f_end = time.time()
print("father runs %s s" %(f_end-f_start))

#父进程会等子进程退出才退出

