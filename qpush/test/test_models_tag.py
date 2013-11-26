# coding=utf-8
import unittest
from qpush.models.tag import TagDao
from qpush.models.tag import TagError
from qpush.models.tag import _hex2bin
from qpush.utils.generateid import gen_app_id_and_key


class TagDaoTestCase(unittest.TestCase):

    def setUp(self):
        tagDao = TagDao()
        self.tagDao = tagDao

    def test_get_uids(self):
        appid, _ = gen_app_id_and_key()
        self.tagDao.set_tags(appid, "test1", ["tag1", "tag2"])
        self.tagDao.set_tags(appid, "test2", ["tag2", "tag3"])

        uids = self.tagDao.get_uids(appid, "tag1")
        self.assertEqual(uids, ["test1"])

        uids = self.tagDao.get_uids(appid, "tag2")
        self.assertEqual(uids, ["test1", "test2"])

        uids = self.tagDao.get_uids(appid, "tag3")
        self.assertEqual(uids, ["test2"])

        uids = self.tagDao.get_uids(appid, "tag4")
        self.assertEqual(uids, [])

        self.tagDao.remove_tag(appid, "test1", "tag1")
        self.tagDao.remove_tag(appid, "test1", "tag2")
        self.tagDao.remove_tag(appid, "test2", "tag2")
        self.tagDao.remove_tag(appid, "test2", "tag3")

    def test_set_tags(self):
        appid, _ = gen_app_id_and_key()
        self.tagDao.set_tags(appid, "test1", ["tag1", "tag2"])
        self.tagDao.set_tags(appid, "test1", ["tag1", "tag3"])
        self.tagDao.set_tags(appid, "test2", ["tag2", "tag3"])

        uids = self.tagDao.get_uids(appid, "tag1")
        self.assertEqual(uids, ["test1"])

        uids = self.tagDao.get_uids(appid, "tag2")
        self.assertEqual(uids, ["test1", "test2"])

        uids = self.tagDao.get_uids(appid, "tag3")
        self.assertEqual(uids, ["test1", "test2"])

        self.tagDao.remove_tag(appid, "test1", "tag1")
        self.tagDao.remove_tag(appid, "test1", "tag2")
        self.tagDao.remove_tag(appid, "test1", "tag3")
        self.tagDao.remove_tag(appid, "test2", "tag2")
        self.tagDao.remove_tag(appid, "test2", "tag3")

    def test_remove_tag(self):
        appid, _ = gen_app_id_and_key()
        self.tagDao.set_tags(appid, "test1", ["tag1", "tag2"])

        self.tagDao.remove_tag(appid, "test1", "tag1")

        uids = self.tagDao.get_uids(appid, "tag1")
        self.assertEqual(uids, [])

        uids = self.tagDao.get_uids(appid, "tag2")
        self.assertEqual(uids, ["test1"])

        self.tagDao.remove_tag(appid, "test1", "tag2")

    def test_hex2bin(self):
        result = _hex2bin("abcdef")
        self.assertEqual("\xab\xcd\xef", result)

        try:
            _hex2bin("x")
            assert False, "never goes here"
        except TagError:
            pass

if __name__ == "__main__":
    unittest.main()
