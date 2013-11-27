#coding:utf-8
import time
import urllib
import logging

from tornado.websocket import WebSocketHandler
from tornado.httpclient  import AsyncHTTPClient

from qpush.models.tag import TagDao
from qpush.utils.getserver import get_pushserver
from qpush.conf import pushservers

def handler_request(response):
    pass

class PublishHandler(WebSocketHandler):

    def open(self):
        pass

    def on_message(self, raw_msg):
        msg = json.loads(raw_msg)
        if msg['action'] = 'publish_msg':
            reqid = msg['reqid']
            appid = msg['appid']
            msg_content = msg['msg']
            tags = msg['tags']
            uids = msg['uids']
            dest_device = msg['dest-device']
            msg_time = int(time.time()
            tagDao = TagDao()
            uids = tagDao.get_uids(appid, tags)

            httpclient = AsyncHTTPClient()

            pushserver_uids_dict = {}

            for uid in uids:
                pushserver = get_pushserver(appid, uid)
                if pushserver_uids_dict.get(pushserver) is None:
                    pushserver_uids_dict[pushserver] = []
                pushserver_uids_dict[pushserver].append(uid)

            for pushserver in pushservers:
                uids = pushserver_uids_dict[pushserver]
                post_data = {
                    'msg': msg_content,
                    'appid': appid,
                    'uids': uids,
                    'msg_time': msg_time,
                    'reqid': reqid
                }
                body = urllib.urlencode(post_data)

                httpclient.fetch("http://%s/msg",
                    handler_request,
                    method='POST',
                    headers=None,
                    body=body)

        else:
            logging.warning("unkown action : %s" % msg['action'])

    def on_close(self):
        pass
