import gevent
from gevent import monkey, socket

monkey.patch_all()


def deal_client(client):
	while True:
		data = client[0].recv(1024) #type(data) str
		if len(data) <= 0:
			client[0].close()
			print client[1], "off line"
			break
		print "recv:", data.decode("gb2312")
		
s_socket = socket.socket()
s_socket.bind(("", 9090))
s_socket.listen(5)	

print "waiting for connent..."
while True:
	c_socket, c_info = s_socket.accept()
	print c_info, "online"
	gevent.spawn(deal_client, (c_socket, c_info))
	#not join
