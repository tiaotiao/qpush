#coding:utf-8
from tornado.web import  Application
from qpush.handlers import MessageHandler 

class PublishApplcation(Application):
    def __init__(self):
        handlers = [
            (r'/msg', PublishCometHandler)    
        ] 
        Application.__init__(self, handlers) 

