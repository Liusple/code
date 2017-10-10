from socket import *

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(("", 7919))

while True:
	data, dest_info = udp_socket.recvfrom(1024)
	if data.decode("gb2312") == "boomshakalaka":
		break
	else:
		print("%s say %s" %(dest_info, data.decode("gb2312")))
