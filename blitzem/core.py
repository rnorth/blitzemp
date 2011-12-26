from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.deployment import MultiStepDeployment, ScriptDeployment, SSHKeyDeployment

from blitzem.model import Size, Node, defaults, nodes

import libcloud.security
import os
from os import path
import textwrap
import ConfigParser
import subprocess
import paramiko

libcloud.security.VERIFY_SSL_CERT = False
# paramiko.util.log_to_file('paramiko.log')

def find_image(conn, name):
	images = [obj for obj in conn.list_images() if obj.name==name]
	if len(images) == 0:
		raise Exception("Could not find an image matching name %s" % name)
	return images[0]

def find_node(conn, name):
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
		raise Exception("Could not find a size for RAM:%d and disk:%d" % (size.ram, size.disk))
	return sizes[0]

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
			print "--  Applying command (%s) to node: %s" % (command, nodename)
			if command == "up":
				node.up(Driver, conn)
			if command == "down":
				node.down(Driver, conn)
			if command == "reboot":
				node.reboot(Driver, conn)
			if command == "ssh":
				node.ssh(Driver, conn)
			print "\n"
