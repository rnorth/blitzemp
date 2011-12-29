import random
import sys

from blitzem.model import Node, Size

if sys.version_info < (2, 7):
	import unittest2 as unittest 
else:
	import unittest

class DummySize():
	def __init__(self):
		self.ram = 512
		self.disk = 10
		self.price = 0.0
		self.name = "512mb DUMMY server"
dummy_size = DummySize()

class DummyImage():
	def __init__(self):
		self.name = "Ubuntu 11.10"
dummy_image = DummyImage()

class DummyDriver():
	def __init__(self):
		print "Created DummyDriver"

class DummyLibCloudNode():
	def __init__(self, nodename):
		self.public_ips = ["ip1", "ip2"]
		self.destroy_called = False
		self.name = nodename
	
	def destroy(self):
		self.destroy_called = True

class DummyConn():
	def __init__(self, node_name="", node_exists = False):
		print "Created DummyConn"
		self.node_name = node_name
		self.deploy_called = False
		self.dummy_lib_cloud_node = DummyLibCloudNode(node_name)
		self.node_exists = node_exists
	def list_sizes(self):
		return [dummy_size]
	def list_images(self):
		return [dummy_image]
	def list_nodes(self):
		if self.node_exists:
			return [self.dummy_lib_cloud_node]
		else:
			return []
	def deploy_node(self, name, image, size, deploy):
		self.deploy_called = True
		assert name == self.node_name
		assert image == dummy_image
		assert size == dummy_size
		return self.dummy_lib_cloud_node
		

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