from socket import *

tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.connect(("192.168.2.101", 9090))
while True:
	data = input(">>")
	tcp_socket.send(data.encode("gb2312"))
	if data == "bye":
		break

tcp_socket.close()
