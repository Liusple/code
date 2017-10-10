#coding=utf-8

from socket import *


udp_socket = socket(AF_INET, SOCK_DGRAM)
ip = "192.168.2.101"
port = 8080
udp_socket.sendto("hello\n".encode("gb2312"), (ip, port))
udp_socket.sendto("你好".encode("gb2312"), (ip, port))
udp_socket.close()
