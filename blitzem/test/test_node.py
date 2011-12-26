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
	def __init__(self):
		self.public_ips = ["ip1", "ip2"]

class DummyConn():
	def __init__(self):
		print "Created DummyConn"
		self.deploy_called = False
	def list_sizes(self):
		return [dummy_size]
	def list_images(self):
		return [dummy_image]
	def deploy_node(self, name, image, size, deploy):
		self.deploy_called = True
		assert name == "node"
		assert image == dummy_image
		assert size == dummy_size
		return DummyLibCloudNode()
		

class TestNode(unittest.TestCase):

	def setUp(self):
		self.node = Node(	name="node", 
							tags=["tag1"],
							size=Size(ram=512))
		self.driver = DummyDriver()
		self.conn = DummyConn()

	def test_up(self):
		self.node.up(self.driver, self.conn)
		self.assertTrue(self.conn.deploy_called)
		# self.assertTrue(self.dummy_node.ssh_called)