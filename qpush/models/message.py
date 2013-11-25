from qpush.db.base import BaseDao
from qpush.db.sqlpool import escape


class MessageDao(BaseDao):
    TABLE = 'qpush_message'

    CREATE_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS `%s`(
    `msgid` INT(11)  NOT NULL,
    `appid` INT(11) NOT NULL,
    `senderid` INT(11)  NOT NULL,
    `tag_name` VARCHAR(30) NOT NULL,
    `content` varchar(240) NOT NULL,
    `status` enum('sending', 'unsend', 'recieved'),
     PRIMARY KEY (`msgid`),
     KEY `index_appid_senderid` (`appid`, `senderid`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8''' % TABLE

    def save_message(self, msgid, senderid, appid, tag_name, content, status):
        self.sqlpool.execute('insert into `qpush_message` (%d, %d, %d, %s, %s, %s)' % (
            msgid,
            senderid,
            appid,
            escape(tag_name),
            escape(content),
            escape(status))
        )

    def delete_message_by_id(self, msgid):
        self.sqlpool.execute('DELETE from `qpush_message` WHERE `id`=%s' % msgid)
