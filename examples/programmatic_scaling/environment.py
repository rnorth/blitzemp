"""
Demonstrates one potential technique of scaling active nodes during peak hours - tagging
servers with 'scheduled_up'/'_down' if they should be on at the time when blitzem is executed.

A crontab could then be used to automatically scale capacity, e.g:
 0 * * * *     blitzem up   scheduled_up
 1 * * * *     blitzem down scheduled_down
"""

import os
from datetime import datetime

from blitzem.model import Node, Size, defaults
from libcloud.compute.deployment import MultiStepDeployment, ScriptDeployment, SSHKeyDeployment

"""
==== WEB TIER ====
"""

base_server_count = 2
peak_server_count = 4
peak_hours = range(13,14) # 13:00 to 14:59

is_peak_period = datetime.now().hour in peak_hours

for i in range(0, peak_server_count):
	
	tags = ["web"]
	if i >= base_server_count:
		# this is a peak-only server
		if is_peak_period:
			tags.append("scheduled_up")
		else:
			tags.append("scheduled_down")
	else:
		tags.append("scheduled_up")
	
	Node( name="web%d" % (i+1), tags = tags)
	