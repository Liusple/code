import threading
import time

def work1(args):
	args.append("sam")
	print("work1 append sam")
	
def work2(args):
	print("work2 args:%s" %args)
	

list_name = ["lius", "alex"]
t1 = threading.Thread(target=work1, args=(list_name, ))
t1.start()
time.sleep(3)
t2 = threading.Thread(target=work2, args=(list_name, ))
t2.start()
time.sleep(1)
print("list_name:%s" %list_name)
