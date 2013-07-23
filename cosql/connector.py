#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    
"""
from threading import Lock

class DBConnector:
	'''連線器
		可設定連線數量
		一個連線器會有一個Command
	'''

	def __init__(self, host="", db="", user="", passwd="", maxline=0, sqltype=None, cmdtype=None):
		self.host = host 	# 連線位置
		self.db = db 		# 資料庫
		self.user = user
		self.passwd = passwd
		self.maxline = maxline 	# 要建立的命令數量
		self.commands = []
		self.lock = Lock()
		for i in xrange(maxline):
			newCmd = cmdtype()
			newCmd.dbObj = sqltype()
			newCmd.connector = self

			# 可以執行的命令列
			self.commands.append(newCmd)

	def connect(self):
		for cmd in self.commands:
			cmd.dbObj.connect(self.host, self.db, self.user, self.passwd)

	def close(self):
		for cmd in self.commands:
			cmd.close()

	def getCommand(self):
		'''取得一個可執行的命令
			thread safe
		'''
		outCmd = None
		self.lock.acquire()
		for cmd in self.commands:
			if cmd.isUse == False:
				cmd.isUse = True
				outCmd = cmd
				break
		self.lock.release()
		return outCmd

	def commandFini(self, cmd):
		'''歸還已經用完的命令
			thread safe
		'''
		self.lock.acquire()
		cmd.isUse = False
		self.lock.release()


