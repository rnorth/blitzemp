""""
model.py

Created by Richard North on 2011-12-26.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import os
from libcloud.compute.deployment import MultiStepDeployment, ScriptDeployment, SSHKeyDeployment
from blitzem.deployment import LoggedScriptDeployment

class Size:
	def __init__(self, ram=None, disk=None):
		self.ram = ram
		self.disk = disk

class Node:
	def __init__(self, name, os=None, tags=[], size=None, deployment=None):
		self._name = name
		if os == None:
			self._os = defaults["os"]
		else:
			self._os = os

		if tags == []:
			self._tags = defaults["tags"]
		else:
			self._tags = tags

		if size == None:
			self._size = defaults["size"]
		else:
			self._size = size

		if deployment == None:
			self._deployment = defaults["deployment"]
		else:
			self._deployment = deployment

		nodes[name] = self
		# print "Instantiated node %s" % name

	def __repr__(self):
		return "<Node:'%s'; OS:'%s'; Tags:%s>" % (self._name, self._os, self._tags)

	def matches(self, name_or_tag):
		return (name_or_tag == self._name) or (name_or_tag in self._tags)

	def up(self, driver, conn):
		try:
			existing_node = find_node(conn, self._name)
			print "    Found node: %s with IP address(es) %s" % (self._name, existing_node.public_ips)
		except Exception:
			print "    Does not exist: %s" % self._name

			size = find_size(conn, self._size)
			print "    Selected size is %s (RAM:%s, Disk: %d, Price: %f)" % (size.name, size.ram, size.disk, size.price)
			image = find_image(conn, self._os)
			print "    Selected image is '%s'" % image.name

			print "    Creating new node named:%s using image: '%s', size: '%s' and tagged %s. Deployment steps will be %s" % (self._name, image.name, size.name, self._tags, self._deployment)
			# deploy_node takes the same base keyword arguments as create_node.
			node = conn.deploy_node(name=self._name, image=image, size=size, deploy=self._deployment)

			print "--  Created node %s (%s)" % (self._name, node.public_ips[0])

	def down(self, driver, conn):
		try:
			existing_node = find_node(conn, self._name)
			print "--  Destroying node: %s" % self._name
			existing_node.destroy()
		except Exception:
			print "    Does not exist"

	def reboot(self, driver, conn):
		try:
			existing_node = find_node(conn, self._name)
			print "--  Rebooting node: %s" % self._name
			existing_node.reboot()
		except Exception:
			print "    Does not exist"

	def ssh(self, driver, conn):
		try:
			existing_node = find_node(conn, self._name)
			print "--  Launching SSH connection to node: %s (root@%s:22)" % (self._name, existing_node.public_ips[0])
			subprocess.call(["ssh", "root@%s" % existing_node.public_ips[0] ])
			print "--  SSH Connection terminated"
		except Exception:
			print "    Does not exist"

defaults ={
	"os": "Ubuntu 11.10",
	"size": Size(ram=256, disk=10),
	"deployment": MultiStepDeployment([
		# Note: This key will be added to the authorized keys for the root user
		# (/root/.ssh/authorized_keys)
		SSHKeyDeployment(open(os.path.expanduser("~/.ssh/id_rsa.pub")).read()),
		LoggedScriptDeployment("apt-get update")
	])
}

nodes = {}