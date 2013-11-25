#!/usr/bin/python
# _*_ coding: UTF-8 _*_
# Author: TooNTonG
# Created on 2010-2-25
#
'''
mysql 数据库线程连接池，每线程一个连接
'''

import _mysql
import time, logging
import threading
from _mysql_exceptions import IntegrityError, OperationalError
from threading import current_thread


def escape(var):
    '''这里假定连接数据库都是使用utf8的。'''
    if var is None:
        return ''
    if isinstance(var, unicode):
        var = var.encode('utf8')
    if not isinstance(var, str):
        var = str(var)
    return _mysql.escape_string(var)

class _SqlConn():
    def __init__(self, conn, owner):
        '''应该由SqlPool的getConn方法去初始化本类'''
        self.conn = conn
        self.owner = owner

    def __del__(self):
        self.close()

    def _affectRows(self):
        '''查看最后一次query影响几行数据.'''
        r = self.conn.affected_rows()
        #TODO 这个值与驱动、系统、硬件CPU位数都可能有关
        if r == 0xFFFFFFFFFFFFFFFF: #64位的-1
            return 0
        return r

    def execute(self, sql):
        '''@return: 成功返回影响行数,失败返回 小于零的整数.-2为主键冲突,其它负数未定义错误类型.'''
        try:
            self.conn.query(sql)
            return self._affectRows()
        except IntegrityError, e:
            return (SqlPool.KEY_ERROR) #发生主键冲突
        except Exception, e:
            logging.error('%s - %s' % (e, sql))
            print e, sql
            raise e # SQL 异常

    def query(self, sql, how = 0):
        '''执行一条查询的SQL语句，返回查询结果,也可以马上调用result方法对能取得. 每次的query对应一次的result.
        @param how:
            0 -- tuples (default), RET_TUPLE
            1 -- dictionaries, key=column or table.column if duplicated
            2 -- dictionaries, key=table.column.'''
        #assert (sql).lower().startswith("select") == True or (sql).lower().startswith("show") == True, 'must readonly query.'
        try:
            self.conn.query(sql)
            res = self.conn.store_result()
            if res:
                return res.fetch_row(res.num_rows(), how)
            else:
                return ()
        except Exception, e:
            logging.error('%s - %s' % (e, sql))
            raise e # SQL 异常

    def close(self):
        '''关闭连接'''
        self.owner.close(self)
        self.conn = None

class SqlPool(threading.Thread):
    '''全局线程变量，继承于local类'''
    KEY_ERROR = -2
    RET_TUPLE = 0
    RET_DICT_ROW_FOR_KEY = 1
    RET_DICT_TABLE_ROW_FOR_KEY = 2

    def __init__(self, host, user, passwd, db, port = 18889):
        threading.Thread.__init__(self, target = self._threadChecker, name = 'sqlpool')
        self._db = db
        self._host = host
        self._user = user
        self._passwd = passwd
        self._port = int(port)
        self._chkThread = None
        self._connect_pool = {}
        self.setDaemon(True)

    def _startChkThread(self):
        for thread in threading.enumerate():
            if thread.getName() == self.getName():
                return self
        else:
            self.start()
            return self

    def _threadChecker(self):
        while True:
            for thread in threading.enumerate():
                if self._connect_pool.has_key(thread.ident) \
                    and not thread.isAlive():
                    self._connect_pool.pop(thread.ident)
            time.sleep(30 * 60)

    def _valid_connection(self):
        if self._connect_pool.get(current_thread().ident) is not None:
            try:
                self._connect_pool[current_thread().ident].ping()
                return True
            except:
                self._connect_pool[current_thread().ident].close()
                self._connect_pool[current_thread().ident] = None
        return False

    def reconnect(self):
        self._connect_pool[current_thread().ident] = _mysql.connect(
            db = self._db,
            host = self._host,
            user = self._user,
            passwd = self._passwd,
            port = self._port)
        self._connect_pool[current_thread().ident].set_character_set('utf8')

    def getConn(self):
        '''获取连接'''
        if not self._valid_connection():
            self.reconnect()
        return _SqlConn(self._connect_pool[current_thread().ident], self)

    def close(self, conn):
        '''关闭连接'''

    def execute(self, sql):
        '''执行语句, 返回影响行数'''
        if self._chkThread is None:
            self._chkThread = True
            self._startChkThread()

        conn = self.getConn()
        try:
            return conn.execute(sql)
        except OperationalError, e:
            if e[0] == 2013 or e[0] == 2006:  # (2006, 'MySQL server has gone away')
                self.reconnect()              # (2013, 'Lost connection to MySQL server during query')
                return self.getConn().execute(sql)
            else:
                logging.error('%s - %s' % (e, sql))
                raise e

    def executeReturnInsertId(self, sql):
        '''执行语句, 返回影响行数及LAST_INSERT_ID'''
        if self._chkThread is None:
            self._chkThread = True
            self._startChkThread()

        conn = self.getConn()
        
        #execute sql
        insertResult = None
        try:
            insertResult = conn.execute(sql)
        except OperationalError, e:
            if e[0] == 2013 or e[0] == 2006:  # (2006, 'MySQL server has gone away')
                self.reconnect()              # (2013, 'Lost connection to MySQL server during query')
                conn = self.getConn()
                insertResult = conn.execute(sql)
            else:
                logging.error('%s - %s' % (e, sql))
                raise e
            
        if insertResult < 1:
            conn.close()
            return (insertResult, 0)
        
        # get id
        ''' NOTICE: 必须使用同一个conn调用LAST_INSERT_ID()。
                    为了兼容mysql-proxy, LAST_INSERT_ID和insert语句之间不能插入其他任何语句。
        '''
        try:
            retData = conn.query('SELECT LAST_INSERT_ID()', 0)
        except OperationalError, e:
            logging.error('%s - %s, LAST_INSERT_ID()' % (e, sql))
            raise e
            
        conn.close()
        
        # ok
        insertId = retData[0][0]
        return (insertResult, int(insertId))

    def query(self, sql, how = 0):
        '''执行语句，返回查询结果'''
        if self._chkThread is None:
            self._chkThread = True
            self._startChkThread()

        sqlConn = self.getConn()
        try:
            retData = sqlConn.query(sql, how)
        except OperationalError, e:
            if e[0] == 2013 or e[0] == 2006:  # (2006, 'MySQL server has gone away')
                self.reconnect()              # (2013, 'Lost connection to MySQL server during query')
                sqlConn = self.getConn()
                retData = sqlConn.query(sql, how)
            else:
                logging.error('%s - %s' % (e, sql))
                raise e
        sqlConn.close()
        return retData

class SqlUtil:
    @staticmethod
    def getFieldsDefaultValue(sqlPool, table):
        res = sqlPool.query('desc %s;' % table, SqlPool.RET_DICT_ROW_FOR_KEY)
        if res:
            defVals = {}
            for row in res:
                if row['Extra'] == 'auto_increment':
                    continue
                
                field, defVal, fieldType = row['Field'], row['Default'], row['Type'].lower()
                if defVal != None:
                    res = sqlPool.query('select default(`%s`) as df from %s limit 1;' % (field, table), 
                                            SqlPool.RET_DICT_ROW_FOR_KEY)
                    defVal = res[0]['df'] if res else defVal
                
                # caution ! here may cause bugs ...
                if (defVal is None) and row['Null'] == 'NO' and fieldType.find('char') != 0:
                    defVal = ''
                elif defVal is not None:
                    if fieldType.find('int') != -1: defVal = int(defVal)
                
                defVals[row['Field']] = defVal
            
            return defVals

# 每一个Dao都设一个假cache，如果使用memcache，在__initialize__时
class FakeCache(object):
    def get(self, key):
        return None
    def set(self, key, val, time = 0):
        return None
    def delete(self, key):
        return None

class DaoBase():
    def __init__(self, host, username, password, database, table):
        self._table = escape(table)
        self._sqlpool = SqlPool(host, username, password, database)
        self.cache = FakeCache()

    def dropTable(self):
        self._sqlpool.execute('DROP TABLES IF  EXISTS `%s`;' % self._table)

    def deploy(self):
        return self._sqlpool.execute(self._getTableStruct() % self._table)

if __name__ == '__main__':

    pool = SqlPool(
        host = '10.20.188.112',
        port = 3306,
        user = 'qing',
        passwd = 'admin',
        db = 'qing')


    print pool.query('show tables', SqlPool.RET_DICT_ROW_FOR_KEY)

    print pool.query('select * from qing_group limit 1', 1)

    for i in range(0, 1):
        print i
