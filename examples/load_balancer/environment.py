import os

from blitzem.model import Node, LoadBalancer, Size, defaults, user_public_ssh_key
from libcloud.compute.deployment import MultiStepDeployment, ScriptDeployment, SSHKeyDeployment
from blitzem.deployment import LoggedScriptDeployment

defaults["deployment"] = MultiStepDeployment([
		# Note: This key will be added to the authorized keys for the root user
		# (/root/.ssh/authorized_keys)
		SSHKeyDeployment(open(user_public_ssh_key).read()),
		# Serve a simple text file on each node to demonstrate load balancing effect
		LoggedScriptDeployment("apt-get update; apt-get install dtach"),
		LoggedScriptDeployment("mkdir web; cd web; hostname > hostname.txt; dtach -n /tmp/simple_http.worker python -m SimpleHTTPServer 8080")
	])



"""
==== WEB TIER ====
"""

LoadBalancer(	name="web_lb1",
				applies_to_tag="web",
				port=8080,
				protocol="http")

# A simple pair of nodes in the 'web' tier
Node(	name="web1",
		tags=["web"])

Node(	name="web2",
		tags=["web"])
