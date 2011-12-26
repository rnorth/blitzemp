import os

from blitzem.model import Node, Size, defaults
from libcloud.compute.deployment import MultiStepDeployment, ScriptDeployment, SSHKeyDeployment

# Can override specific default settings.
defaults["os"] = "Ubuntu 11.10"


"""
==== WEB TIER ====
"""
# A simple node in the 'web' tier
Node(	name="web1",
		tags=["web"])

# A node with more customized settings - also tagged 'peakload' for scaling control
Node(	name="web2",
		os="Ubuntu 11.04",
		tags=["web", "peakload"],
		size=Size(ram=512))

"""
==== APP TIER ====
"""
Node(	name="app1",
		os="Ubuntu 11.04",
		tags=["app"])

# also tagged 'peakload' for scaling control
Node(	name="app2",
		os="Ubuntu 11.04",
		tags=["app", "peakload"])

"""
==== DB TIER ====
"""
Node(	name="db1",
		os="Ubuntu 11.04",
		tags=["db"],
		# We can customize the deployment steps, although the values shown here are
		#  simply the defaults, repeated for visibility.
		# Normally a provisioning tool such as puppet, chef, cfengine or similar should
		#  be used for detailed provisioning - these deployment steps may be used to 
		#  bootstrap the provisioning tool, though.
		deployment=MultiStepDeployment([
			SSHKeyDeployment(open(os.path.expanduser("~/.ssh/id_rsa.pub")).read()),
			ScriptDeployment("apt-get update"),
			ScriptDeployment("apt-get -y install puppet")
		]))