#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The manager of sql connection and command.
"""

class DBManager:
	'''管理所有連線器用'''

	def __init__(self):
		self.conns = {}
		pass

	def regConnector(self, type, connector):
		self.conns[type] = connector
		pass

	def start(self):
		for k, v in self.conns.items():
			v.connect()
		
	def finish(self):
		for k, v in self.conns.items():
			v.close()

	def getCommand(self, type):
		conn = self.conns.get(type)
		if conn:
			return conn.getCommand()

		return None
