#coding=utf-8
import unittest
from qpush.models.app import AppDao
from qpush.utils.generateid import gen_app_id_and_key


class AppDaoTestCase(unittest.TestCase):
    def setUp(self):
        appDao = AppDao()
        self.appDao = appDao

    def test_get_appkey_by_appid(self):

        appid, appkey = gen_app_id_and_key()
        test_appkey = self.appDao.get_appkey_by_appid(appid)
        self.assertEqual(appkey, test_appkey)

        self.appDao.delete_app_by_appid(appid)
        test_appkey = self.appDao.get_appkey_by_appid(appid)
        self.assertEqual(None, test_appkey)

    def test_delete_app_by_appid(self):
        appid, appkey = gen_app_id_and_key()
        self.appDao.delete_app_by_appid(appid)

        test_appkey = self.appDao.get_appkey_by_appid(appid)
        self.assertEqual(None, test_appkey)


if __name__ == '__main__':
    unittest.main()
