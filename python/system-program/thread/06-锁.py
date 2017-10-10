import threading
import time

g_num = 0

def work1():
	global g_num
	mutex.acquire()
	for i in range(1000000):
		g_num += 1
	#mutex.release()
	print("work1 g_num:%s" %g_num)
	
def work2():
	global g_num
	mutex.acquire()
	for i in range(1000000):
		g_num += 1
	mutex.release()
	print("work2 g_num:%s" %g_num)

mutex = threading.Lock()
t1 = threading.Thread(target=work1)
t2 = threading.Thread(target=work2)
t1.start()
#time.sleep(2)
t2.start()
print("g_num:%s" %g_num)


	

