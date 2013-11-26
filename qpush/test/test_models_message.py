# coding=utf-8
import unittest
from qpush.models.message import MessageInfoDao
from qpush.models.message import MessageContentDao
from qpush.utils.generateid import gen_app_id_and_key
from qpush.utils.generateid import gen_msg_id


class MessageInfoDaoTestCase(unittest.TestCase):

    def setUp(self):
        msgInfoDao = MessageInfoDao()
        self.msgInfoDao = msgInfoDao

    def test_creat_msgInfo(self):
        appid, _ = gen_app_id_and_key()
        msgid = gen_msg_id()
        self.msgInfoDao.create_msgInfo(msgid, appid, "test")


    def test_update_msg_status(self):
        appid, _ = gen_app_id_and_key()
        msgid = gen_msg_id()
        self.msgInfoDao.create_msgInfo(msgid, appid, "test")
        self.msgInfoDao.update_msg_status(msgid, "success")

class MessageContentDaoTestCase(unittest.TestCase):
    def setUp(self):
        msgContentDao = MessageContentDao()
        self.msgContentDao = msgContentDao


if __name__ == "__main__":
    unittest.main()
