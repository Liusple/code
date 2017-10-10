import threading

def work(args):
	#global local_student
	local_student.name = args
	fun()
	
def fun():
	#global local_student
	print("%s name:%s" %(threading.current_thread(), local_student.name))
	
local_student = threading.local()
t1 = threading.Thread(target=work, args=("lius",))
t2 = threading.Thread(target=work, args=("sam", ))
t1.start()
t2.start()
