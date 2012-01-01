#!/usr/bin/env python
# encoding: utf-8
"""
test_load_balancer.py

Created by Richard North on 2011-12-30.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os

from blitzem.model import LoadBalancer
from blitzem.test.dummies import DummyDriver, DummyConn

if sys.version_info < (2, 7):
	import unittest2 as unittest 
else:
	import unittest

class TestLoadBalancer(unittest.TestCase):

	def setUp(self):
		self.driver = DummyDriver()

	def create_dummies(self, lb_name, lb_exists=False):
		self.lb = LoadBalancer(	name=lb_name, 
							applies_to_tag=["tag1"])
		self.conn = DummyConn(lb_name, lb_exists)

	# def test_up(self):
	# 	self.create_dummies("lbtocreate", lb_exists=False)
	# 	
	# 	self.lb.up(self.driver, self.driver, self.conn)
	# 	self.assertTrue(self.driver.deploy_lb_called)
