"""
deployment.py

Created by Richard North on 2011-12-26.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
from libcloud.compute.deployment import ScriptDeployment

def format(text, indent=2):
	return (" " * indent) + ("\n" + (" " * indent)).join(text.split("\n"))

class LoggedScriptDeployment(ScriptDeployment):
	def run(self, node, client):
		"""
		Uploads the shell script and then executes it, and also prints out any stdout/stderr resulting from the script.

		See also L{ScriptDeployment.run}
		"""

		print "    > Exec: %s" % self.script

		super(LoggedScriptDeployment, self).run(node, client)
		
		print "    > STDOUT: \n%s" % format(self.stdout, indent=14)
		print "    > STDERR: \n%s" % format(self.stderr, indent=14)
		print "    > Exit Status: %s" % self.exit_status

def main():
	pass


if __name__ == '__main__':
	main()
