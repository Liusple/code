#coding=utf-8

from socket import *

#绑定端口，一般是服务端绑定端口
udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(("", 7799))

ip = "192.168.2.101"
port = 8080
udp_socket.sendto("hello\n".encode("gb2312"), (ip, port))
udp_socket.close()
