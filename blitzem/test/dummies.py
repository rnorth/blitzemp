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
	pass

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