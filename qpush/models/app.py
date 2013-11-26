#coding=utf-8
from qpush.db.base import BaseDao
from qpush.db.sqlpool import escape
from binascii import hexlify
from binascii import unhexlify


class AppError(Exception):
    pass


class AppExits(AppError):
    pass


class AppNotFound(AppError):
    pass


class AppDao(BaseDao):
    TABLE = 'qpush_app'

    CREATE_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS `%s`(
    `appid` BINARY(16) NOT NULL,
    `appkey` BINARY(8) NOT NULL,
    `appname` VARCHAR(64) DEFAULT '',
    `appdecs` VARCHAR(300) DEFAULT '',
     PRIMARY KEY (`appid`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8''' % TABLE

    def create_app(self, appid, appkey):
        u'''创建app,成功返回`appid`'''

        try:
            appid_bin = unhexlify(appid)
            appkey_bin = unhexlify(appkey)
        except TypeError:
            raise AppError("invalid appid or appkey")

        result = self.sqlpool.execute(
            "INSERT INTO `qpush_app` "
            "(appid, appkey) "
            "VALUES('%s', '%s')"
            % (escape(appid_bin), escape(appkey_bin))
        )

        if result == -2:
            raise AppExits

    def get_appkey_by_appid(self, appid):
        try:
            appid_bin = unhexlify(appid)
        except TypeError:
            raise AppError('invalid appid')
        result = self.sqlpool.query(
            "SELECT HEX(appkey)"
            "FROM `qpush_app`"
            "WHERE `appid`='%s'" % escape(appid_bin))

        if result:
            return result[0][0].lower()
        raise AppNotFound("no app found with appid: %s" % appid)

    def delete_app_by_appid(self, appid):
        try:
            appid_bin = unhexlify(appid)
        except TypeError:
            raise AppError('invalid appid')
        resutl = self.sqlpool.execute(
            "DELETE FROM `qpush_app`"
            "WHERE `appid`='%s'" % escape(appid_bin)
        )
        if resutl == 0:
            raise AppNotFound


if __name__ == '__main__':
    a = AppDao()
    b = AppDao()
    print a is b
    print a.create_app is b.create_app
    print a.create_app is AppDao.create_app
