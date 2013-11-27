#coding=utf-8
from redis import Redis

from qpush.conf import redis as rds_conf


class AppDao(object):
    def get_appkey_by_appid(self, appid):
        rds = Redis(rds_conf['host'], rds_conf['port'], rds_conf['db'])

        return rds.get("qpush:appid:%d:appkey" % appid)

    def delete_app_by_appid(self, appid):
        rds = Redis(rds_conf['host'], rds_conf['port'], rds_conf['db'])

        return rds.delete("qpush:appid:%d:appkey" % appid)
