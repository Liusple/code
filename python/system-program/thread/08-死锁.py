import threading
import time, os

def work1():
	mutexA.acquire()
	print("in work1")
	time.sleep(1)
	if mutexB.acquire():
		print("work1 mutexB.acquire")
		mutexB.release()
	mutexA.release()
	
def work2():
	mutexB.acquire()
	print("in work2")
	time.sleep(1)
	if mutexA.acquire():
		print("work2 mutexA.acquire")
		mutexA.release()
	mutexB.release()

print("pid:%s" %os.getpid())
mutexA = threading.Lock()
mutexB = threading.Lock()

t1 = threading.Thread(target=work1)
t2 = threading.Thread(target=work2)

t1.start()
t2.start()

