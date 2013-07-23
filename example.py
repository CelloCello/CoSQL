#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cosql.manager import DBManager
from cosql.connector import DBConnector
from cosql.command import DBCommand
from cosql.command import db_checker
from cosql.sqlobject import SQLiteObject

class SQLiteCmd(DBCommand):

    @db_checker
    def select(self):
        #self.execcmd("select * from TestTable where id = 9930 or id=5678 order by id")
        return self.execcmd("SELECT * FROM TestTable WHERE id IN (9930, 5678) ORDER BY id")
            

dbc_sqlite = DBConnector(host="test.db", maxline=1, sqltype=SQLiteObject, cmdtype=SQLiteCmd)
dbm = DBManager()
dbm.regConnector("sqlite", dbc_sqlite)
dbm.start()

def cosql_sqlite_select():
    cmd = dbm.getCommand("sqlite")
    return cmd.select().getOne(0)

if __name__ == '__main__':

    rst = cosql_sqlite_select()
    print rst.id

    cmd = dbm.getCommand("sqlite")
    rst = cmd.select()
    for i in xrange(rst.rowNum):
        print rst.getOne(0).name

