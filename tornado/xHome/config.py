#coding=utf-8
import os

settings = dict(
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		cookie_secret = "HhLXI+BRRomtuaG47hsXEg3JCdi0BUi8vrpWmoxaoyI=",
		#xsrf_cookies = True,
		debug = True
	)

mysql_options = dict(
		host = "127.0.0.1",
		database = "ihome",
		user="root",
		password="qwer1234"
	)

redis_options = dict(
		host = "127.0.0.1",
		port = 6379
	)

log_path = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"
# 密码加密密钥
passwd_hash_key = "nlgCjaTXQX2jpupQFQLoQo5N4OkEmkeHsHD9+BBx2WQ="