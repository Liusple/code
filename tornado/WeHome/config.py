import os

settings = dict(
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		cookie_secret = "test",
		#xsrf_cookies = True,
		debug = True
	)

mysql_options = dict(
		host = "127.0.0.1",
		database = "pHome",
		user="root",
		password="qwer1234"
	)

redis_options = dict(
		host = "127.0.0.1",
		port = 6379
	)

log_path = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"