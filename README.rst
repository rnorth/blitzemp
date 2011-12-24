=========
Blitz 'em
=========

blitzem is a simple cloud server management tool, inspired by Vagrant. This tool is just a proof-of-concept at the current time, and quite likely to change.

Copyright Richard North 2011, released under the BSD Licence (see LICENCE.txt).

Installation
============

    python setup.py install

Usage
=====

Tailor the environment.py file to suit your desired server environment - example content shown here::

    Node( name="web1",
          tags=["web"])

    Node(   name="web2",
          os="Ubuntu 11.04",
          tags=["web", "peakload"],
          size=Size(ram=512))

    Node(   name="app1",
          os="Ubuntu 11.04",
          tags=["app"])

    Node(   name="app2",
          os="Ubuntu 11.04",
          tags=["app", "peakload"])

    Node(   name="db1",
          tags=["db"],
          size=Size(ram=8192),
          deployment=MultiStepDeployment([
                            SSHKeyDeployment(open(os.path.expanduser("~/.ssh/id_rsa.pub")).read()),
                            ScriptDeployment("apt-get update"),
                            ScriptDeployment("apt-get -y install puppet")])))

Using the configuration example given above:

* web1 and db1 will inherit default 'OS' settings rather than specifying their own

* web1 and web2 will be tagged in the 'web' tier of servers, while app1 and app2 will be tagged in the 'app' tier

* web2 and app2 are also tagged 'peakload', which allows them to be brought up/down separately

* all nodes will be sized at the default 256MB RAM, except web2 and db1, which will be 512MB and 8192MB instances respectively

* db1 will have custom deployment steps (additional installation of puppet, on top of the defaults)

For example:

   $ blitzem up                    # will launch all nodes if they are not already running

   $ blitzem up app                # will launch just the nodes tagged 'app' if they're not already running

   $ blitzem down web              # brings down all 'web' tagged nodes

   $ blitzem up peakload           # brings up 'peakload' nodes (e.g. during peak periods of the day)

   $ blitzem ssh db1               # launches an interactive SSH session to db1

   $ blitzem reboot web            # runs a reboot of the 'web' tier


Limitations
===========

* Only supports Rackspace Cloud UK as a service provider

* Other issues/potential improvements listed here

* This tool is highly experimental and the author takes absolutely no responsibility for any consequences of its use!
