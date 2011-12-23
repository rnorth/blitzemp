from blitz import Node, Size, defaults

defaults["os"] = "Ubuntu 11.10"

Node(	name="web1",
		tags=["web"])

Node(	name="web2",
		os="Ubuntu 11.04",
		tags=["web", "peakload"],
		size=Size(ram=512))

Node(	name="app1",
		os="Ubuntu 11.04",
		tags=["app"])

Node(	name="app2",
		os="Ubuntu 11.04",
		tags=["app", "peakload"])

Node(	name="db1",
		os="Ubuntu 11.04",
		tags=["db"])