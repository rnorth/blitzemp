import random
import sys

from blitzem.model import Node, Size
from blitzem.test.dummies import DummyDriver, DummyConn

if sys.version_info < (2, 7):
	import unittest2 as unittest 
else:
	import unittest

class TestNode(unittest.TestCase):

	def setUp(self):
		self.node = None
		self.conn = None
		self.driver = DummyDriver()

	def create_dummies(self, node_name="", node_exists=False):
		self.node = Node(	name=node_name, 
							tags=["tag1"],
							size=Size(ram=512))
		self.conn = DummyConn(node_name, node_exists)

	def test_up(self):
		self.create_dummies("nodetocreate", node_exists=False)
		
		self.node.up(self.driver, self.conn)
		self.assertTrue(self.conn.deploy_called)
		
	def test_down(self):
		self.create_dummies("nodetodestroy", node_exists=True)
		
		self.node.down(self.driver, self.conn)
		self.assertTrue(self.conn.dummy_lib_cloud_node.destroy_called)