from binascii import unhexlify
from qpush.db.base import BaseDao
from qpush.db.sqlpool import escape


class TagError(Exception):
    pass


class TagDao(BaseDao):
    TABLE = 'qpush_tag'

    CREATE_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS `%s`(
    `appid` BINARY(16) NOT NULL,
    `tag_name` VARCHAR(64)  NOT NULL,
    `uid` VARCHAR(64)  NOT NULL,
     PRIMARY KEY (`appid`, `tag_name`, `uid`),
     KEY `index_name` (`tag_name`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8''' % TABLE

    def set_tags(self, appid, uid, tags):

        appid_bin = _hex2bin(appid)

        for tag_name in tags:
            self.sqlpool.execute(
                "INSERT INTO `qpush_tag` "
                "(`tag_name`, `appid`, `uid`) "
                " VALUES('%s', '%s', '%s')" % (
                    escape(tag_name),
                    escape(appid_bin),
                    escape(uid)
                )
            )

    def get_uids(self, appid, tag_name):

        appid_bin = _hex2bin(appid)

        resutls = self.sqlpool.query(
            "SELECT `uid` FROM `qpush_tag` "
            "WHERE `appid`='%s' "
            "AND `tag_name`='%s'" % (
                escape(appid_bin),
                escape(tag_name)
            ), 1)

        uids = [result['uid'] for result in resutls]
        return uids

    def remove_tag(self, appid, uid, tag_name):
        appid_bin = _hex2bin(appid)

        self.sqlpool.execute(
            "DELETE FROM `qpush_tag` WHERE `appid`='%s' "
            "AND `uid`='%s' "
            "AND `tag_name`='%s' " % (
                escape(appid_bin),
                escape(uid),
                escape(tag_name))
        )


def _hex2bin(appid):
    try:
        appid_bin = unhexlify(appid)
        return appid_bin
    except TypeError:
        raise TagError("invalid appid")
