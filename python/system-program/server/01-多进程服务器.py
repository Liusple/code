from socket import *
from multiprocessing import Process


def deal_new_connect(client_socket, client_info):
	while True:
		data = client_socket.recv(1024)
		if len(data) <= 0:
			break
		print("%s say %s" %(client_info, data.decode("utf-8")))
	client_socket.close()
	

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(("", 8888))
server_socket.listen(5)
try:
	while True:
		client_socket, client_info = server_socket.accept()
		p = Process(target=deal_new_connect, args=(client_socket, client_info))
		p.start()
		print("new client:%s" %client_info[0])
		#已经向子进程复制了一份socket，所以这里可以关闭
		client_socket.close()
except Exception as e:
	print(e)
finally:
	print("close server socket")
	server_socket.close()
