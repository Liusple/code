from socket import *
from multiprocessing import Process

HTML_DIR = "./html"

class HttpServer():
    def __init__(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # self.server_socket.listen(5)

    def bind(self, port):
        self.server_socket.bind(("", port))

    def start(self):
        self.server_socket.listen(4)
        while True:
            client_socket, client_info = self.server_socket.accept()
            print("%s on line" %(client_info,))
            p = Process(target=self.deal_client, args=(client_socket,))
            p.start()
            client_socket.close()

    def deal_client(self, client_socket):
        data = client_socket.recv(1024)
        data = data.decode("utf-8")
        start_line = data.splitlines()[0]
        file_name  = start_line.split()[1]
        if file_name == "/":
            file_name = "/index.html"
        print(start_line, file_name)
        try:
            file = open(HTML_DIR + file_name, "rb")
            response_body = file.read().decode("utf-8")
            response_start = "HTTP/1.1 200 OK \r\n"
            response_header = "Server:Test \r\n"
        except:
            response_start = "HTTP/1.1 404 NOT FOUND \r\n"
            response_header = "Server:Test \r\n"
            response_body = "File open error"
        response = response_start + response_header + "\r\n" + response_body
        client_socket.send(response.encode("utf-8"))
        client_socket.close()


http_server = HttpServer()
http_server.bind(5000)
http_server.start()













