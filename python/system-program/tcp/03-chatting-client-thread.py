from socket import *
from threading import Thread

def send():
	global client_socket
	global run_flag
	while run_flag:
		send_data = input(">")
		client_socket.send(send_data.encode("utf-8"))
	client_socket.close()

def recv():
	global client_socket
	global run_flag
	while True:
		recv_data = client_socket.recv(1024)
		if len(recv_data):
			print("recv %s" %recv_data.decode("utf-8"))
		else:
			print("break")
			break
	run_flag = False

run_flag = True
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(("192.168.2.102", 8982))

t1 = Thread(target=send)
t2 = Thread(target=recv)
t1.start()
t2.start()
