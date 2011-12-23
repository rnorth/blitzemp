from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.deployment import MultiStepDeployment, ScriptDeployment, SSHKeyDeployment
import libcloud.security
import os
from os import path
import ConfigParser
import subprocess
import paramiko

libcloud.security.VERIFY_SSL_CERT = False
# paramiko.util.log_to_file('paramiko.log')

class Size:
	def __init__(self, ram=None, disk=None):
		self.ram = ram
		self.disk = disk

defaults ={
	"os": "Ubuntu 11.10",
	"size": Size(ram=256, disk=10),
	"deployment": MultiStepDeployment([
		# Note: This key will be added to the authorized keys for the root user
		# (/root/.ssh/authorized_keys)
		SSHKeyDeployment(open(os.path.expanduser("~/.ssh/id_rsa.pub")).read()),
		ScriptDeployment("apt-get update")
	])
}

nodes = {}


def find_image(conn, name):
	images = [obj for obj in conn.list_images() if obj.name==name]
	if len(images) == 0:
		raise Exception("Could not find an image matching name %s" % name)
	return images[0]

def find_node(conn, name):
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
		raise Exception("Could not find a size for RAM:%d and disk:%d" % (size.ram, size.disk))
	return sizes[0]

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
		print "-- Checking whether node '%s' currently exists" % self._name

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

			print "    Created node %s" % node
	
	def down(self, driver, conn):
		print "-- Checking whether node '%s' currently exists" % self._name

		try:
			existing_node = find_node(conn, self._name)
			print "    Destroying node: %s" % self._name
			existing_node.destroy()
		except Exception:
			print "    Does not exist"
	
	def reboot(self, driver, conn):
		print "-- Checking whether node '%s' currently exists" % self._name

		try:
			existing_node = find_node(conn, self._name)
			print "    Rebooting node: %s" % self._name
			existing_node.reboot()
		except Exception:
			print "    Does not exist"

	def ssh(self, driver, conn):
		print "-- Checking whether node '%s' currently exists" % self._name

		try:
			existing_node = find_node(conn, self._name)
			print "    Launching SSH connection to node: %s (root@%s:22)" % (self._name, existing_node.public_ips[0])
			subprocess.call(["ssh", "root@%s" % existing_node.public_ips[0] ])
			print "    ====== SSH CONNECTION TERMINATED ======"
		except Exception:
			print "    Does not exist"

def process_settings():

	config_file = path.expanduser('~/.blitz.cfg')
	config = ConfigParser.SafeConfigParser()
	config.read(config_file)
	if not config.has_section('general'):
		config.add_section('general')
	if not config.has_section('rackspace'):
		config.add_section('rackspace')
	
	try:
		username = config.get('rackspace', 'username')
		api_key = config.get('rackspace','api_key')
	except ConfigParser.NoOptionError:
		username = raw_input("Rackspace Username: ")
		api_key = raw_input("Rackspace API Key: ")

	config.set('rackspace', 'username', username)
	config.set('rackspace', 'api_key', api_key)
	config.write(open(config_file, 'w'))

	Driver = get_driver(Provider.RACKSPACE_UK)
	conn = Driver(username, api_key)

	return (Driver, conn)

def sync(command, tag):

	(Driver, conn) = process_settings()

	print "\n\n"

	for nodename, node in nodes.items():
		if node.matches(tag) or tag == "":
			print "Applying command (%s) to node: %s" % (command, nodename)
			if command == "up":
				node.up(Driver, conn)
			if command == "down":
				node.down(Driver, conn)
			if command == "reboot":
				node.reboot(Driver, conn)
			if command == "ssh":
				node.ssh(Driver, conn)
			print "\n"
