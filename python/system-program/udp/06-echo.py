from socket import *

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(("", 7878))

while True:
	data, info = udp_socket.recvfrom(1024)
	udp_socket.sendto(data, info)
	
