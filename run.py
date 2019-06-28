#! -*- coding: utf-8 -*-
import os

from tornado.httpserver import HTTPServer
from tornado import ioloop
from tornado.options import options, define
from tornado import web
import tornado


define("port", default=8888, help="run on thr given port", type=int)


class Application(web.Application):
    def __init__(self, debug=False):
        handlers = [
            (r"/", 'handlers.AccountHandler'),
            (r"/api/?", 'handlers.APIRequestHandler'),
        ]

        app_settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'template'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=debug,
        )
    
        super(Application, self).__init__(handlers=handlers, **app_settings)


if __name__ == "__main__":
    options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
