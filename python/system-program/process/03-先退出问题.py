import os
import time


pid = os.fork()
if pid == 0:
	print("child start sleep")
	time.sleep(5)
	print("child sleep end")
else:
	print("father start sleep")
	time.sleep(2)
	print("father sleep end")

print("-----------over---------")
#主进程不会等待子进程退出才退出
