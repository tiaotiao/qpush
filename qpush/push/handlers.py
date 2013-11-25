#coding:utf-8
import json
import logging

from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler

from qpush.utils.generateid import gen_msg_id
from qpush.models.message import MessageDao


class ConnectionPool(object):
    connections = set()

    @classmethod
    def add_conn(cls, conn):
        cls.connections.add(conn)

    @classmethod
    def remove_conn(cls, conn):
        try:
            cls.connections.remove(conn)
        except KeyError:
            logging.warning("cannot remove conn %s" % conn)


class StatusHandler(WebSocketHandler):

    def open(self):
        ConnectionPool.add_conn(self)

    def on_message(self, raw_msg):
        msg = json.loads(raw_msg)
        if msg['action'] == 'online':
            pass
        elif msg['action'] == 'offline':
            pass
        elif msg['action'] == 'set_tags':
            pass
        else:
            pass

    def on_close(self):
        ConnectionPool.remove_conn(self)


class MessageHandler(RequestHandler):
    def post(self):
        msg_content = self.get_argument('msg')
        appid = self.get_arguments('appid')
        uid = self.get_arguments('uid')
        msgid = gen_msg_id()
        #
        if ConnectionPool.connections:
            for conn in ConnectionPool.connections:
                try:
                    conn.write_message(msg_content)
                except Exception as error:
                    logging.error(error)
            msg_status = 'sending'
        else:
            msg_status = 'unsend'

        msgDao = MessageDao()
        msgDao.save_message(msgid, appid, uid, msg_content, msg_status)
        self.write("ok")
