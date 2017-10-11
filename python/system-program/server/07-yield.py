import time

def work1():
	while True:
		print("---A---")
		yield
		time.sleep(1)
	
def work2(f):
	while True:
		print("---B---")
		next(f)
		time.sleep(1)

f = work1()
work2(f)
