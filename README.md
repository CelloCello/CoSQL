CoSQL
=====

Call SQL or dig SQL. (The pronunciation of 'co' means dig in Chinese. XD)


It helps you to manager the connection of SQL lib.	
You just connect once and reuse the DBCommand to do SQL things.

Features:

1. easy to use and light
2. high efficiency
3. thread safe
4. support sqlite¡Bmysql¡Bmssql ...

How to use
----------

here is an example of sqlite.	

import files:

	from cosql.manager import DBManager
	from cosql.connector import DBConnector
	from cosql.command import DBCommand
	from cosql.command import db_checker


You can select 'sqlobject' you like.	
SQLiteObject¡BMySQLObject¡BMsSQLObject...	


	from cosql.sqlobject import SQLiteObject


Make your own 'DBCommand':

	class SQLiteCmd(DBCommand):
	    @db_checker
	    def select(self):
	        return self.execcmd("SELECT * FROM TestTable WHERE id IN (9930, 5678) ORDER BY id")


Declare 'DBConnector' and register connector into 'DBManager'.	
Then 'start()' to start all connections.	

	dbc_sqlite = DBConnector(host="test.db", maxline=1, sqltype=SQLiteObject, cmdtype=SQLiteCmd)

	dbm = DBManager()
	dbm.regConnector("sqlite", dbc_sqlite)
	dbm.start()


Get command object and do what you want to do!	
Use 'getOne()' to get the data in the result list.	
The column name will become the attribute of the return object automaticlly.	

	cmd = dbm.getCommand("sqlite")
    rst = cmd.select().getOne(0)
    print rst.name

    cmd = dbm.getCommand("sqlite")
    rst = cmd.select()
    for i in xrange(rst.rowNum):
        print rst.getOne(0).name

Bugs:

- callproc() can't work in mssql