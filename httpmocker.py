#!/usr/bin/env python
# coding: utf-8

import configobj
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

config = configobj.ConfigObj("config.ini")


class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        if self.request.uri == "/favicon.ico":
            self.finish()


class HttpMockerHandler(BaseHandler):
    def get(self, slug):
        self.write(str(config))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/([\d\D]*)", HttpMockerHandler)
        ]
        settings = dict(
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(config["httpmocker"]["port"])
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
