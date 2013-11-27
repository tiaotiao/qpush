from qpush.conf import pushservers
from binascii import crc32


def get_pushserver(appid, uid):
    key = crc32("%s%s" % (appid, uid))
    index = key % len(pushservers)
    return pushservers[index]
