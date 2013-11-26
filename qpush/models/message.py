from binascii import unhexlify
from qpush.db.base import BaseDao
from qpush.db.sqlpool import escape


class MessageError(Exception):
    pass


class MessageExists(MessageError):
    pass


class MessageNotFound(MessageError):
    pass


class MessageInfoDao(BaseDao):
    TABLE = 'qpush_message_info'

    CREATE_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS `%s`(
    `msgid` INT(11) UNSIGNED  NOT NULL,
    `appid` BINARY(16) NOT NULL,
    `uid` VARCHAR(64)  NOT NULL,
    `status` enum('fail', 'success') DEFAULT 'fail',
     PRIMARY KEY (`msgid`),
     KEY `index_appid_uid` (`appid`, `uid`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8''' % TABLE

    def create_msgInfo(self, msgid, appid, uid):
        appid_bin = unhexlify(appid)
        self.sqlpool.execute(
            "INSERT INTO `qpush_message_info` "
            "(`msgid`, `appid`, `uid`) "
            "VALUES (%d, '%s', '%s') " % (
                msgid, escape(appid_bin), escape(uid))
        )

    def update_msg_status(self, msgid, status):
        self.sqlpool.execute(
            "UPDATE `qpush_message_info` "
            "SET `status`='%s' "
            "WHERE `msgid`=%d " % (
                escape(status),
                msgid
             )
        )

   # def get_last_msgid(self):
   #     result = self.sqlpool.query(
   #         "SELECT LAST(`msgid`)"
   #         "FROM `qpush_message_info` "
   #     )

   #     return result[0][0]


class MessageContentDao(BaseDao):
    TABLE = 'qpush_message_content'
    CREATE_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS `%s`(
    `msgid` INT(11) UNSIGNED  NOT NULL,
    `msg_content` VARCHAR(300) NOT NULL,
     PRIMARY KEY (`msgid`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8''' % TABLE

    def save_msg(self, msgid, msg_content):
        self.sqlpool.execute(
            "INSERT INTO `qpush_message_content` "
            "(`msgid`, `msg_content`) "
            "VALUES(%d, '%s')" % (msgid, msg_content)
        )
