#!/usr/bin/env python
# encoding: utf-8
"""
dummynode.py

Copyright (c) 2011 Richard North. 
"""

class DummyNode:
	def __init__(self, name):
		print "Created DummyNode"
		self._name = name
		self.matches_called = False
		self.ssh_called = False
	
	def matches(self, name_or_tag):
		self.matches_called = True
		return name_or_tag == self._name
	
	def ssh(self,driver,conn):
		self.ssh_called = True
		return
