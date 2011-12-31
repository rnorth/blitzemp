=========
Blitz 'em
=========

blitzem is a simple cloud server management tool, inspired by Vagrant. This tool is just a proof-of-concept at the current time, and quite likely to change.

Copyright Richard North 2011, released under the BSD Licence (see LICENCE.txt).

Install using pip
=================

Enter::

    pip install blitzem

Building from source
====================

Enter::

    python setup.py install

Usage
=====

Tailor the environment.py file to suit your desired server environment - example content shown here::

    LoadBalancer(   name="web_lb1",
                    applies_to_tag="web",     # all nodes matching this tag will be fronted by this LB
                    port=8080,                # what input & output port should be balanced
                    protocol="http")

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

With an environment.py in the current working directory, the ``blitzem`` command can be used to control the environment. For example::

   $ blitzem up                    # will launch all nodes if they are not already running

   $ blitzem up app                # will launch just the nodes tagged 'app' if they're not already running

   $ blitzem down web              # brings down all 'web' tagged nodes

   $ blitzem up peakload           # brings up 'peakload' nodes (e.g. during peak periods of the day)

   $ blitzem ssh db1               # launches an interactive SSH session to db1

   $ blitzem reboot web            # runs a reboot of the 'web' tier

   $ blitzem status                # displays a status table similar to the below:
   Blitzing all nodes status

   --  Retrieving status of all nodes
   Name Status  IP Address      Tags    State  
   ---- ------  -------------   ------- -------
   web1 UP      31.222.171.85   ['web'] RUNNING
   web2 UP      31.222.171.86   ['web'] RUNNING

   Unmatched nodes (live in cloud but not present in environment.py):
   serverA  46.38.172.52

   $ blitzem hostfile              # for convenience, enumerate nodes in /etc/hosts format
   Blitzing all nodes hostfile

   -- Retrieving node information for /etc/hosts
   46.38.172.52 serverA
   31.222.171.85    web1
   31.222.171.86    web2



Limitations
===========

* Only supports Rackspace Cloud UK as a service provider

* Other issues/potential improvements listed here

* This tool is highly experimental and the author takes absolutely no responsibility for any consequences of its use!

Building notes
==============

On ubuntu, the following packages must be installed to enable blitzem to be built (mainly for the prerequisites of apache libcloud). Other platforms may have similar requirements if not already installed:

* python-dev

* gcc

* python-setuptools

* python-virtualenv

* libbz2-dev