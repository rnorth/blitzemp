#!/usr/bin/env python

import sys

from blitzem.core import sync

def main():

	execfile("environment.py", locals(), globals())

	command = sys.argv[1]
	if len(sys.argv) > 2:
		tag = sys.argv[2]
		print "Blitzing nodes named/tagged '%s' %s\n\n" % (tag, command)
	else:
		tag = ""
		print "Blitzing all nodes %s\n\n" % command

	sync(command, tag)
