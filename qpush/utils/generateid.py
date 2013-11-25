from redis import Redis       
from qpush.conf import redis as rds

def gen_msg_id():
   r = Redis(rds['host'], rds['port'], rds['db'])
   return r.incr('msgid')
