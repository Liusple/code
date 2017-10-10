#coding=utf-8

from threading import Thread
import time, os

def work():
	print("thread pid:%s ppid:%s" %(os.getpid(), os.getppid()))
	time.sleep(1)
	print("thread end")
	
print("pid:%s ppid:%s" %(os.getpid(), os.getppid()))
for i in range(3):
	t = Thread(target=work)
	t.start()
print("---run here---")
#主线程会等待子线程退出
