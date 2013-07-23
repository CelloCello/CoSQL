#!/usr/bin/env python
# -*- coding: utf-8 -*-


from cosql.manager import DBManager
from cosql.connector import DBConnector
from cosql.command import DBCommand
from cosql.command import db_checker
from cosql.sqlobject import SQLiteObject
from cosql.sqlobject import MySQLObject
from cosql.sqlobject import MsSQLObject

import sqlite3
import MySQLdb

# mosql
# from mosql.result import Model


# class MoSQLite(Model):
#     @classmethod
#     def getconn(cls):
#         return sqlite3.connect('test.db')

#     @classmethod
#     def putconn(cls, conn):
#         conn.close()

# class MoMySQL(Model):
#     @classmethod
#     def getconn(cls):
#         return MySQLdb.connect(user='cello', db='cello', passwd='cello', host='192.168.44.142')

#     @classmethod
#     def putconn(cls, conn):
#         conn.close()

# class MoTable(MoMySQL):
#     table = 'TestTable'


class SQLiteCmd(DBCommand):

    def GetMemData(self):
        rst = self.execcmd("select * from MemberData")
        #result = self.dbObj.fetchall()
        print "====MY_cmd_SQLite===="
        #mydata = MyData()
        #self.getOneData(mydata, result[0])
        # print vars(rst)
        # print "bbbbbbbb"
        # for dd in rst:
        #     print dd
        print vars(rst)

    @db_checker
    def insert(self):
       for i in xrange(10000):
        sql = "insert into [TestTable] (id,name,phone) values (%d, '%s', %d)" % (i, "cello_"+str(i), 100+i)
        #print sql
        self.execcmd(sql)   

    @db_checker
    def select(self):
        #self.execcmd("select * from TestTable where id = 9930 or id=5678 order by id")
        self.execcmd("SELECT * FROM TestTable WHERE id IN (9930, 5678) ORDER BY id")

class MySQLCmd(DBCommand):

    @db_checker
    def insert(self):
       for i in xrange(10000):
        sql = "insert into TestTable (id,name,phone) values (%d, '%s', %d)" % (i, "cello_"+str(i), 100+i)
        #print sql
        self.execcmd(sql)   

    @db_checker
    def select(self):
        #self.execcmd("select * from TestTable where id = 9930 or id=5678 order by id")
        self.execcmd("SELECT * FROM TestTable WHERE id IN (9930, 5678) ORDER BY id")

            

dbc_sqlite = DBConnector(host="test.db", maxline=1, sqltype=SQLiteObject, cmdtype=SQLiteCmd)
dbc_mysql = DBConnector(host="192.168.44.142",db="cello", user='cello', passwd='cello', maxline=1, sqltype=MySQLObject, cmdtype=MySQLCmd)

dbm = DBManager()
dbm.regConnector("sqlite", dbc_sqlite)
dbm.regConnector("mysql", dbc_mysql)
dbm.start()
#cmd = dbm.getCommand("sqlite")
#cmd.GetMemData()



conn = sqlite3.connect('test.db')
cur = conn.cursor()

def create_table():
    cur.execute("""create table [TestTable] 
        (serial integer primary key autoincrement,
         id int not null,
         name nvarchar(20),
         phone int not null default 0
        )""")

def org_sqlite_insert():
    for i in xrange(10000):
        sql = "insert into [TestTable] (id,name,phone) values (%d, '%s', %d)" % (i, "cello_"+str(i), 100+i)
        #print sql
        cur.execute(sql)   
        conn.commit() 

def org_sqlite_select():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    #cur.execute("select * from TestTable where id = 9930 or id=5678 order by id")
    cur.execute("SELECT * FROM TestTable WHERE id IN (9930, 5678) ORDER BY id")
    cur.fetchall()
    cur.close()
    conn.close()

def org_mysql_select():
    conn = MySQLdb.connect(host="192.168.44.142", db="cello", user="cello", passwd="cello")
    cur = conn.cursor()
    #cur.execute("select * from TestTable where id = 9930 or id=5678 order by id")
    cur.execute("SELECT * FROM TestTable WHERE id IN (9930, 5678) ORDER BY id")
    cur.fetchall()
    cur.close()
    conn.close()

def cosql_sqlite_insert():
    cmd = dbm.getCommand("sqlite")
    cmd.insert()

def cosql_sqlite_select():
    cmd = dbm.getCommand("sqlite")
    cmd.select()

def cosql_mysql_insert():
    cmd = dbm.getCommand("mysql")
    cmd.insert()

def cosql_mysql_select():
    cmd = dbm.getCommand("mysql")
    cmd.select()

def mosql_sqlite_select():
    MoTable.select(
        where    = {'id': (9930, 5678)},
        order_by = ('id',)
        )

def mosql_mysql_select():
    MoTable.select(
        where    = {'id': (9930, 5678)},
        order_by = ('id',)
        )


if __name__ == '__main__':

    #create_table()
    
    from timeit import timeit
    #print timeit(org_sqlite_insert, number=1)
    # > 1199.38689613
    #print timeit(cosql_sqlite_insert, number=1)
    # > 982.994023229
    #org_sqlite_insert()

    # sqlite
    print timeit(org_sqlite_select, number=10000)
    # > 23.1159019341
    print timeit(cosql_sqlite_select, number=10000)
    # > 15.0218633958
    #print timeit(mosql_sqlite_select, number=1000)

    # # mysql
    # # print timeit(cosql_mysql_insert, number=1)
    # print timeit(org_mysql_select, number=5000)
    # # > 41.8026446688
    # print timeit(cosql_mysql_select, number=5000)
    # # > 29.3979253909
    # print timeit(mosql_mysql_select, number=5000)
    # # > 44.2078964827

