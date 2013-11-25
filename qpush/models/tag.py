from qpush.db.base import BaseDao
from qpush.db.sqlpool import escape


class TagDAO(BaseDao):
    TABLE = 'qpush_tag'

    CREATE_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS `%s`(
    `name` VARCHAR(30)  NOT NULL,
    `appid` INT(11) NOT NULL,
    `uid` INT(11)  NOT NULL,
     KEY `index_name` (`name`),
     KEY `index_appid_uid` (`appid`, `uid`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8''' % TABLE

    def set_tags(self, appid, uid, tags):
        for tag in tags:
            self.sqlpool.execute("INSERT INTO `qpush_tag` VALUES(%s, %d, %d)" % escape(tag), appid, uid)

    def get_appid_uid_pairs(self, tag):
        self.sqlpool.query("SELECT `appid`, `uid` FROM `qpush_tag` WHERE name='%s'" % tag)
