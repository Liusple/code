from socket import *
from threading import Thread

def deal_client(client_socket, client_info):
	while True:
		data = client_socket.recv(1024)
		if len(data) <= 0:
			print("%s disconnect" %client_info[0])
			break
		print("%s say %s" %(client_info, data.decode("gb2312")))
	client_socket.close()	
	
def main():
	server_socket = socket(AF_INET, SOCK_STREAM)
	server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	server_socket.bind(("", 7878))
	server_socket.listen(4)
	try:
		while True:
			client_socket, client_info = server_socket.accept()
			print("%s connect" %client_info)
			p = Thread(target=deal_client, args=(client_socket, client_info))
			p.start()
			#client_socket.close()
	except Exception as e:
		print(e)
	finally:
		server_socket.close()
		
if __name__ == "__main__":
	main()
