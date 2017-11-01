from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", 9090))
server_socket.listen(5)
#设置为堵塞后，如果accept时，恰巧没有客户端connect，那么accept会
#产生异常，所以需要try来进⾏处理
server_socket.setblocking(False)

socket_list = []

try:
	while True:
		try:
			client_socket, client_info = server_socket.accept()
		except:
			pass #没有accept的时候程序进这里
		else:
			client_socket.setblocking(False)
			socket_list.append((client_socket, client_info))
			print("%s:%s connect" %(client_info[0], client_info[1]))
		for sock, info in socket_list:
			try:
				data = sock.recv(1024)
			except:
				pass
			else:
				if len(data) <= 0:
					socket_list.remove((sock, info))
					sock.close()
					print("%s:%s disconnect" %(info[0], info[1]))
				else:
					print("%s say %s" %(info, data.decode("gb2312")))
except Exception as e:
	print(e)
finally:
	print("close server socket")
	server_socket.close()

