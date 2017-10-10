from socket import *
import threading

def send():
	global udp_socket
	while True:
		data = input(">")
		udp_socket.sendto(data.encode("gb2312"), ("192.168.2.101", 8080))
	
def receive():
	global udp_socket
	#udp没有判断len(data)
	while True:
		data, dest_info = udp_socket.recvfrom(1024)
		print("\r<%s say:%s" %(dest_info, data.decode("gb2312")), end="\n>")

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(("", 7979))
t1 = threading.Thread(target=send)
t2 = threading.Thread(target=receive)
t1.start()
t2.start()
