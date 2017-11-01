#coding=utf-8

from multiprocessing import Pool
import time, os

def work(args):
	print("pid:%s, args:%s" %(os.getpid(), args))
	time.sleep(1)

#只会产生3个进程，由3个进程处理10个任务
p = Pool(3)
print("father start child process")
for i in range(10):
	#p.apply_async(work, (i,))
	#apply为阻塞式，只有第一个进程处理结束了，第二个进程才能开始处理
	p.apply(work, (i,))
	
p.close()
p.join()
print("child end") #父进程不会等待子进程，必须使用join

