from socket import *

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(("", 7878))
data = udp_socket.recvfrom(1024)
print(type(data))
print(data)
print("receive msg:%s from:%s" %(data[0].decode("gb2312"), data[1][0]))
udp_socket.close()

#这种写法
#data, dest_info = udp_socket.recvfrom(1024)
