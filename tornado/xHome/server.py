#coding=utf-8

import os
import torndb
import config
import redis

from handlers import Passport
from urls import urls

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import options, define

define("port", default=8000, type=int, help="run server on the given port")

class Application(tornado.web.Application):
	def __init__(self, *args, **kwargs):
		super(Application, self).__init__(*args, **kwargs)
		# self.db = tornadb.Connection(
		# 		host = config.mysql_options["host"],
		# 		database = config.mysql_options["database"],
		# 		user = config.mysql_options["user"],
		# 		password = config.mysql_options["password"]
		# 	)
		self.db = torndb.Connection(**config.mysql_options)
		self.redis = redis.StrictRedis(**config.redis_options)

def main():
	options.log_file_prefix = config.log_path
	options.logging = config.log_level
	tornado.options.parse_command_line()
	app = Application(
			urls,
			**config.settings
		)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
	main()