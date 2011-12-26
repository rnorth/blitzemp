""""
core.py

Incorporates blitzem's core control-flow logic and processing of settings file.

Copyright (c) 2011 Richard North. All rights reserved.
"""
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

	selected_driver = get_driver(Provider.RACKSPACE_UK)
	established_conn = selected_driver(username, api_key)

	return (selected_driver, established_conn)

def sync(command, tag, driver_override=None, conn_override=None):
	
	driver = driver_override
	conn = conn_override
	if driver==None or conn==None:
		(driver, conn) = process_settings()

	print "\n\n"

	for nodename, node in nodes.items():
		if node.matches(tag) or tag == "":
			print "--  Applying command (%s) to node: %s" % (command, nodename)
			if command == "up":
				node.up(driver, conn)
			if command == "down":
				node.down(driver, conn)
			if command == "reboot":
				node.reboot(driver, conn)
			if command == "ssh":
				node.ssh(driver, conn)
			print "\n"