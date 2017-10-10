import threading
import time

g_num = 0

def work1():
	global g_num
	g_num = 6
	print("work1 set g_num:%s" %g_num)

def work2():
	global g_num
	time.sleep(2)
	print("work2 get g_num:%s" %g_num)
	
print("origin g_num:%s" %g_num)
t1 = threading.Thread(target=work1)
t1.start()
t2 = threading.Thread(target=work2)
t2.start()
