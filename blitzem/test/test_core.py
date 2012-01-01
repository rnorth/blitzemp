import random
import sys

from blitzem.test.dummies import DummyNode
from blitzem.core import sync
from blitzem.model import nodes

if sys.version_info < (2, 7):
	import unittest2 as unittest 
else:
	import unittest

class TestCore(unittest.TestCase):

	def setUp(self):
		self.dummy_node = DummyNode("dummy")
		nodes.append(self.dummy_node)

	def test_sync_matches_name(self):
		sync('ssh','dummy', compute_driver_override="dummy_driver", compute_conn_override="dummy_conn")
		self.assertTrue(self.dummy_node.matches_called)
		self.assertTrue(self.dummy_node.ssh_called)
		
	def test_sync_no_matches_wrong_name(self):
		sync('ssh','notdummy', compute_driver_override="dummy_driver", compute_conn_override="dummy_conn")
		self.assertTrue(self.dummy_node.matches_called)
		self.assertFalse(self.dummy_node.ssh_called)

