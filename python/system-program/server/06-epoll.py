from socket import *
import select

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(("", 9090))
server_socket.listen(4)

epoll = select.epoll()
#EPOLLIN	（可读）
#EPOLLOUT	（可写）
#EPOLLET	（ET模式）
#LT模式：当epoll检测到描述符事件发生并将此事件通知应用程序，应用程序可以不立即处理该事件。下次调用epoll时，会再次响应应用程序并通知此事件。
#ET模式：当epoll检测到描述符事件发生并将此事件通知应用程序，应用程序必须立即处理该事件。如果不处理，下次调用epoll时，不会再次响应应用程序并通知此事件。

epoll.register(server_socket.fileno(), select.EPOLLIN | select.EPOLLET)

connections = {}
address = {}
print("start to accept")
while True:
	#epoll进⾏fd	扫描的地⽅	--未指定超时时间则为阻塞等待
	epoll_list = epoll.poll()
	for fd, events in epoll_list:
		if fd == server_socket.fileno():
			conn, addr = server_socket.accept()
			print("%s online" %(addr, ))
			connections[conn.fileno()] = conn
			address[conn.fileno()] = addr
			epoll.register(conn.fileno(), select.EPOLLIN | select.EPOLLET)
		elif events == select.EPOLLIN:
			data = connections[fd].recv(1024)
			if len(data) > 0:
				print("%s say %s" %(address[fd], data.decode("gb2312")))
			else:
				epoll.unregister(fd)
				connections[fd].close()
				print("%s offline" %(address[fd], ))
