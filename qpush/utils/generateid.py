import random
from uuid import uuid1
from string import hexdigits
from redis import Redis
from qpush.conf import redis as rds


def gen_msg_id():
    r = Redis(rds['host'], rds['port'], rds['db'])
    return r.incr('msgid')


def gen_app_id_and_key():
    appid = uuid1().hex

    lowcase_hexdigits = hexdigits[:16]
    appkey = ''.join(random.choice(lowcase_hexdigits) for i in range(16))

    return appid, appkey

if __name__ == '__main__':
    print gen_app_id_and_key()
