import time
from my_web_server import HttpServer 

class Application(object):
    def __init__(self, urls):
        self.urls = urls

    def __call__(self, env, response):
        path = env.get("PATH_INFO", "/")
        for url, handler in self.urls:
            if path == url:
                return handler(env, response)
        status = "404 NOT FOUND"
        response(status, [])
        return "not found"

def say_hello(env, response):
    response("200 OK", [])
    return "hello"

def show_time(env, response):
    response("200 OK", [])
    return time.ctime()

urls = [
        ("/hello", say_hello),
        ("/time", show_time)
]

app = Application(urls)

if __name__ == "__main__":
    urls = [
        ("/hello", say_hello),
        ("/time", show_time)
    ]

    app = Application(urls)
#    http_server = HttpServer(app)
#    http_server.bind(5000)
#    http_server.start()



