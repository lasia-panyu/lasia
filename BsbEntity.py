# -- coding: utf-8 --
import  re
import MySQLdb
import threading
import sys
import json
from DBUtils.PooledDB import PooledDB

reload(sys)
sys.setdefaultencoding('utf8')

"""
 base基类,无固定参数
 制定设置 key为模板建议要求，value为属性值
 type   str   操作类型
 field  list  字段名称
 tb     str   数据库表名
 cause  map   where 附属条件
 page   int   页数条数
 curpage itn  选择页数

  {"type":'SELECT',"field":['name','desc'],"tn":'product',"cause":{"id":1}}
"""

pool = PooledDB(MySQLdb, 5, host='124.94.129.94', user='mibank_test', passwd='mibank_test', db='mibank_test', port=3306,charset="utf8")

class BsbEntity():
    threadList=[threading.Thread(name='bsbThread'+str(x)) for x in range(4)]
    regex = "(\\])|(\\[)|(\\')"


    def execSql(self, **kargs):
        print("begin")
        conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        cur = conn.cursor()
        dict1 = {}
        dict2 = {}
        cur.execute(self.toSql(**kargs))
        results = cur.fetchall()
        dict2 = {}
        for x in range(len(results)):
            dict1 = {}
            for y in range(len(results[x])):
                dict1[cur.description[y][0]] = str(results[x][y])
            print dict1
            dict2[x] = dict1
        cur.close()
        conn.close()
        return dict2

    def sqlFilter (self, fromregex, toregex, *args):
        print str(*args)
        return filter(lambda x: re.sub(fromregex,toregex , str(x)),str(*args))

    def mapToSql (self,wcause,  **kargs):
        if kargs:
            return ""
        else:
            print [' and ']+[str(k).replace("\\'", '') + " = \'" + str(v) + "\' " for k, v in kargs[wcause].iteritems()]
            return [' and ']+[str(k).replace("\\'", '') + " = \'" + str(v) + "\' " for k, v in kargs[wcause].iteritems()]

    def __init__(self, **kargs):
          self.baseMap=kargs

    # toSql : 转化为sql
    # type:操作类型
    # map{filed:list,tn:list,cause:map,fiedc:map}

    def toSql(self, **kargs):
        if kargs['type'] == 'SELECT':
            return "select %s from %s where 1=1 %s LIMIT %d,%d" % (self.sqlFilter(self.regex, '', kargs['field']),\
                                                          self.sqlFilter(self.regex, '', [kargs['tn']]),\
                                                         self.sqlFilter(self.regex, '', self.mapToSql("cause", **kargs)),\
                                                        kargs['page']*(kargs['curpage']-1),\
                                                       kargs['page']*(kargs['curpage'])\
                                                                   )
        if kargs['type'] == 'INSERT':
            return "insert into %s values (%s)"(filter(self.regex), '', kargs['tn'], \
                                                   filter(self.regex), '', self.mapToSql('cause',kargs))
        if kargs['type'] == 'UPDATE':
            return "update %s set %s where 1=1 %s"(filter(self.regex), '', kargs['tn'],\
                                                     filter(self.regex), '', self.mapToSql('fiedc',kargs),\
                                                    filter(self.regex), '', self.mapToSql('cause', kargs) )
        if kargs['type'] == 'DELETE':
            return "delete from %s where %s"(filter(self.regex), '', kargs['tn'], \
                                                filter(self.regex), '', self.mapToSql('cause', kargs))

"""
def a(sql):
    dict1 = {}
    dict2 = {}
    for x in range(len(sql)):
        dict1 = {}
        for y in range(len(sql[x])):
            dict1[cur.description[y][0]] = str(sql[x][y])
        print dict1
        dict2[x]=dict1
    print "ending"
    return dict2
conn = MySQLdb.Connect(host='124.94.129.94', user='mibank_test', passwd='mibank_test', db='mibank_test', port=3306,charset="utf8")
#conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
cur = conn.cursor()
cur.execute("select * from tb_account_info where 1=1  LIMIT 0,3")
print cur.description
results = cur.fetchall()

print a(results)
json_data = json.dumps(a(results))
print json_data
cur.close()
conn.close()
"""
