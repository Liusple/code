from threading import Thread, enumerate
import os, time

def work1():ge
	print("in work1")
	time.sleep(2)
	print("work1 end")
	
def work2():
	print("in work2")
	time.sleep(2)
	print("work2 end")
	
t1 = Thread(target=work1)
t2 = Thread(target=work2)
t1.start()
t2.start()
while True:
	length = len(enumerate())
	print("threads num:%s" %length)
	if length <= 1:
		break;
	
