from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", 8982))
server_socket.listen(5)

try:
	while True:
		client_socket, client_info = server_socket.accept()
		while True:
			recv_data = client_socket.recv(1024) #recv_data type is bytes
			if len(recv_data) <= 0:
				break
			print("%s say %s" %(client_info, recv_data.decode("utf-8")))
			send_data = input(">")
			client_socket.send(send_data.encode("utf-8"))
		client_socket.close()
except:
	pass
finally:
	print("close server socket")
	server_socket.close()

