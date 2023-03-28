import MySQLdb
import sys
from .globalobjs import *
import logging

logger = logging.getLogger(__name__)

class DbTool:

    def __init__(self, host=host, root=root, pwd=pwd, db_name=db_name):
        try:
            logging.info("host:%s, root:%s, pwd:%s, db_name:%s" % (host, root, pwd, db_name))
            self.db = MySQLdb.connect(host, root, pwd, db_name, charset='utf8')
        except BaseException as e:
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)


    def select(self, sql, result):
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            # total row number
            # print 'row_count', cursor.rowcount
            while True:
                # current row number
                # print 'row_number', cursor.rownumber
                data = cursor.fetchone()
                if data is not None:
                    # print data
                    result.append(data)
                else:
                    break
        except BaseException as e:
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)


    def update(self, sql):
        try:
            cursor = self.db.cursor()
            num = cursor.execute(sql)
            self.db.commit()
            return num
        except BaseException as e:
            self.db.rollback()
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)
            return 0
        pass

    def close(self):
        try:
            self.db.close()
        except BaseException as e:
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)

    @staticmethod
    def checkParam(param):
        try:
            param = str(param).upper()
            if param.find('OR') != -1 or param.find('AND') != -1 or param.find('=') != -1 \
                    or param.find('DELETE') != -1 or param.find('DROP') != -1 \
                    or param.find('SELECT') != -1 or param.find('WHERE') != -1 \
                    or param.find('UPDATE') != -1 or param.find('INSERT') != -1 \
                    or param.find('(') != -1 or param.find(')') != -1 or param.find('LIKE') != -1:
                logging.error('异常，检测到 Sql 注入:')
                logging.error(param)
                return False
            else:
                return True
            pass
        except BaseException as e:
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)
            return False

def main():
    db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name)
    result = []
    db.select('select * from water_base', result)
    print(result)
    db.close()
    pass



if __name__ == '__main__':
    main()
    pass