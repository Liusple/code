from socket import *

tcp_socket = socket(AF_INET, SOCK_STREAM)

tcp_socket.bind(("", 7070))
tcp_socket.listen(5)
print("---A---")
client_socket, info = tcp_socket.accept()
print("---B---")
data = client_socket.recv(1024)
print("%s say %s" %(info, data.decode("gb2312")))
client_socket.send("hello".encode("gb2312"))
client_socket.close()
tcp_socket.close()

