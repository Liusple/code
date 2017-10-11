from socket import *


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", 9090))
server_socket.listen(5)

while True:
	client_socket, client_info = server_socket.accept()
	print("%s connect" %(str(client_info)))
	while True:
		data = client_socket.recv(1024)#type(data) bytes
		if len(data) <= 0:
			client_socket.close()
			print("%s disconnect" %(str(client_info)))
			break
		else:
			print(type(client_info))
			print("%s say %s" %(client_info, data.decode("gb2312")))

server_socket.close()
