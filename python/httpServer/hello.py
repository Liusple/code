def application(env, response):
    response("200", [("Server", "Test Server")])
    return "hello world"
