#coding:utf-8
import tornado.options
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.httpserver import HTTPServer

from qpush.push.app import PushApplication


def main():
    define("port", default=8000, help="run on the given port")
    tornado.options.parse_command_line()

    app = PushApplication()
    http_server = HTTPServer(app)
    http_server.listen(options.port)

    IOLoop.instance().start()

if __name__ == '__main__':
    main()
