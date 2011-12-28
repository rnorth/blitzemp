""""
model.py

Describes the model of blitzem's DSL.

Copyright (c) 2011 Richard North. All rights reserved.
"""
import os
from libcloud.compute.deployment import MultiStepDeployment, ScriptDeployment, SSHKeyDeployment
from blitzem.deployment import LoggedScriptDeployment

def find_image(conn, name):
	images = [obj for obj in conn.list_images() if obj.name==name]
	if len(images) == 0:
		raise Exception("Could not find an image matching name %s" % name)
	return images[0]

def find_node(conn, name, silent=False):
	
	if not silent:
		print "--  Checking whether node '%s' currently exists" % name
	
	nodes = [obj for obj in conn.list_nodes() if obj.name==name]
	if len(nodes) == 0:
		raise Exception("Node %s not found" % name)
	return nodes[0]

def find_size(conn, size):
	sizes = conn.list_sizes()
	if size.ram != None:
		sizes = [obj for obj in sizes if obj.ram == size.ram]
	if size.disk != None:
		sizes = [obj for obj in sizes if obj.disk == size.disk]
	if len(sizes) == 0:
		raise Exception("Could not find a size for RAM:%s and disk:%s" % (size.ram, size.disk))
	return sizes[0]

libcloud_state_mapping = {
	0: "RUNNING",
	1: "REBOOTING",
	2: "TERMINATED",
	3: "PENDING",
	4: "UNKNOWN"
}

class Size:
	"""
	Represents sizing requirements for a Node.
	"""
	def __init__(self, ram=None, disk=None):
		self.ram = ram
		self.disk = disk

class Node:
	"""
	Represents a single server node.
	"""
	def __init__(self, name, os=None, tags=[], size=None, deployment=None):
		"""
		@type name: C{str}
	    @param name: Name of the node - should be unique.

	    @type os: C{str}
	    @param os: The name of the OS (image) that this node should be built from.

	    @type tags: C{list} of C{str}
	    @param tags: What tags blitzem should recognise this node by (these tags are not stored permanently in server metadata).

		@type size: C{Size}
	    @param size: The size that this node should be.
	
		@type tags: C{Deployment}
	    @param tags: Deployment step (e.g. MultiStepDeployment) to be carried out on the node after creation.
		"""
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

		nodes.append(self)
		# print "Instantiated node %s" % name

	def __repr__(self):
		return "<Node:'%s'; OS:'%s'; Tags:%s>" % (self._name, self._os, self._tags)

	def matches(self, name_or_tag):
		"""
		Does this node meet certain selection criteria? (either by name or matching tag)
		"""
		return (name_or_tag == self._name) or (name_or_tag in self._tags)

	def up(self, driver, conn):
		"""
		Create this node if it doesn't already exist.
		"""
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
		"""
		Destroy this node if it exists.
		"""
		try:
			existing_node = find_node(conn, self._name)
			print "--  Destroying node: %s" % self._name
			existing_node.destroy()
		except Exception:
			print "    Does not exist"

	def reboot(self, driver, conn):
		"""
		Reboot this node.
		"""
		try:
			existing_node = find_node(conn, self._name)
			print "--  Rebooting node: %s" % self._name
			existing_node.reboot()
		except Exception:
			print "    Does not exist"

	def ssh(self, driver, conn):
		"""
		Launch an interactive SSH session to the node. At present this is done simply through a subprocess call
		to the system ssh command.
		"""
		try:
			existing_node = find_node(conn, self._name)
			print "--  Launching SSH connection to node: %s (root@%s:22)" % (self._name, existing_node.public_ips[0])
			subprocess.call(["ssh", "root@%s" % existing_node.public_ips[0] ])
			print "--  SSH Connection terminated"
		except Exception:
			print "    Does not exist"
			
	def status(self, driver, conn):
		try:
			existing_node = find_node(conn, self._name, silent=True)
			status = "UP"
			state = libcloud_state_mapping[existing_node.state]
			size = existing_node.size
			image = existing_node.image
			extra = existing_node.extra
			ip = existing_node.public_ips[0]
		except Exception:
			status = "DOWN"
			ip = "n/a"
			state = ""
			size = ""
			image = ""
			extra = ""
		
		return (self._name, status, ip, str(self._tags), state)
		
"""
Standard defaults that should be used in the absence of specific node settings. Can be overriden in environment.py.
"""
user_public_ssh_key = os.path.expanduser("~/.ssh/id_rsa.pub")
if not os.path.exists(user_public_ssh_key):
	raise Exception("A public SSH key is required for SSH access to nodes, but could not be found at: %s. Please create a public/private keypair and try again." % user_public_ssh_key)
	
defaults ={
	"os": "Ubuntu 11.10",
	"size": Size(ram=256, disk=10),
	"deployment": MultiStepDeployment([
		# Note: This key will be added to the authorized keys for the root user
		# (/root/.ssh/authorized_keys)
		SSHKeyDeployment(open(user_public_ssh_key).read()),
		LoggedScriptDeployment("apt-get update")
	])
}

"""
Maintain a list of known (i.e. specified in environment.py) nodes.
"""
nodes = []