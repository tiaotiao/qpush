import random
from string import letters
from string import digits

from redis import Redis

from qpush.conf import redis as rds_conf
from qpush.conf import INIT_AAPID
from qpush.conf import INIT_MSGID


def gen_msg_id():
    rds = Redis(rds_conf['host'], rds_conf['port'], rds_conf['db'])
    if rds.get("qpush:last_msgid") is None:
        rds.set("qpush:last_msgid", INIT_MSGID)

    return rds.incr('qpush:last_msgid')


def gen_app_id_and_key():
    rds = Redis(rds_conf['host'], rds_conf['port'], rds_conf['db'])
    if rds.get("qpush:last_appid") is None:
        rds.set("qpush:last_appid", INIT_AAPID)

    appid = rds.incr("qpush:last_appid")
    while rds.get("qpush:appid:%d:appkey" % appid):
        appid = rds.incr("last_appid")

    appkey = ''.join(random.choice(letters+digits) for i in range(40))

    rds.set("qpush:appid:%d:appkey" % appid, appkey)

    return appid, appkey

if __name__ == '__main__':
    i, k = gen_app_id_and_key()
