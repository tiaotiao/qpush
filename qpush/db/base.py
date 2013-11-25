from qpush.db.sqlpool import SqlPool
from qpush.conf import db


class DaoMetaClass(type):
    def __init__(cls, name, bases, attrs):
        if cls.CREATE_TABLE_SQL is not None:
            cls.sqlpool.execute(cls.CREATE_TABLE_SQL)
        type.__init__(cls, name, bases, attrs)


class BaseDao(object):

    __metaclass__ = DaoMetaClass

    CREATE_TABLE_SQL = None

    sqlpool = SqlPool(
        host=db['host'],
        port=db['port'],
        db=db['name'],
        user=db['user'],
        passwd=db['password'],
    )
