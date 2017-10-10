#coding=utf-8
from multiprocessing import Process
import os
import time

def fun(*args):
	time.sleep(1)	
	print(type(args))
	print("child process run, args:%s, pid:%d ppid:%d" %(args, os.getpid(), os.getppid()))

tmp = [1, 2, 3]
p = Process(target=fun, args=(*tmp,))
p.start()
#p.join() #等待子进程执行完毕
print("father process run")
print("father id:%s" %os.getpid())

#主进程会等子进程结束了才退出
