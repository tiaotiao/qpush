#coding:utf-8
from tornado.web import  Application
from qpush.publish import PublishHandler 

class PublishApplcation(Application):
    def __init__(self):
        handlers = [
            (r'/',  PublishHandler),    
        ] 
        Application.__init__(self, handlers) 

