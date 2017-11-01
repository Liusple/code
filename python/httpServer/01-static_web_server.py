from socket import *
from multiprocessing import Process

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(("", 5000))
server_socket.listen(4)

def deal_client(client_socket):
    data = client_socket.recv(1024)
    # print(type(data)) #byte
    # print(data)
    start_line = "HTTP/1.1 200 OK\r\n"
    headers = "Server: Lisuple server\r\n"
    body = "Welcome!\r\n"
    response = start_line + headers + "\r\n" + body
    client_socket.send(bytes(response, "utf-8")) # must be bytes
    client_socket.close()
    

while True:
    client_socket, client_info = server_socket.accept()
    print("%s on line" %(client_info,))
    p = Process(target=deal_client, args=(client_socket,))
    p.start()
    client_socket.close()
