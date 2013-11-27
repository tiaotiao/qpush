#coding:utf-8
import json
import logging

from redis import Redis

from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler

from qpush.models.message import MessageInfoDao
from qpush.models.message import MessageContentDao
from qpush.models.message import TagDao
from qpush.utils.generateid import gen_msg_id
from qpush.conf import redis as rds_conf
from qpush.conf import MSG_QUEUE_MAX_LEN


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


class MessageQueue(object):
    queue = []

    @classmethod
    def msg_enqueue(cls, msg):
        cls.queue.append(msg)
        if len(cls.queue) > MSG_QUEUE_MAX_LEN:
            cls.queue = cls.queue[-MSG_QUEUE_MAX_LEN:]


class StatusHandler(WebSocketHandler):

    def open(self):
        ConnectionPool.add_conn(self)

    def on_message(self, raw_msg):
        msg = json.loads(raw_msg)
        if msg['action'] == 'online':
            #reqid = msg['reqid']
            appid = msg['appid']
            uid = msg['uid']
            device = msg['device']
            connid = msg['connid']

            rds = Redis(rds_conf['host'], rds_conf['port'], rds_conf['db'])
            devicekey = 'appid:%s:uid:%s:devices' % (appid, uid)
            connidkey = 'appid:%s:uid:%s:connids' % (appid, uid)
            rds.sadd(devicekey, device)
            rds.sadd(connidkey, connid)

        elif msg['action'] == 'offline':
            appid = msg['appid']
            uid = msg['uid']
            device = msg['device']
            connid = msg['connid']

            rds = Redis(rds_conf['host'], rds_conf['port'], rds_conf['db'])
            devicekey = 'appid:%s:uid:%s:devices' % (appid, uid)
            connidkey = 'appid:%s:uid:%s:connids' % (appid, uid)
            rds.srem(devicekey, device)
            rds.srem(connidkey, connid)

        elif msg['action'] == 'set_tags':
            appid = msg['appid']
            uid = msg['uid']
            tags = msg['tags']
            tagDao = TagDao()
            tagDao.set_tags(appid, uid, tags)

        elif msg['action'] == 'del_tags':
            appid = msg['appid']
            uid = msg['uid']
            tags = msg['tags']
            tagDao = TagDao()
            tagDao.del_tags(appid, uid, tags)

        elif msg['action'] == 'get_tags':
            appid = msg['appid']
            uid = msg['uid']
            tagDao = TagDao()
            tagDao.get_tags(appid, uid)

        else:
            logging.warning("unkown action: %s" % msg['action'])

    def on_close(self):
        ConnectionPool.remove_conn(self)


class MessageHandler(RequestHandler):
    def post(self):

        msg_content = self.get_argument('msg')
        appid = self.get_arguments('appid')
        uid = self.get_arguments('uid')
        msg_time = self.get_arguments('msg_time')
        reqid = self.get_argument('reqid')

        msgid = gen_msg_id()

        result = json.dumps({
            'action': 'push_msg',
            'reqid': reqid,
            'appid': appid,
            'msg_id': msgid,
            'msg_type': '',
            'msg_time': msg_time
        })

        MessageQueue.msg_enqueue(result)

        if ConnectionPool.connections:
            for conn in ConnectionPool.connections:
                try:
                    conn.write_message(result)
                except Exception as error:
                    logging.error(error)

        msgContentDao = MessageContentDao()
        msgContentDao.save_msg(msgid, msg_content)
        msgInfoDao = MessageInfoDao()
        msgInfoDao.create_msgInfo(msgid, appid, uid)
