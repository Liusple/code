from multiprocessing import Pool
import os,time
def work():
	print("in work")
	time.sleep(4)
	return "lius"

#回调函数由主进程执行，两个pid相等，参数由work返回
def fun(args):
	print("func args:%s, pid:%s" %(args, os.getpid()))
	

p = Pool(3)
print("pid:%s" %os.getpid())
p.apply_async(func=work, callback=fun)
while True:
	print("in running")
	time.sleep(0.5)
