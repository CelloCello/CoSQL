#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   SQLObject
   ~~~~~~~~~

   To descript how to connect、close、exec ... in every kind of SQL service.
   Now support SQLite、MySQL、MS-SQL 
"""


import MySQLdb
import sqlite3
import pymssql


class SQLObject:
	'''The object to descript the way of connect and execute.'''

	def __init__(self):
		self.connObj = None
		self.cmdObj = None
		pass

	def connect(self, host="", db="", user="", passwd=""):
		pass

	def close(self):
		pass

	# def fetchone(self):
	# 	pass

	# def fetchall(self):
	# 	pass

	def execcmd(self, cmd):
		pass
	def callproc(self, proc, param=None):
		pass


class SQLiteObject(SQLObject):

	def connect(self, host="", db="", user="", passwd=""):
		self.connObj = sqlite3.connect(host)

	def close(self):
		self.cmdObj.close()

	# def fetchall(self):
	# 	return self.cmdObj.fetchall()

	def execcmd(self, cmd):
		self.cmdObj = self.connObj.cursor()
		self.cmdObj.execute(cmd)
		self.connObj.commit()

	def callproc(self, proc, param=None):
		self.cmdObj = self.connObj.cursor()
		self.cmdObj.callproc(proc, param)
		

class MySQLObject(SQLObject):

	def connect(self, host="", db="", user="", passwd=""):
		self.connObj = MySQLdb.connect(host=host, db=db, user=user, passwd=passwd)

	def close(self):
		self.cmdObj.close()

	# def fetchall(self):
	# 	return self.cmdObj.fetchall()

	def execcmd(self, cmd):
		self.cmdObj = self.connObj.cursor()
		self.cmdObj.execute(cmd)
		self.connObj.commit()

	def callproc(self, proc, param=None):
		self.cmdObj = self.connObj.cursor()
		self.cmdObj.callproc(proc, param)

class MsSQLObject(SQLObject):

	def connect(self, host="", db="", user="", passwd=""):
		self.connObj = pymssql.connect(host=host, database=db, user=user, password=passwd, as_dict=True)
		self.cmdObj = self.connObj.cursor()

	def close(self):
		self.cmdObj.close()

	# def fetchall(self):
	# 	return self.cmdObj.fetchall()

	def execcmd(self, cmd):
		self.cmdObj = self.connObj.cursor()
		self.cmdObj.execute(cmd)
		self.cmdObj.commit()

	def callproc(self, proc, param=None):
		self.cmdObj = self.connObj.cursor()
		self.cmdObj.callproc(proc, param)