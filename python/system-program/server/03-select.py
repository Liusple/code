from socket import *
import select
import sys

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", 9090))
server_socket.listen(4)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

input_list = [server_socket, sys.stdin]

running = True
while True:
	readable, writeable, exceptable = select.select(input_list, [], [])
	for sock in readable:
		if sock == server_socket:
			client_socket, client_info = sock.accept()
			print("%s:%s connect" %(client_info[0], client_info[1]))
			input_list.append(client_socket)
		elif sock == sys.stdin:
			cmd = sys.stdin.readline()
			running = False
		else:
			data = sock.recv(1024)
			if len(data) <=0:
				input_list.remove(sock)
				sock.close()
			else:
				print("recv:%s" %data.decode("gb2312"))
				sock.send(data)
				
	if not running:
		print("program will stop")
		break
		
server_socket.close()
		
