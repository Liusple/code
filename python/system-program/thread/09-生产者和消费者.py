import threading
from queue import Queue
import time
global g_queue

'''
为什么要使⽤⽣产者和消费者模式
在线程世界⾥，⽣产者就是⽣产数据的线程，消费者就是消费数据的线程。
在多线程开发当中，如果⽣产者处理速度很快，⽽消费者处理速度很慢，那
么⽣产者就必须等待消费者处理完，才能继续⽣产数据。同样的道理，如果
消费者的处理能⼒⼤于⽣产者，那么消费者就必须等待⽣产者。为了解决这
个问题于是引⼊了⽣产者和消费者模式。

什么是⽣产者消费者模式
⽣产者消费者模式是通过⼀个容器来解决⽣产者和消费者的强耦合问题。⽣
产者和消费者彼此之间不直接通讯，⽽通过阻塞队列来进⾏通讯，所以⽣产
者⽣产完数据之后不⽤等待消费者处理，直接扔给阻塞队列，消费者不找⽣
产者要数据，⽽是直接从阻塞队列⾥取，阻塞队列就相当于⼀个缓冲区，平
衡了⽣产者和消费者的处理能⼒。
这个阻塞队列就是⽤来给⽣产者和消费者解耦的。纵观⼤多数设计模式，都
会找⼀个第三者出来进⾏解耦，
'''

class Producer(threading.Thread):
	def run(self):
		global g_queue
		count = 0
		while True:
			if g_queue.qsize() < 1000:
				for i in range(200):
					count += 1
					g_queue.put(count)
					print("Producer put %s" %count)
			time.sleep(1)
		
class Consumer(threading.Thread):
	def run(self):
		global g_queue
		while True:
			if g_queue.qsize() > 100:
				print("Consumer get %s" %g_queue.get())
			#time.sleep(1)
		

g_queue = Queue()
for i in range(100):
	g_queue.put(i)
	
p = Producer()
c = Consumer()
p.start()
c.start()
