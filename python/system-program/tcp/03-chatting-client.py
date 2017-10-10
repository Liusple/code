from socket import *

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(("192.168.2.102", 8992))
try:
	while True:
		send_data = input(">")
		client_socket.send(send_data.encode("utf-8"))
		recv_data = client_socket.recv(1024)
		if len(recv_data):
			print("recv data:%s" %(recv_data.decode("utf-8")))
		else:
			break
except:
	pass
finally:
	print("close clinet socket")
	client_socket.close()
