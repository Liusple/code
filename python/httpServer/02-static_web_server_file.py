from socket import *
from multiprocessing import Process


HTML_DIR = "./html"


def deal_client(client_socket):
    data = client_socket.recv(1024)
    #print(data)
    data = data.decode("utf-8")
    data = data.splitlines()
    start_line = data[0]
    print(start_line)
    file = start_line.split()[1]
    print(file)
    if file == "/":
        file = "/index.html"
    response = ""
    try:
        f = open(HTML_DIR + file, "rb")
        body = f.read().decode("utf-8")
        f.close()
        start_line = "HTTP/1.1 200 OK \r\n"
        header = "Server: Test server \r\n"
        response = start_line + header + "\r\n" + body
    except:
        start_line = "HTTP/1.1 404 NOT FOUND \r\n"    
        response = start_line + "\r\n" + "file error"
    client_socket.send(bytes(response, "utf-8"))
    client_socket.close()



if __name__ == "__main__":
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(("", 5000))
    server_socket.listen(5)

    client_socket, client_info = server_socket.accept()
    print("%s on line" %(client_info, ))
    p = Process(target=deal_client, args=(client_socket,))
    p.start()
    client_socket.close()

