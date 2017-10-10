#coding:utf-8

import os

pid = os.fork()

if pid < 0:
	print("fork error")
elif pid == 0:
	print("子线程pid:%s 父线程pid:%s" %(os.getpid(), os.getppid()))
else:
	print("父线程pid:%s 返回的pid:%s" %(os.getpid(), pid))
	
print("父子进程都可以执行这里")
