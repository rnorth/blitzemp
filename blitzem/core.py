""""
core.py

Incorporates blitzem's core control-flow logic and processing of settings file.

Copyright (c) 2011 Richard North. All rights reserved.
"""
from libcloud.compute.types import Provider as Compute_Provider
from libcloud.loadbalancer.types import Provider as LB_Provider
from libcloud.compute.providers import get_driver as get_compute_driver
from libcloud.loadbalancer.providers import get_driver as get_lb_driver
from libcloud.compute.deployment import MultiStepDeployment, ScriptDeployment, SSHKeyDeployment

from blitzem.model import Size, Node, defaults, nodes, load_balancers
from blitzem.print_table import print_table

import libcloud.security
import os
from os import path
import textwrap
import ConfigParser
import paramiko
from urllib import urlretrieve

"""
 Ensure that SSL certs are available - no suitable certs are bundled on OS X, so
  must download from some source. We use the cURL pre-prepared CA bundle.
  See http://wiki.apache.org/incubator/LibcloudSSL
"""
cert_found = False
for cert_path in libcloud.security.CA_CERTS_PATH:
	if path.exists(cert_path):
		cert_found = True
if not cert_found:
	print "No system SSL Certs found in potential paths (tried %s)." % libcloud.security.CA_CERTS_PATH
	downloaded_cert_path = path.abspath("curl-ca-bundle.crt")
	if not path.exists(downloaded_cert_path):
		curl_ca_bundle = "http://curl.haxx.se/ca/cacert.pem"
		print "Downloading cURL SSL Cert bundle from %s" % curl_ca_bundle
		urlretrieve(curl_ca_bundle, downloaded_cert_path)
	print "Using cURL SSL Cert bundle at %s" % downloaded_cert_path
	libcloud.security.CA_CERTS_PATH.append(downloaded_cert_path)

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

	compute_driver = get_compute_driver(Compute_Provider.RACKSPACE_UK)
	lb_driver = get_lb_driver(LB_Provider.RACKSPACE_UK)(username, api_key)
	established_compute_conn = compute_driver(username, api_key)

	return (compute_driver, lb_driver, established_compute_conn)

def sync(command, tag, driver_override=None, conn_override=None):
	
	driver = driver_override
	conn = conn_override
	if driver==None or conn==None:
		(compute_driver, lb_driver, established_compute_conn) = process_settings()
	
	if command == "status":
		print "--  Retrieving status of all nodes"
		
		table_data = [("Name", "Status", "IP Address", "Tags", "State")]
		for node in nodes:
			table_data.append(node.status(compute_driver, established_compute_conn))
		print_table(table_data)
		
		print "\nUnmatched nodes (live in cloud but not present in environment.py):"
		nodenames = [obj._name for obj in nodes]
		unmatched_nodes = [(obj.name, obj.public_ips[0]) for obj in established_compute_conn.list_nodes() if obj.name not in nodenames]
		for node in unmatched_nodes:
			print "%s\t%s" % node
		
		return
		
	if command == "hostfile":
		print "-- Retrieving node information for /etc/hosts"
		existing_nodes = [(obj.public_ips[0], obj.name) for obj in established_compute_conn.list_nodes()]
		for node in existing_nodes:
			print "%s\t%s" % node
		return

	for node in nodes:
		if node.matches(tag) or tag == "":
			print "--  Applying command (%s) to node: %s" % (command, node._name)
			if command == "up":
				node.up(compute_driver, established_compute_conn)
			if command == "down":
				node.down(compute_driver, established_compute_conn)
			if command == "reboot":
				node.reboot(compute_driver, established_compute_conn)
			if command == "ssh":
				node.ssh(compute_driver, established_compute_conn)
			print "\n"
	
	for load_balancer in load_balancers:
		if load_balancer.matches(tag) or tag == "":
			print "--  Applying command (%s) to load balancer: %s" % (command, load_balancer._name)
			if command == "up":
				load_balancer.up(compute_driver, established_compute_conn, lb_driver)
			if command == "down":
				load_balancer.down(lb_driver)