#coding=utf-8

import tornado.ioloop
import tornado.options
import tornado.web
import os.path
from tornado.options import define, options
import tornado.websocket
import logging
import uuid
import datetime

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/chatsocket", ChatSocketHandler),
		]

		settings = dict(
				cookie_secret = "Forever young",
				template_path = os.path.join(os.path.dirname(__file__), "templates"),
				static_path = os.path.join(os.path.dirname(__file__), "static"),
				xsrf_cookies = True,
			)
		super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html", messages=ChatSocketHandler.cache, users=ChatSocketHandler.waiters, username="游客%d" %ChatSocketHandler.client_id)

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
	waiters = set()
	client_id = 1
	cache = []
	cache_size = 200

	def open(self):
		self.client_id = ChatSocketHandler.client_id
		ChatSocketHandler.client_id += 1
		self.username = "游客%d" %self.client_id
		ChatSocketHandler.waiters.add(self)

		chat = {
			"id": str(uuid.uuid4()),
			"type": "online",
			"client_id": self.client_id,
			"username": self.username,
			"datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		}
		ChatSocketHandler.send_updates(chat)

	def on_close(self):
		ChatSocketHandler.waiters.remove(self)
		chat = {
			"id": str(uuid.uuid4()),
			"type": "offline",
			"client_id": self.client_id,
			"username": self.username,
			"datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		}
		ChatSocketHandler.send_updates(chat)


	def on_message(self, message):
		logging.info("recv message:%r", message)
		parsed = tornado.escape.json_decode(message)  #???
		self.username = parsed["username"]
		chat = {
			"id": str(uuid.uuid4()),
			"body": parsed["body"],
			"type": "message",
			"client_id": self.client_id,
			"username": self.username,
			"datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		}

		chat["html"] = tornado.escape.to_basestring(
				self.render_string("message.html", message=chat)
			)
		ChatSocketHandler.update_cache(chat)
		ChatSocketHandler.send_updates(chat)

	@classmethod
	def update_cache(cls, chat):
		cls.cache.append(chat)
		if len(cls.cache) > cls.cache_size:
			cls.cache = cls.cache[-cls.cache_size:]

	@classmethod
	def send_updates(cls, chat):
		logging.info("send message to %d waiters", len(cls.waiters))
		for waiter in cls.waiters:
			try:
				waiter.write_message(chat)
			except:
				logging.error("Error send message", exc_info=True)

def main():
	tornado.options.parse_command_line()
	app = Application()
	app.listen(options.port)
	tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
	main()