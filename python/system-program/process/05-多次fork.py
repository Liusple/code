import os
import time

#8个进程
os.fork()
os.fork()
os.fork()

print("---before sleep---")
time.sleep(4)
print("---after sleep---")
