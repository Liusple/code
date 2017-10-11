from greenlet import greenlet
import time

def work1():
	while True:
		print("---A---")
		time.sleep(1)
		g2.switch()

	
def work2():
	while True:
		print("---B---")
		time.sleep(1)
		g1.switch()

	
g1 = greenlet(work1)
g2 = greenlet(work2)

g1.switch()
