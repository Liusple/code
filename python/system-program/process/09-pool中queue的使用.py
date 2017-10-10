from multiprocessing import Manager, Pool
import time

def write(q):
	for i in "hello":
		print("write %s" %i)
		q.put(i)

def read(q):
	print("read sleep 5s")
	time.sleep(5)
	for i in range(q.qsize()):
		print("read %s" %q.get())

	

p = Pool(3)
queue = Manager().Queue()
p.apply_async(write, args=(queue, ))
p.apply_async(read, args=(queue, ))
p.close()
p.join()

print("end all")

