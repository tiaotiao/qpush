#coding:utf-8
import tornado.options
from tornado.ioloop import IOLoop
from tornado.optins import define, options
from tornado.httpserver import HTTPServer

from qpush.push import PublishApplication


def main():
    define("port", default=9000, help="run on the given port")
    tornado.options.parse_command_line()

    app = PublishApplication()
    http_server = HTTPServer(app)
    http_server.listen(options.port)

    #start ioloop
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
