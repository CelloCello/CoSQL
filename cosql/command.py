#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   
"""

class OneResult:
	'''一筆資料'''
	def __init__(self):
		pass


class Result:
	'''查詢後的結果'''
	def __init__(self):
		self.cols = []
		self.colNum = 0
		self.rowNum = 0

	# def __getitem__(self, idx):
	# 	name = self.cols[idx]
	# 	return self.__dict__[name]

	# def __iter__(self):
	# 	return (name for name in self.cols)

	def getOne(self, idx, data=None):
		if self.rowNum <= 0:
			return None

		rst = data
		if rst == None:
			rst = OneResult()
		for col in self.cols:
			rst.__dict__[col] = self.__dict__[col][idx]
		return rst

	def getColumn(self, name):
		return self.__dict__[name]


def db_checker(fn):
	'''監視器 decor, 可以回收命令'''
	def wrapper(self, *args):
		rst = fn(self, *args)
		self.connector.commandFini(self)
		return rst
	return wrapper
	

class DBCommand:
	'''表示要做的事'''

	def __init__(self):
		self.dbObj = None
		self.isUse = False
		self.connector = None

	def execcmd(self, cmd):
		self.dbObj.execcmd(cmd)
		#self.dbObj.cmdObj.callproc(cmd, ())
		rst = Result()

		# name to param
		cmdObj = self.dbObj.cmdObj
		if cmdObj.rowcount == 0 or cmdObj.description is None:
			return None
		rst.cols = [name[0].lower() for name in cmdObj.description]
		for name in cmdObj.description:
			rst.__dict__[name[0].lower()] = []
			rst.colNum += 1

		for dataRow in cmdObj:
			rst.rowNum += 1
			for idx, name in enumerate(rst.cols):
				rst.__dict__[name].append(dataRow[idx])

		cmdObj.close()
		return rst

	def callproc(self, proc, param=None):
		self.dbObj.callproc(proc, param)
		rst = Result()

		# name to param
		cmdObj = self.dbObj.cmdObj
		#print cmdObj.fetchall()
		#print cmdObj.description
		rst.cols = [name[0].lower() for name in cmdObj.description]
		for name in cmdObj.description:
			rst.__dict__[name[0].lower()] = []
			rst.colNum += 1

		for dataRow in cmdObj:
			rst.rowNum += 1
			for idx, name in enumerate(rst.cols):
				rst.__dict__[name].append(dataRow[idx])

		cmdObj.close()
		return rst
