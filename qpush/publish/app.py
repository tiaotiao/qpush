#coding:utf-8
from tornado.web import  Application
from qpush.publish import PublishPushHandler 
from qpush.publish import PublishCometHandler 

class PublishApplcation(Application):
    def __init__(self):
        handlers = [
            (r'/push2publish',  PublishPushHandler),    
            (r'/comet2publish', PublishCometHandler)    
        ] 
        Application.__init__(self, handlers) 

