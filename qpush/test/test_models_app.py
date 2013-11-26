#coding=utf-8
import unittest
from qpush.models.app import AppDao
from qpush.models.app import AppError
from qpush.models.app import AppExits
from qpush.models.app import AppNotFound
from qpush.utils.generateid import gen_app_id_and_key


class AppDaoTestCase(unittest.TestCase):
    def setUp(self):
        appDao = AppDao()
        self.appDao = appDao

    def test_create_app(self):
        appid, appkey = gen_app_id_and_key()
        self.appid = appid
        self.appDao.create_app(appid, appkey)

        try:
            self.appDao.create_app(appid, appkey)
            assert False, "never goes here"
        except AppExits:
            pass

        try:
            self.appDao.create_app("1234x", "xyz")
            assert False, "never goes here"
        except AppError as error:
            self.assertEqual(error.message, "invalid appid or appkey")

        self.appDao.delete_app_by_appid(self.appid)

    def test_get_appkey_by_appid(self):

        appid, appkey = gen_app_id_and_key()
        self.appid = appid
        self.appDao.create_app(appid, appkey)

        test_appkey = self.appDao.get_appkey_by_appid(appid)
        self.assertEqual(test_appkey, appkey)

        appid, _ = gen_app_id_and_key()
        try:
            test_appkey = self.appDao.get_appkey_by_appid(appid)
            assert False, "never goes here"
        except AppNotFound:
            pass

        try:
            self.appDao.get_appkey_by_appid('abcdf')
            assert False, "never goes here"
        except AppError as error:
            self.assertEqual(error.message, "invalid appid")

        self.appDao.delete_app_by_appid(self.appid)

    def test_delete_app_by_appid(self):
        appid, appkey = gen_app_id_and_key()
        self.appDao.create_app(appid, appkey)

        self.appDao.delete_app_by_appid(appid)

        try:
            self.appDao.delete_app_by_appid(appid)
            assert False, "never goes here"
        except AppNotFound:
            pass

        try:
            self.appDao.delete_app_by_appid("xxx")
            assert False, "never goes here"
        except AppError as error:
            self.assertEqual(error.message, "invalid appid")

if __name__ == '__main__':
    unittest.main()
