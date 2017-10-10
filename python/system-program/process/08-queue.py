from multiprocessing import Queue, Process
import time,random

def write(q):
	for i in "hello":
		print("write put %s" %i)
		q.put(i)
		time.sleep(random.random())
	print("write end")
	
def read(q):
	while True:
		if not q.empty():
			print("read %s" %(q.get()))
		else:
			break;
		
q = Queue(10)
p1 = Process(target=write, args=(q, ))
p1.start()
p1.join()

p2 = Process(target=read, args=(q, ))
p2.start()
p2.join()

print("end all")

