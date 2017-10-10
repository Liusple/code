import os
import time

g_num = 0

pid = os.fork()
if pid == 0:
	g_num = 2
	print("child set g_num to 2")
else:
	time.sleep(2)	
	print("father get g_num:%s" %g_num)
	
#多进程中每个进程所有数据都各自拥有一份，互补影响
