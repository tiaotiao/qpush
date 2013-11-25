#coding:utf-8
from tornado.web import  Application
from qpush.push.handlers import StatusHandler 
from qpush.push.handlers import MessageHandler 

class PushApplication(Application):
    def __init__(self):
        handlers = [
            (r'/status', StatusHandler),    
            (r'/msg', MessageHandler)    
        ] 
        Application.__init__(self, handlers) 

